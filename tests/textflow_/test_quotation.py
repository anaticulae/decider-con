# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import decider_textflow.path
import tests.textflow_


def run_quotation_linter(source, pages, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    pages = utila.from_tuple(pages, separator=',')
    cmd = f'-i={source} --quotation --pages={pages}'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    result = serializeraw.load_findings(
        decider_textflow.path.quotation_linted(testdir.tmpdir))
    return result


@utilatest.longrun
def test_home18_quotation_start_with_ellipsis(testdir, monkeypatch):
    source = power.link(power.HOME018_PDF)
    result = run_quotation_linter(source, (7,), testdir, monkeypatch)
    assert not result
