# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila


def create(
    avoid: str = None,
    improvement: str = None,
    phrases: str = None,
    pleonasma: str = None,
    reduce: str = None,
    pages: tuple = None,
):
    # prepare findings
    avoid = load_textadvice(avoid, pages=pages)
    improvement = load_textadvice(improvement, pages=pages)
    phrases = load_textadvice(phrases, pages=pages)
    pleonasma = load_textadvice(pleonasma, pages=pages)
    reduce = load_textadvice(reduce, pages=pages)
    # driver
    driver = protocol.driver(
        avoid=avoid,
        improvement=improvement,
        phrases=phrases,
        pleonasma=pleonasma,
        reduce=reduce,
    )
    return driver


def load_textadvice(path: str, pages: tuple = None):
    if not utila.exists(path):
        return None
    result = serializeraw.load_textadvices(path, pages=pages)
    return result


def create_spelling(hyphen: str, guess: str, pages: tuple):
    hyphen = load_textadvice(hyphen, pages)
    if not hyphen:
        hyphen = []
    guess = load_textadvice(guess, pages)
    if not guess:
        guess = []
    result = protocol.driver(
        hyphen=hyphen,
        guess=guess,
    )
    return result
