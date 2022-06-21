# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import decider_textflow

run, fail = utilatest.create_cli_runner(decider_textflow)


def run_textflow(
    source,
    pages,
    lineending: bool = False,
    quotation: bool = False,
):
    actions = ''
    if lineending:
        actions += ' --lineending'
    if quotation:
        actions += ' --quotation'
    utila.run(f'textflow -i={source}  --pages={pages} {actions}')
