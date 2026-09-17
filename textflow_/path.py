# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import textflow_


def lineendings_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'lineending_user',
        prefix,
    )


def startend_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'startend_user',
        prefix,
    )


def writing_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'writing_user',
        prefix,
    )


def paragraph_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'paragraph_user',
        prefix,
    )


def quotation_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'quotation_user',
        prefix,
    )


def character_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'character_user',
        prefix,
    )


def docref_linted(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(
        path,
        textflow_.PROCESS,
        'docref_user',
        prefix,
    )
