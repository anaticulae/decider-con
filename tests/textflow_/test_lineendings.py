# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import tests.textflow_
import textflow_.path


@utilotest.nightly
@utilotest.requires(hoverpower.MASTER083_PDF)
def test_lineendings_master83page6_lineending(td, mp):
    source = hoverpower.link(hoverpower.MASTER083_PDF)
    tests.textflow_.run_textflow(
        source,
        pages=6,
        lineending=True,
        quotation=True,
    )
    # lint result
    tests.textflow_.run(f'-i={source} --pages=6', mp=mp)
    result = serializeraw.load_findings(
        textflow_.path.lineendings_linted(td.tmpdir),
        7000,
    )
    assert len(result) == 2, str(result)


@utilotest.requires(hoverpower.BACHELOR067_PDF)
def test_list_not_included_bachelor67page10(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR067_PDF)
    # lint result
    cmd = f'-i={source} --pages=10 --lineending'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.findings_from_path(td.tmpdir, msgid=7005)
    assert len(result) == 1, str(result)


@utilotest.requires(hoverpower.MASTER072_PDF)
def test_list_not_included_master072page7(td, mp):
    """Regression test that start was detected not correctly.

    O’Reilly nennt in seinem Artikel sieben Hauptpunkte, die das Web 2.0
    kennzeichnen10:
    """
    source = hoverpower.link(hoverpower.MASTER072_PDF)
    # lint result
    cmd = f'-i={source} --pages=7 --lineending'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.findings_from_path(td.tmpdir, msgid=7005)
    assert not result


@utilotest.requires(hoverpower.BACHELOR067_PDF)
def test_list_better_included_bachelor67page10(td, mp):
    """No list is included via sentence end sign.

    If these error occurs, may the list is not parsed correctly. See
    words__sentences_sentences.yaml.
    """
    source = hoverpower.link(hoverpower.BACHELOR067_PDF)
    # lint result
    cmd = f'-i={source} --pages=10 --lineending'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.findings_from_path(td.tmpdir, msgid=7006)
    assert not result, str(result)


@pytest.mark.xfail(reason='formula produces no result')
@utilotest.requires(hoverpower.HOME050_PDF)
def test_formula_better_included_home050page31(td, mp):
    source = hoverpower.link(hoverpower.HOME050_PDF)
    cmd = f'-i={source} -o {td.tmpdir} --pages=31 --lineending'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.findings_from_path(td.tmpdir, msgid=7011)
    assert len(result) == 1, str(result)


@utilotest.requires(hoverpower.DISS157_PDF)
def test_formula_list_diss157page144_included(td, mp):
    """On page144 the list is included very well.

    This is a regression test, cause before there where false linting
    inside the list. The implementation before requires list inclusion
    inside a list what is very senceless.
    """
    source = hoverpower.link(hoverpower.DISS157_PDF)
    cmd = f'-i={source} -o {td.tmpdir} --pages=144 --lineending'
    tests.textflow_.run(cmd, mp=mp)
    result = serializeraw.findings_from_path(td.tmpdir, msgid={7005, 7706})
    assert not result
