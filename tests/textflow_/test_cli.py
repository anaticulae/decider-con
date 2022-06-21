# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests.textflow_


def test_cli_help(monkeypatch):
    tests.textflow_.run('--help', monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(power.TECH024_PDF, id='technical24'),
    pytest.param(power.BACHELOR037_PDF, id='bachelor37'),
    pytest.param(power.BACHELOR076_PDF, id='bachelor76'),
    pytest.param(power.DOCU035_PDF, id='docu35'),
    pytest.param(power.BOOK007_PDF, id='book7'),
    pytest.param(power.MASTER072_PDF, id='master72'),
    pytest.param(power.MASTER078_PDF, id='master78'),
    pytest.param(power.MASTER098_PDF, id='master98'),
    pytest.param(power.MASTER099_PDF, id='master99'),
])
@utilatest.nightly
def test_cli_textflow_example(source, testdir, monkeypatch):
    """Run textflow"""
    source = power.link(source)
    # TODO: MOVE TO TEST DATA GENERATOR
    utila.run(f'textflow -i {source}')
    cmd = f'-i {source}'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
