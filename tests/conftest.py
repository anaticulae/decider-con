# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
    power.DOCU014_PDF,
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER075_PDF, '0:15'),
    (power.MASTER078_PDF, '0:10'),
]

WORKER = 6


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run([power.generated()])


def extract(resources):
    # ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If resources provide only a
    # single file the parental determination is not possible. Therefore we
    # have to add the data root of all test files.
    utila.log(f'root: {power.REPOSITORY}')
    resources.append(power.REPOSITORY)

    genex.extract(
        files=resources,
        destination=power.generated(),
        groupme=True,
        sections=True,
        words=True,
        magic=True,
        morefeatures=['chapter'],
        worker=WORKER,
        pages=':',
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
