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
import pytest
import utilotest

import tests.textflow_


@pytest.mark.xfail(reason='???')
@utilotest.requires(hoverpower.BACHELOR128_PDF)
def test_writing_bachelor128page69(td, mp):
    """Regression that replaced quote was detected as finding.

    `**Wir** im Satz: **** sollte vermieden werden.`
    """
    source = hoverpower.link(hoverpower.BACHELOR128_PDF)
    cmd = f'-i {source} --writing --pages=69'
    tests.textflow_.run(cmd, mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir, msgid=7600)
    assert not findings
