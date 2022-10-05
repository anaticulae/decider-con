# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import power
import protocol
import serializeraw
import utilatest

import decider_textflow.features.startend
import decider_textflow.path
import tests
import tests.textflow_


@contextlib.contextmanager
def startend(source, pages, findingid, mp):
    utilatest.fixture_requires(source)
    source = power.link(source)
    cmd = f'-i={source} --startend --pages={pages}'
    tests.textflow_.run(cmd, mp=mp)
    cwd = os.getcwd()
    result = serializeraw.load_findings(
        decider_textflow.path.startend_linted(cwd),
        findingid,
    )
    yield result


def test_startend_hurenkind_bachelor90_page16(td, mp):  # pylint:disable=W0613
    """After oneline a headline follow which marks a `Hurenkind`.

    Load one page before and one page after to load required headlines.
    """
    with startend(power.BACHELOR090_PDF, '15:17', 7620, mp) as result:
        assert len(result) == 1, str(result)


def test_startend_hurenkind_bachelor90_page18(td, mp):  # pylint:disable=W0613
    """After a short line a full line follow, which marks a `Hurenkind`.

    Load one page before and one page after to load required
    headlines.
    """
    with startend(power.BACHELOR090_PDF, '17:19', 7620, mp) as result:
        assert len(result) == 1, str(result)


@utilatest.longrun
def test_startend_figure_start_bachelor90p40p55(td, mp):  # pylint:disable=W0613
    with startend(power.BACHELOR090_PDF, '40:55', 7625, mp) as result:
        pages = sorted([finding.location.page for finding in result])
    assert pages == [41, 47, 50]


def test_startend_figure_start_bachelor90p34(td, mp):  # pylint:disable=W0613
    """Ensure to detect page starts with an image instead of text."""
    with startend(power.BACHELOR090_PDF, '34:40', 7625, mp) as result:
        assert len(result) == 1, str(result)
    assert len(protocol.select_pages(result, 34)) == 1


def test_startswith_figureonly_page(td, mp):  # pylint:disable=W0613
    """Do not figure only page as a page with wrong page start.

    Before the patch, the caption-magic was detected as linted line.
    """
    with mp.context() as context:
        # disable this check
        context.setattr(decider_textflow.features.startend,
                        'STARTEND_PAGES_MIN', 0)
        with startend(power.DISS144_PDF, '16:20', 7625, mp) as result:
            page18 = protocol.select_pages(result, 18)
    assert not page18


def test_startend_hurenkind_bachelor128p7(td, mp):  # pylint:disable=W0613
    with startend(power.BACHELOR128_PDF, '7', 7620, mp) as result:
        assert not result


def test_startend_hurenkind_chapter_x_pattern(td, mp):  # pylint:disable=W0613
    with startend(power.MASTER110_PDF, '18', 7620, mp) as result:
        assert not result
