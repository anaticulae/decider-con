# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import protocol
import pytest
import utila
import utilatest

import decider_con
import tests.chapter_
import tests.smarty_
import tests.textflow_

ARCHIVE = utila.join(decider_con.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source', [
    pytest.param(power.BACHELOR063_PDF, id='bachelor063'),
    pytest.param(power.BACHELOR076_PDF, id='bachelor076'),
    pytest.param(power.BACHELOR090_PDF, id='bachelor090'),
    pytest.param(power.MASTER072_PDF, id='master072'),
    pytest.param(power.MASTER075_PDF, id='master075'),
])
@utilatest.nightly
def test_validate_huge(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


def run_extraction(cmd, monkeypatch):  # pylint:disable=W0613
    tests.chapter_.run(cmd, monkeypatch=monkeypatch)
    tests.smarty_.run(cmd, monkeypatch=monkeypatch)
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                run_extraction,
                monkeypatch=monkeypatch,
            ),
            step=None,
            pages=':',
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        return protocol.findings_from_path(path)

    def raw(self, value) -> str:
        findings = utila.flatten_content(value)
        findings = [line(item) for item in findings]
        findings = sorted(findings, key=utila.alphabetically)
        result = utila.NEWLINE.join(findings)
        return result


def line(finding) -> str:
    result = str(finding.msgid).zfill(5) + ' '
    try:
        result += finding.location.raw().zfill(5)
    except AttributeError:
        result += str(finding.location).zfill(5)
    result += ' ' + finding.solution.title
    return result
