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

import decider_textflow.path
import tests.textflow_


def decide_textflow(source, pages, testdir, monkeypatch, msgids=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.textflow_.run(
        f'--docref -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.docref_linted(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


def test_bachelor76_docref_negative(testdir, monkeypatch):
    """This document contains only valid references.

    Therefore we do not detect any missing references.
    """
    source = power.BACHELOR076_PDF
    pages = '0:30'
    findings = decide_textflow(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids={7200, 7202},
    )
    assert not findings


def test_bachelor76_figure_missing_intext_ref(testdir, monkeypatch):
    """Remove this test after extending docref intext parser.

    Pattern: 'Die folgende Abbildung soll durch' not supported yet.
    """
    source = power.BACHELOR076_PDF
    pages = '0:30'
    findings = decide_textflow(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids={7200, 7202},
    )
    assert not findings


def test_master75_docref(testdir, monkeypatch):
    # TODO: DESCRIBE PURPOSE OF TEST
    source = power.MASTER075_PDF
    findings = decide_textflow(
        source,
        ':',
        testdir,
        monkeypatch,
        msgids={7200, 7202},
    )
    assert not findings  # may changes later


def test_bachelor56page15_tableref(testdir, monkeypatch):
    """Verify that `s. Tab. 1` matches with `Tabelle 1`"""
    source = power.BACHELOR056_PDF
    pages = '15'
    findings = decide_textflow(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids={7202},
    )
    assert not findings
