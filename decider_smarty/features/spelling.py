# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import protocol

import decider_smarty.driver
import decider_smarty.features.badwords


def work(hyphen: str, guess: str, pages: tuple = None) -> protocol.ResultType:
    driver = create_driver(
        hyphen,
        guess,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


def create_driver(hyphen: str, guess: str, pages: tuple):
    hyphen = decider_smarty.driver.load_textadvice(hyphen, pages)
    if not hyphen:
        hyphen = []
    guess = decider_smarty.driver.load_textadvice(guess, pages)
    if not guess:
        guess = []
    result = protocol.driver(
        hyphen=hyphen,
        guess=guess,
    )
    return result


SOLUTION_8200 = """\
Wortverbindung uneindeutig

**{{rawword}}** unterscheidet sich in der Schreibweise von anderen im \
Dokument gefundenen, überprüfen Sie ob ein Bindestrich notwendig ist, \
oder korrigieren Sie die anderen Schreibweisen.
"""


def check_8200_hyphen_missing(linter: callable, driver):
    for error in driver.hyphen:
        converted = [german.token_plain(item) for item in error.docref.raw]
        rawword = '; '.join(converted)
        location = decider_smarty.features.badwords.create_location(error)
        linter(
            rawword=rawword,
            location=location,
        )
