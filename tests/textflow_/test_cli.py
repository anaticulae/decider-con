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
import utilotest

import tests.textflow_


def test_cli_help(mp):
    tests.textflow_.run('--help', mp=mp)


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.TECH024_PDF, id='technical24'),
    pytest.param(hoverpower.BACHELOR037_PDF, id='bachelor37'),
    pytest.param(hoverpower.BACHELOR076_PDF, id='bachelor76'),
    pytest.param(hoverpower.DOCU035_PDF, id='docu35'),
    pytest.param(hoverpower.BOOK007_PDF, id='book7'),
    pytest.param(hoverpower.MASTER072_PDF, id='master72'),
    pytest.param(hoverpower.MASTER078_PDF, id='master78'),
    pytest.param(hoverpower.MASTER098_PDF, id='master98'),
    pytest.param(hoverpower.MASTER099_PDF, id='master99'),
])
@utilotest.nightly
def test_cli_textflow_example(source, td, mp):  # pylint:disable=W0613
    """Run textflow."""
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textflow_.run(
        f'-i {source}',
        mp=mp,
    )
