# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import protoerror
import pytest
import serializeraw
import utilo
import utilotest

import tests.textflow_
import textflow_.features.abbrev

TABLE = iamraw.AbbreviationResult(abbreviations=[
    iamraw.Abbreviation(
        short='SCB',
        description='Soli Chobi Bobi',
    ),
    iamraw.Abbreviation(
        short='WAL',
        description='Word Aliance Lord',
    ),
])

EXAMPLE = [
    iamraw.ExtractedTextAbbreviation(
        page=2,
        content=[
            iamraw.Abbreviation(
                short='SCB',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=1,
                ),
            ),
            iamraw.Abbreviation(
                short='WAL',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=2,
                ),
            ),
            iamraw.Abbreviation(
                short='WAL',
                description='Word Aliance Lord',
                position=iamraw.AbbreviationPosition(
                    page=2,
                    sentence=10,
                ),
            ),
        ]),
]


def test_linter_abbreviation_text_before_used():
    driver = protoerror.driver(
        abbr_table=TABLE,
        abbr_text=EXAMPLE,
    )
    user, _ = protoerror.run(
        modulename=textflow_.features.abbrev.__name__,
        driver=driver,
    )
    findings = serializeraw.load_findings(user, msgids=5100)
    assert len(findings) == 1


@pytest.mark.parametrize('source, pages', [
    pytest.param(hoverpower.BACHELOR037_PDF, '1', id='bachelor37'),
])
@utilotest.longrun
def test_cli_reftable_abbreviation_text(source, pages, td, mp):
    """Run decider"""
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    root = td.tmpdir
    cmd = f'reftable -i {source} -o {root} --abbrev --pages={pages}'
    completed = utilo.run(cmd)
    assert completed.returncode == utilo.SUCCESS, str(completed)
    cmd = f'-i {root} -i {source} -o {root} --abbrev'
    tests.textflow_.run(cmd, mp=mp)
