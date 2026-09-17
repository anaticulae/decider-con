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

import smarty_
import tests.smarty_


def decide_smarty_badwords(source, pages, td, mp, msgid=None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.smarty_.run(
        f'--badwords -i {source} --pages={pages}',
        mp=mp,
    )
    path = smarty_.path.badwords(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgid)
    return findings


def test_smarty_badwords_bachelor128_non_formal_speach(td, mp):
    findings = decide_smarty_badwords(
        hoverpower.BACHELOR128_PDF,
        ':',
        td,
        mp,
        msgid=8100,
    )
    assert len(findings) >= 11


@pytest.mark.xfail(reason='broken test, overlapped by figures?')
def test_smarty_badwords_bachelor128_pleonasms(td, mp):
    findings = decide_smarty_badwords(
        hoverpower.BACHELOR128_PDF,
        ':',
        td,
        mp,
        msgid=8105,
    )
    assert len(findings) >= 2


def test_smarty_badwords_bachelor128_not_required_prefix(td, mp):
    findings = decide_smarty_badwords(
        hoverpower.BACHELOR128_PDF,
        ':',
        td,
        mp,
        msgid=8110,
    )
    assert len(findings) >= 1
