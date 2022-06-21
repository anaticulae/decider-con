# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila
import writers

import decider_con

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = decider_con.PROCESS
power.setup(decider_con.ROOT)

RESOURCES = [
    (power.BACHELOR037_PDF, '0:20'),
    (power.BACHELOR056_PDF, '0:20'),
    (power.BACHELOR067_PDF, '8:11,50:59'),
    (power.BACHELOR128_PDF, '0:20,50:70'),
    (power.BOOK007_PDF, '0:10'),
    (power.DISS144_PDF, '10:25'),
    (power.DISS157_PDF, '140:150'),
    (power.DOCU035_PDF, '0:10'),
    (power.HOME050_PDF, '30:40'),
    (power.MASTER063_PDF, '20:30'),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER075_PDF, '0:15'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    (power.MASTER099_PDF, '0:10'),
    (power.MASTER110_PDF, '0:70'),
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.TECH024_PDF, '0:15'),
    power.BACHELOR028_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR090_PDF,
    power.DOCU014_PDF,
    power.HOME018_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    # ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If resources provide only a
    # single file the parental determination is not possible. Therefore we
    # have to add the data root of all test files.
    utila.log(f'root: {power.REPOSITORY}')
    genex.extract(
        files=resources,
        destination=power.generated(),
        full=True,
        morefeatures=['chapter'],
        worker=WORKER,
        pages=':',
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
