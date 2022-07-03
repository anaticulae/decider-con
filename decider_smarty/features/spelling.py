# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_smarty.driver
import decider_smarty.features.badwords


def work(hyphen: str, pages: tuple = None) -> protocol.ResultType:
    driver = create_driver(
        hyphen,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


def create_driver(hyphen, pages: tuple):
    hyphen = decider_smarty.driver.load_textadvice(hyphen, pages)
    if not hyphen:
        hyphen = []
    return protocol.driver(hyphen=hyphen)


SOLUTION_8200 = """\
Wortverbindung uneindeutig

**{{rawword}}** unterscheidet sich in der Schreibweise von anderen im \
Dokument gefundenen, überprüfen Sie ob ein Bindestrich notwendig ist, \
oder korrigieren Sie die anderen Schreibweisen.
"""


def check_8200_hyphen_missing(linter: callable, driver):
    for error in driver.hyphen:
        rawword = '; '.join(' '.join(item) for item in error.docref.raw)
        location = decider_smarty.features.badwords.create_location(error)
        linter(
            rawword=rawword,
            location=location,
        )
