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
import utilatest

import decider_textflow.path
import tests.textflow_


def decider_textflow_character(
    source,
    pages,
    testdir,
    monkeypatch,
    msgids=None,
):
    utilatest.fixture_requires(source)
    tests.textflow_.run(
        f'--writing -i {source} --pages={pages} --character',
        monkeypatch=monkeypatch,
    )
    path = decider_textflow.path.character_linted(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


def test_textflow_character_space_before_comma(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = '30'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7650,
    )
    assert len(findings) == 1


@utilatest.nightly
def test_textflow_character_missing_space_after_comma(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7651,
    )
    assert len(findings) == 2


@utilatest.longrun
def test_textflow_character_space_before_square_bracket(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7652,
    )
    assert len(findings) == 2


@pytest.mark.xfail(reason='layout parser?')
@utilatest.longrun
def test_textflow_character_space_after_square_bracket(testdir, monkeypatch):
    """[ Hello24]."""
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7653,
    )
    assert len(findings) == 2


@pytest.mark.xfail(reason='ana is changed from all to sentence only')
@utilatest.longrun
def test_textflow_character_missing_space_before_semicolon(testdir, monkeypatch): # yapf:disable
    source = power.link(power.BACHELOR090_PDF)
    pages = ':'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7654,
    )
    assert len(findings) == 22  # TODO: VALIDATE LATER


@utilatest.longrun
def test_missing_space_after_semicolon_master110_page59(
    testdir,
    monkeypatch,
):
    """Verify that magic content skips errors located in formula."""
    source = power.link(power.MASTER110_PDF)
    pages = '59'
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7655,
    )
    # works after fixing rawmaker, or formula detector?
    assert not findings


@pytest.mark.xfail(reason='require line formula inside parser')
@utilatest.longrun
def test_character_missing_space_after_comma_master116_page23(
    testdir,
    monkeypatch,
):
    """False positve comma detection. TODO: In the current
    implementation `𝑐𝑤,anfang=0.23` is detected as an false positiv
    error. After introduce a inline formula detector, this problem can
    be solved."""
    source = power.link(power.MASTER116_PDF)
    pages = 23
    findings = decider_textflow_character(
        source,
        pages,
        testdir,
        monkeypatch,
        msgids=7651,
    )
    assert not findings


def test_bachelor028_highnote_space(testdir, monkeypatch):
    """\
    page:17
    Dabei geht die Anti-BEPS-Richtlinie zum Teil auch inhaltlich
    deutlich über die OECDEmpfehlungen hinaus. 60 Erstens,
    """
    source = power.link(power.BACHELOR028_PDF)
    findings = decider_textflow_character(
        source,
        '17',
        testdir,
        monkeypatch,
        msgids=7666,
    )
    assert len(findings) == 3  # VALIDATED
