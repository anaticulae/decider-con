#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

PACKAGES = [
    'chapter_',
    'chapter_.features',
    'decider_con',
    'smarty_',
    'smarty_.features',
    'textflow_',
    'textflow_.docref',
    'textflow_.features',
    'textflow_.startend',
    'textflow_.writing',
]
ENTRY_POINTS = dict(console_scripts=[
    'chapter_ = chapter_.cli:main',
    'smarty_ = smarty_.cli:main',
    'textflow_ = textflow_.cli:main',
])
if __name__ == "__main__":
    utilo.install(__file__)
