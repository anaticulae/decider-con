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

import chapter_
import tests.chapter_


def run_intro(source, td, mp, optional: str = ''):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    # run intro
    tests.chapter_.run(
        f'--intro -i={source} {optional}',
        mp=mp,
    )
    # load findings
    path = chapter_.path.chapter__intro(td.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.MASTER072_PDF, id='master72'),
])
def test_intro_x(source, td, mp):
    findings = run_intro(source, td, mp)
    assert not findings


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.MASTER075_PDF, id='master75'),
    pytest.param(hoverpower.MASTER078_PDF, id='master78'),
])
def test_intro_x_error(source, td, mp):
    findings = run_intro(source, td, mp)
    # TODO: ADD SEPARATE VALIDATE METHODS
    assert findings


def test_intro_disable_small_document(td, mp):
    """Do not use this AI-Linter on small documents."""
    source = hoverpower.DOCU014_PDF
    findings = run_intro(source, td, mp, optional='--docinfo=14')
    assert not findings
