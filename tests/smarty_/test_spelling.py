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


def decide_smarty_spelling(source, pages, td, mp, msgid=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.smarty_.run(
        f'--spelling -i {source} --pages={pages}',
        mp=mp,
    )
    path = decider_smarty.path.spelling(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgid)
    return findings


@utilatest.longrun
def test_smarty_spelling_hyphen(td, mp):
    findings = decide_smarty_spelling(
        power.BACHELOR077_PDF,
        ':',
        td,
        mp,
        msgid=8200,
    )
    assert len(findings) >= 5
