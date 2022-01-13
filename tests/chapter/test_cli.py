# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utila

import decider_chapter
import tests.chapter


def test_decider_content_cli_help(monkeypatch):
    tests.chapter.run('--help', monkeypatch=monkeypatch)


def test_decider_content_nomonkey_cli_help():
    utila.run(f'{decider_chapter.PROCESS} --help')


def test_language_decorator(testdir, monkeypatch):
    """Disable 6500 for other language than german."""
    source = power.link(power.MASTER075_PDF)
    german = testdir.tmpdir.join('german')
    tests.chapter.run(f'-i {source} -o {german}', monkeypatch=monkeypatch)
    germans = protocol.findings_from_path(german, msgid=6500)
    assert germans
    # skip check for english lang
    english = testdir.tmpdir.join('english')
    cmd = f'-i {source} -o {english} --docinfo=english'
    tests.chapter.run(cmd, monkeypatch=monkeypatch)
    englishs = protocol.findings_from_path(english, msgid=6500)
    assert not englishs, 'is english supported now?'
