# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import chapter_
import chapter_.path

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'intro',
        inputs=[
            utilo.ResultFile('chapter', 'intro_intro'),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    hook = protoerror.integrate(
        root=chapter_.ROOT,
        features='chapter_.features',
    )
    docinfo = protoerror.integrate_docinfo()
    utilo.featurepack(
        workplan=WORKPLAN,
        root=chapter_.ROOT,
        featurepackage='chapter_.features',
        config=utilo.FeaturePackConfig(
            cli_hook=[
                docinfo,
                hook,
            ],
            description=DESCRIPTION,
            multiprocessed=True,
            name=chapter_.PROCESS,
            pages=True,
            version=chapter_.__version__,
        ),
    )
