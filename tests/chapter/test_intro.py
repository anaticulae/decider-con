# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import decider_chapter
import tests.chapter


def test_intro_master72(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    tests.chapter.run(f'--intro -i={source}', monkeypatch=monkeypatch)

    path = decider_chapter.path.decider_chapter_intro(testdir.tmpdir)
    findings = serializeraw.load_findings(path)
    assert not findings
