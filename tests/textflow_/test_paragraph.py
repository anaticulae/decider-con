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
import serializeraw
import utila
import utilatest

import decider_textflow.path
import tests
import tests.textflow_


def run_paragraph_length_linter(source, pages, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    source = power.link(source)
    pages = utila.from_tuple(pages, separator=',')
    cmd = f'-i={source} --paragraph --pages={pages}'
    # run textflow
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    result = serializeraw.load_findings(
        decider_textflow.path.paragraph_linted(testdir.tmpdir),
        7630,
    )
    return result


@utilatest.longrun
@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR090_PDF, (12, 13, 14), 5, id='bachelor90'),
    pytest.param(power.MASTER116_PDF, (18,), 0, id='master116'),
])
def test_paragraph_too_short(source, pages, expected, testdir, monkeypatch):
    result = run_paragraph_length_linter(source, pages, testdir, monkeypatch)
    assert len(result) == expected, str(result)  # TODO: VALIDATE LATER


@utilatest.longrun
def test_list_no_paragraph_too_short(testdir, monkeypatch):
    source = power.MASTER072_PDF
    pages = (7,)
    result = run_paragraph_length_linter(source, pages, testdir, monkeypatch)
    result = [item for item in result if item.location.page == 7]
    # TODO: This content before a list should not be an error
    # REMAINING ERROR:
    # O’Reilly nennt in seinem Artikel sieben Hauptpunkte, die das Web 2.0
    # kennzeichnen10:
    assert len(result) == 1, str(result)
