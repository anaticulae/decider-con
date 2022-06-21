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
import utilatest

import tests.textflow_


@utilatest.requires(power.BACHELOR128_PDF)
def test_writing_bachelor128page69(testdir, monkeypatch):
    """Regression that replaced quote was detected as finding.

    `**Wir** im Satz: **** sollte vermieden werden.`
    """
    source = power.link(power.BACHELOR128_PDF)
    cmd = f'-i {source} --writing --pages=69'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir, msgid=7600)
    assert not findings
