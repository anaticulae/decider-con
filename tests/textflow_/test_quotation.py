# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import tests.textflow_
import textflow_.path


def run_quotation_linter(source, pages, td, mp):
    utilotest.fixture_requires(source)
    pages = utilo.from_tuple(pages, separator=',')
    cmd = f'-i={source} --quotation --pages={pages}'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.load_findings(
        textflow_.path.quotation_linted(td.tmpdir))
    return result


@utilotest.longrun
def test_home18_quotation_start_with_ellipsis(td, mp):
    source = hoverpower.link(hoverpower.HOME018_PDF)
    result = run_quotation_linter(source, (7,), td, mp)
    assert not result
