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

import decider_textflow
import tests.textflow_


@pytest.mark.xfail(reason='???')
@utilatest.longrun
@utilatest.requires(power.MASTER116_PDF)
def test_paragraph_too_short_in_table_master116_page79(td, mp):
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source}  --paragraph --pages=79'
    tests.textflow_.run(cmd, mp=mp)
    path = decider_textflow.path.paragraph_linted(td.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7630})
    expected = [
        (10, 11),
        # (13, 15), # TODO: ENABLE AFTER FIXING HEADLINES
        (26, 28),
    ]
    current = [
        (finding.location.line, finding.location.line_end) for finding in loaded
    ]
    assert current == expected
