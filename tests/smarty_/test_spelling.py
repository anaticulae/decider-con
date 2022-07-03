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
import utilatest

import decider_smarty
import tests.smarty_


def decide_smarty_spelling(source, pages, testdir, monkeypatch, msgid=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.smarty_.run(
        f'--spelling -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_smarty.path.spelling(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgid)
    return findings


def test_smarty_spelling_hyphen(testdir, monkeypatch):
    findings = decide_smarty_spelling(
        power.BACHELOR077_PDF,
        ':',
        testdir,
        monkeypatch,
        msgid=8200,
    )
    assert len(findings) >= 5
