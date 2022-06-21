# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_smarty


def badwords(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_smarty.PROCESS,
        'badwords_user',
        prefix,
    )
