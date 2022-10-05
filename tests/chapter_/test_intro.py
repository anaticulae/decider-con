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

import decider_chapter
import tests.chapter_


def run_intro(source, td, mp, optional: str = ''):
    utilatest.fixture_requires(source)
    source = power.link(source)
    # run intro
    tests.chapter_.run(
        f'--intro -i={source} {optional}',
        mp=mp,
    )
    # load findings
    path = decider_chapter.path.decider_chapter_intro(td.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.parametrize('source', [
    pytest.param(power.MASTER072_PDF, id='master72'),
])
def test_intro_x(source, td, mp):
    findings = run_intro(source, td, mp)
    assert not findings


@pytest.mark.parametrize('source', [
    pytest.param(power.MASTER075_PDF, id='master75'),
    pytest.param(power.MASTER078_PDF, id='master78'),
])
def test_intro_x_error(source, td, mp):
    findings = run_intro(source, td, mp)
    # TODO: ADD SEPARATE VALIDATE METHODS
    assert findings


def test_intro_disable_small_document(td, mp):
    """Do not use this AI-Linter on small documents."""
    source = power.DOCU014_PDF
    findings = run_intro(source, td, mp, optional='--docinfo=14')
    assert not findings
