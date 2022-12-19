#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'decider_chapter',
    'decider_chapter.features',
    'decider_con',
    'decider_smarty',
    'decider_smarty.features',
    'decider_textflow',
    'decider_textflow.docref',
    'decider_textflow.features',
    'decider_textflow.startend',
    'decider_textflow.writing',
]
ENTRY_POINTS = dict(console_scripts=[
    'decider_chapter = decider_chapter.cli:main',
    'decider_smarty = decider_smarty.cli:main',
    'decider_textflow = decider_textflow.cli:main',
])
if __name__ == "__main__":
    utila.install(__file__)
