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

import smarty_

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'badwords',
        inputs=[
            utilo.ResultFile('smarty', 'avoid_avoid'),
            utilo.ResultFile('smarty', 'improvement_improvement'),
            utilo.ResultFile('smarty', 'phrases_phrases'),
            utilo.ResultFile('smarty', 'pleonasma_pleonasma'),
            utilo.ResultFile('smarty', 'reduce_reduce'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'spelling',
        inputs=[
            utilo.ResultFile('smarty', 'spelling_hyphen'),
            utilo.ResultFile('smarty', 'spelling_guess'),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    root, features = smarty_.ROOT, 'smarty_.features'
    hook = protoerror.integrate(root=root, features=features)
    utilo.featurepack(
        workplan=WORKPLAN,
        featurepackage=features,
        root=root,
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            name=smarty_.PROCESS,
            pages=True,
            version=smarty_.__version__,
        ),
    )
