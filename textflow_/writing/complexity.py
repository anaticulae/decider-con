# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

SENTENCE_COMPLEXITY_MAX = configos.HV_INT_PLUS(default=7)


def too_complex(line: str) -> bool:
    if ':' in line:
        return False
    subsentence = [item for item in line.split(',;') if len(item.split()) > 3]
    if len(subsentence) > SENTENCE_COMPLEXITY_MAX:
        return True
    return False
