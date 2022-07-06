# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_smarty

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'badwords',
        inputs=[
            utila.ResultFile('smarty', 'avoid_avoid'),
            utila.ResultFile('smarty', 'improvement_improvement'),
            utila.ResultFile('smarty', 'phrases_phrases'),
            utila.ResultFile('smarty', 'pleonasma_pleonasma'),
            utila.ResultFile('smarty', 'reduce_reduce'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'spelling',
        inputs=[
            utila.ResultFile('smarty', 'spelling_hyphen'),
            utila.ResultFile('smarty', 'spelling_guess'),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    root, features = decider_smarty.ROOT, 'decider_smarty.features'
    hook = protocol.integrate(root=root, features=features)
    utila.featurepack(
        workplan=WORKPLAN,
        featurepackage=features,
        root=root,
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            name=decider_smarty.PROCESS,
            pages=True,
            version=decider_smarty.__version__,
        ),
    )
