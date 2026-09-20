# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import utilo
import utilotest

import chapter_
import tests.chapter_


def test_decider_content_cli_help(mp):
    tests.chapter_.run('--help', mp=mp)


@utilotest.hasprog(chapter_.PROCESS)
def test_decider_content_nomonkey_cli_help():
    utilo.run(f'{chapter_.PROCESS} --help')


@utilotest.requires(hoverpower.MASTER075_PDF)
def test_language_decorator(td, mp):
    """Disable 6500 for other language thangermania."""
    source = hoverpower.link(hoverpower.MASTER075_PDF)
    german = td.tmpdir.join('german')
    tests.chapter_.run(f'-i {source} -o {german}', mp=mp)
    germans = protoerror.findings_from_path(german, msgid=6500)
    assert germans
    # skip check for english lang
    english = td.tmpdir.join('english')
    cmd = f'-i {source} -o {english} --docinfo=english'
    tests.chapter_.run(cmd, mp=mp)
    englishs = protoerror.findings_from_path(english, msgid=6500)
    assert not englishs, 'is english supported now?'
