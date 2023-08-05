# -*- coding: utf-8 -*-
#
# This file is part of hepcrawl.
# Copyright (C) 2017 CERN.
#
# hepcrawl is a free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Functional tests for Desy spider"""

from __future__ import absolute_import, division, print_function

import copy
import hashlib
import os
from time import sleep

import pytest

from hepcrawl.testlib.celery_monitor import CeleryMonitor
from hepcrawl.testlib.fixtures import (
    get_test_suite_path,
    expected_json_results_from_file,
    clean_dir,
)
from hepcrawl.testlib.tasks import app as celery_app
from hepcrawl.testlib.utils import get_crawler_instance


def override_dynamic_fields_on_records(records):
    clean_records = []
    for record in records:
        clean_record = override_dynamic_fields_on_record(record)
        clean_records.append(clean_record)

    return clean_records


def override_dynamic_fields_on_record(record):
    def _override(field_key, original_dict, backup_dict, new_value):
        backup_dict[field_key] = original_dict[field_key]
        original_dict[field_key] = new_value

    clean_record = copy.deepcopy(record)
    overriden_fields = {}
    dummy_random_date = u'2017-04-03T10:26:40.365216'

    overriden_fields['acquisition_source'] = {}
    _override(
        field_key='datetime',
        original_dict=clean_record['acquisition_source'],
        backup_dict=overriden_fields['acquisition_source'],
        new_value=dummy_random_date,
    )
    _override(
        field_key='submission_number',
        original_dict=clean_record['acquisition_source'],
        backup_dict=overriden_fields['acquisition_source'],
        new_value=u'5652c7f6190f11e79e8000224dabeaad',
    )

    return clean_record


def assert_files_equal(file_1, file_2):
    """Compares two files calculating the md5 hash."""
    def _generate_md5_hash(file_path):
        hasher = hashlib.md5()
        with open(str(file_path), 'rb') as fd:
            buf = fd.read()
            hasher.update(buf)
            return hasher.hexdigest()

    file_1_hash = _generate_md5_hash(file_1)
    file_2_hash = _generate_md5_hash(file_2)
    assert file_1_hash == file_2_hash


def assert_ffts_content_matches_expected(record):
    for fft_field in record.get('_fft', []):
        assert_fft_content_matches_expected(fft_field)


def assert_fft_content_matches_expected(fft_field):
    expected_file_name = get_file_name_from_fft(fft_field)
    assert_files_equal(expected_file_name, fft_field['path'])


def get_file_name_from_fft(fft_field):
    file_path = get_test_suite_path(
        'desy',
        'fixtures',
        'ftp_server',
        'DESY',
        'FFT',
        fft_field['filename'] + fft_field['format'],
        test_suite='functional',
    )
    return file_path


def get_ftp_settings():
    netrc_location = get_test_suite_path(
        'desy',
        'fixtures',
        'ftp_server',
        '.netrc',
        test_suite='functional',
    )

    return {
        'CRAWLER_HOST_URL': 'http://scrapyd:6800',
        'CRAWLER_PROJECT': 'hepcrawl',
        'CRAWLER_ARGUMENTS': {
            'ftp_host': 'ftp_server',
            'ftp_netrc': netrc_location,
        }
    }


def get_local_settings():
    package_location = get_test_suite_path(
        'desy',
        'fixtures',
        'ftp_server',
        'DESY',
        test_suite='functional',
    )

    return {
        'CRAWLER_HOST_URL': 'http://scrapyd:6800',
        'CRAWLER_PROJECT': 'hepcrawl',
        'CRAWLER_ARGUMENTS': {
            'source_folder': package_location,
        }
    }


@pytest.fixture(scope="function")
def cleanup():
    # The test must wait until the docker environment is up (takes about 10
    # seconds).
    sleep(10)
    yield

    clean_dir(path=os.path.join(os.getcwd(), '.scrapy'))
    clean_dir('/tmp/file_urls')
    clean_dir('/tmp/DESY')


@pytest.mark.parametrize(
    'expected_results, settings',
    [
        (
            expected_json_results_from_file(
                'desy',
                'fixtures',
                'desy_ftp_records_expected.json',
            ),
            get_ftp_settings(),
        ),
        (
            expected_json_results_from_file(
                'desy',
                'fixtures',
                'desy_local_records_expected.json',
            ),
            get_local_settings(),
        )

    ],
    ids=[
        'ftp package',
        'local package'
    ]
)
def test_desy(
    expected_results,
    settings,
    cleanup,
):
    crawler = get_crawler_instance(
        settings.get('CRAWLER_HOST_URL')
    )

    results = CeleryMonitor.do_crawl(
        app=celery_app,
        monitor_timeout=5,
        monitor_iter_limit=100,
        events_limit=2,
        crawler_instance=crawler,
        project=settings.get('CRAWLER_PROJECT'),
        spider='desy',
        settings={},
        **settings.get('CRAWLER_ARGUMENTS')
    )

    results = sorted(results, key=lambda x: x['control_number'])

    gotten_results = override_dynamic_fields_on_records(results)
    expected_results = override_dynamic_fields_on_records(expected_results)

    assert gotten_results == expected_results

    for record in gotten_results:
        assert_ffts_content_matches_expected(record)
