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

import decider_textflow.features.writing
import decider_textflow.path
import tests.textflow_


def decide_textflow(source, td, mp, pages=None, msgids=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'--writing -i {source} '
    if pages:
        cmd += f'--pages={pages}'
    tests.textflow_.run(cmd, mp=mp)
    path = decider_textflow.path.writing_linted(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@utilatest.nightly
def test_bachelor76_perspective(td, mp):
    source = power.BACHELOR076_PDF
    findings = decide_textflow(source, td, mp, msgids=7600)
    assert len(findings) == 5  # VALIDATED


@pytest.mark.xfail(reason='man in quotation')
@utilatest.longrun
def test_master72_writing_quotation(td, mp):
    """Do not detect errors in perspective inside quotations."""
    source = power.MASTER072_PDF
    pages = '12:15'
    findings = decide_textflow(source, td, mp, pages, msgids=7600)
    assert not findings


EXPECTED = """Norbert Schneider &#40;2012&#41; sieht die „Selbstentblößung“ in \
den Medien als Folge einer Individualisierung und als Ersatz für die verlorene \
Bestätigung aus einem Kollektiv, dem man angehörte, z.B."""


@utilatest.longrun
def test_master72_merge_token_correctly(td, mp):
    """Do not detect errors in perspective inside quotations."""
    source = power.MASTER072_PDF
    pages = '16'
    findings = decide_textflow(source, td, mp, pages, msgids=7600)
    assert len(findings) == 1
    description = findings[0].solution.description
    assert EXPECTED in description


@utilatest.longrun
def test_master72_text_too_long(td, mp):
    """Detect sentence which are too long."""
    source = power.MASTER072_PDF
    pages = '3:6'
    with mp.context() as context:
        context.setattr(
            decider_textflow.features.writing,
            'SENTENCE_LENGTH_MAX',
            100,
        )
        findings = decide_textflow(
            source,
            td,
            mp,
            pages=pages,
            msgids=7605,
        )
    assert len(findings) == 26


@utilatest.longrun
def test_writing_text_statistics(td, mp):
    source = power.MASTER110_PDF
    findings = decide_textflow(
        source,
        td,
        mp,
        msgids=7616,
    )
    assert len(findings) == 1


@utilatest.longrun
def test_writing_repeating_sentence_start(td, mp):
    source = power.MASTER110_PDF
    findings = decide_textflow(
        source,
        td,
        mp,
        msgids=7611,
    )
    assert findings
    # assert len(findings) in (0, 23, 24, 25)  # NOT VALIDATED


def test_sentence_start_repeat_inside_list_master063p24(td, mp):
    """Do not detect repeating sentence start inside list.

    banks, those risks are:
        - Risks to price stability
        - Risks to financial stability
        - Risks to payment system stability
    """
    source = power.MASTER063_PDF
    findings = decide_textflow(
        source,
        td,
        mp,
        pages=24,
        msgids=7611,
    )
    # 'risks to
    findings = [
        item for item in findings if 'risks to' in item.solution.description
    ]
    assert not findings


@utilatest.longrun
def test_writing_repeating_sentence_pattern(td, mp):
    source = power.MASTER110_PDF
    with mp.context() as context:
        context.setattr(
            decider_textflow.features.writing,
            'SENTENCE_PATTERN_WINDOW',
            3,
        )
        findings = decide_textflow(
            source,
            td,
            mp,
            msgids=7610,
        )
    assert findings
    # assert len(findings) in (7,8,9, 10, 11)  # NOT VALIDATED
