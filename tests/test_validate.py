# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import protoerror
import pytest
import utilo
import utilotest

import decider_con
import tests.chapter_
import tests.conftest
import tests.smarty_
import tests.textflow_

ARCHIVE = utilo.join(decider_con.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize(
    'source',
    utilotest.test_resources(tests.conftest.RESOURCES),
)
@utilotest.nightly
def test_validate_huge(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


def run_extraction(cmd, mp):  # pylint:disable=W0613
    tests.chapter_.run(cmd, mp=mp)
    tests.smarty_.run(cmd, mp=mp)
    tests.textflow_.run(cmd, mp=mp)


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(
                run_extraction,
                mp=mp,
            ),
            step=None,
            pages=':',
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )

    def frompath(self, path):  # pylint:disable=R0201
        return protoerror.findings_from_path(path)

    def raw(self, value) -> str:
        findings = utilo.flatten_content(value)
        findings = [line(item) for item in findings]
        findings = sorted(findings, key=utilo.alphabetically)
        result = utilo.NEWLINE.join(findings)
        return result


def line(finding) -> str:
    result = str(finding.msgid).zfill(5) + ' '
    result += str(finding.location) + ' '
    result += finding.solution.title
    return result
