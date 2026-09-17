# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import tests.textflow_
import textflow_.path


def textflow__character(
    source,
    pages,
    td,
    mp,
    msgids=None,
):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'--writing -i {source} --pages={pages} --character',
        mp=mp,
    )
    path = textflow_.path.character_linted(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@utilotest.longrun
def test_textflow_character_space_before_comma(td, mp):
    findings = textflow__character(
        hoverpower.BACHELOR090_PDF,
        '30',
        td,
        mp,
        msgids=7650,
    )
    assert len(findings) == 1


@utilotest.nightly
def test_textflow_character_missing_space_after_comma(td, mp):
    findings = textflow__character(
        hoverpower.BACHELOR090_PDF,
        ':',
        td,
        mp,
        msgids=7651,
    )
    assert len(findings) == 2


@utilotest.longrun
def test_textflow_character_space_before_square_bracket(td, mp):
    findings = textflow__character(
        hoverpower.BACHELOR090_PDF,
        ':',
        td,
        mp,
        msgids=7652,
    )
    assert len(findings) == 2


@pytest.mark.xfail(reason='layout parser?')
@utilotest.longrun
def test_textflow_character_space_after_square_bracket(td, mp):
    """[ Hello24]."""
    findings = textflow__character(
        hoverpower.BACHELOR090_PDF,
        ':',
        td,
        mp,
        msgids=7653,
    )
    assert len(findings) == 2


@pytest.mark.xfail(reason='ana is changed from all to sentence only')
@utilotest.longrun
def test_textflow_character_missing_space_before_semicolon(td, mp): # yapf:disable
    findings = textflow__character(
        hoverpower.BACHELOR090_PDF,
        ':',
        td,
        mp,
        msgids=7654,
    )
    assert len(findings) == 22  # TODO: VALIDATE LATER


@utilotest.longrun
def test_missing_space_after_semicolon_master110_page59(
    td,
    mp,
):
    """Verify that magic content skips errors located in formula."""
    findings = textflow__character(
        hoverpower.MASTER110_PDF,
        '59',
        td,
        mp,
        msgids=7655,
    )
    # works after fixing rawmaker, or formula detector?
    assert not findings


@pytest.mark.xfail(reason='require line formula inside parser')
@utilotest.longrun
def test_character_missing_space_after_comma_master116_page23(
    td,
    mp,
):
    """False positve comma detection.

    TODO: In the current implementation `𝑐𝑤,anfang=0.23` is detected
    as an false positiv error. After introduce a inline formula
    detector, this problem can be solved.
    """
    findings = textflow__character(
        hoverpower.MASTER116_PDF,
        '23',
        td,
        mp,
        msgids=7651,
    )
    assert not findings


def test_bachelor028_highnote_space(td, mp):
    """\
    page:17
    Dabei geht die Anti-BEPS-Richtlinie zum Teil auch inhaltlich
    deutlich über die OECDEmpfehlungen hinaus. 60 Erstens,
    """
    findings = textflow__character(
        hoverpower.BACHELOR028_PDF,
        '17',
        td,
        mp,
        msgids=7666,
    )
    assert len(findings) == 3  # VALIDATED
