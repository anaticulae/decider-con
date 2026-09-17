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


def decide_textflow(source, pages, td, mp, msgids=None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'--docref -i {source} --pages={pages}',
        mp=mp,
    )
    path = textflow_.path.docref_linted(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@pytest.mark.xfail(reason='???')
def test_bachelor76_docref_negative(td, mp):
    """This document contains only valid references.

    Therefore we do not detect any missing references.
    """
    source = hoverpower.BACHELOR076_PDF
    pages = '0:30'
    findings = decide_textflow(
        source,
        pages,
        td,
        mp,
        msgids={7200, 7202},
    )
    assert not findings


def test_bachelor76_figure_missing_intext_ref(td, mp):
    """Remove this test after extending docref intext parser.

    Pattern: 'Die folgende Abbildung soll durch' not supported yet.
    """
    source = hoverpower.BACHELOR076_PDF
    pages = '0:30'
    findings = decide_textflow(
        source,
        pages,
        td,
        mp,
        msgids={7201},
    )
    # assert not findings # TODO: ENABLE LATER
    # TODO: REMOVE LATER, # TABLE IS PRINTED INSIDE AN IMAGE
    assert len(findings) == 2


def test_master75_docref(td, mp):
    # TODO: DESCRIBE PURPOSE OF TEST
    source = hoverpower.MASTER075_PDF
    findings = decide_textflow(
        source,
        ':',
        td,
        mp,
        msgids={7200, 7202},
    )
    assert findings  # may changes later


def test_bachelor56page15_tableref(td, mp):
    """Verify that `s. Tab. 1` matches with `Tabelle 1`"""
    source = hoverpower.BACHELOR056_PDF
    pages = '15'
    findings = decide_textflow(
        source,
        pages,
        td,
        mp,
        msgids={7202},
    )
    assert not findings
