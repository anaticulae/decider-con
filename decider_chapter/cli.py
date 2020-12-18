# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_chapter
import decider_chapter.path

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'intro',
        inputs=[
            utila.ResultFile('chapter', 'intro_intro'),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_chapter.ROOT,
        featurepackage='decider_chapter.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            pages=True,
            name=decider_chapter.PROCESS,
            version=decider_chapter.__version__,
        ),
    )
