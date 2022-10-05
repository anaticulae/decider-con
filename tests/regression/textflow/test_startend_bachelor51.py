# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textflow
import tests.textflow_


@utilatest.requires(power.BACHELOR051_PDF)
def test_empty_start_bachelor51page2128(td, mp, capsys):
    """The table on page 21 is on the bottom of the page. Page 28 starts
    with a list, which was also false detected cause of invalid magic
    content check.

    Before this table is a gap of text content. There was a bug, that
    text before was detected as justified text. And there was a second
    bug, that checking valid magic content was not worked correctly.

    After fixing magic content check, valid magic content is handled
    correctly.
    """
    source = power.link(power.BACHELOR051_PDF)
    cmd = f'-i {source}  --startend --pages=15:30'
    tests.textflow_.run(cmd, mp=mp)
    # ensure that startend is runned
    assert 'disable `startend`' not in utilatest.stderr(capsys)
    path = decider_textflow.path.startend_linted(td.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7625}, pages=(21, 28))
    assert not loaded
