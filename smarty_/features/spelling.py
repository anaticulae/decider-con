# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import germania
import protoerror

import smarty_.driver
import smarty_.utils


def work(hyphen: str, guess: str, pages: tuple = None) -> protoerror.ResultType:
    driver = smarty_.driver.create_spelling(
        hyphen,
        guess,
        pages=pages,
    )
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
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
        converted = [germania.token_plain(item) for item in error.docref.raw]
        rawword = '; '.join(converted)
        location = smarty_.utils.create_location(error)
        linter(
            rawword=rawword,
            location=location,
        )


SOLUTION_8205 = """\
Wortverbindung empfohlen

**{{rawword}}** überlegen Sie sich ob Bindestriche hier notwendig sind.

TODO: SIEHE DUDEN
"""


def check_8205_try_hyphen(linter: callable, driver):
    inside = smarty_.driver.create_tokeninside(driver.hyphen)
    for error in driver.guess:
        docref = error.docref
        dones = [
            any(
                inside.contains(docref.page, docref.sentence, token)
                for token in tokens)
            for tokens in docref.marked
        ]
        converted = [
            germania.token_plain(item)
            for item, skip in zip(error.docref.raw, dones)
            if not skip
        ]
        if not converted:
            # all words are already markes as hyphen error
            continue
        rawword = '; '.join(converted)
        location = smarty_.utils.create_location(error)
        linter(
            rawword=rawword,
            location=location,
        )
