# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_textflow


def lineendings_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'lineending_user',
        prefix,
    )


def startend_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'startend_user',
        prefix,
    )


def writing_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'writing_user',
        prefix,
    )


def paragraph_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'paragraph_user',
        prefix,
    )


def quotation_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'quotation_user',
        prefix,
    )


def character_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'character_user',
        prefix,
    )


def docref_linted(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_textflow.PROCESS,
        'docref_user',
        prefix,
    )
