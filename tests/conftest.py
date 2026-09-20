# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
import writers
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import decider_con

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = decider_con.PROCESS
hoverpower.setup(decider_con.ROOT)

RESOURCES = [
    (hoverpower.BACHELOR037_PDF, '0:20'),
    (hoverpower.BACHELOR051_PDF, '0:30'),
    (hoverpower.BACHELOR056_PDF, '0:20'),
    (hoverpower.BACHELOR067_PDF, '8:11,50:59'),
    (hoverpower.BACHELOR128_PDF, '0:20,50:70'),
    (hoverpower.BOOK007_PDF, '0:10'),
    (hoverpower.DISS157_PDF, '140:150'),
    (hoverpower.DOCU035_PDF, '0:10'),
    (hoverpower.HOME050_PDF, '30:40'),
    (hoverpower.MASTER063_PDF, '20:30'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER083_PDF, '0:10'),
    (hoverpower.MASTER098_PDF, '0:10,43:65,88:97'),
    (hoverpower.MASTER099_PDF, '0:10'),
    (hoverpower.MASTER110_PDF, '0:70'),
    (hoverpower.MASTER116_PDF, '0:50,75:115'),
    (hoverpower.TECH024_PDF, '0:15'),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.DISS144_PDF,
    hoverpower.DOCU014_PDF,
    hoverpower.HOME018_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
]

WORKER = utilotest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        full=True,
        morefeatures=['chapter'],
        worker=WORKER,
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
