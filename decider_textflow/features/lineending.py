# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import serializeraw
import texmex
import textflow.features.lineending
import utila

import decider_textflow.features


def work(
    lineendings: str,
    sentences: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(
        lineendings=lineendings,
        sentences=sentences,
        pages=pages,
    )
    result = protocol.run(
        __name__,
        driver=driver,
    )
    return result


SOLUTION_7000 = """\
Zu viele aufeinander folgende Trennungen

Es wird empfohlen die Anzahl der aufeinander folgenden Zeilen die eine \
Trennung enthalten auf 3 zu beschränken.

{darstellung/schriftbild#trennungen}
"""

FOLLOWING_DIVISION_MAX = configo.HV_INT_PLUS(default=3)


def check_7000_more_than_three_division(linter: callable, driver):
    """Ensure that there are not more than three following line
    divisions(-)."""

    def more_than_three(items):
        if not items:
            return []
        collected = [[items[0]]]
        for item in items[1:]:
            if collected[-1][-1][0] == '-' and item[0] == '-':
                collected[-1].append(item)
            else:
                collected.append([item])
        result = [
            item for item in collected if len(item) > FOLLOWING_DIVISION_MAX
        ]
        return result

    def merge_bounding(items):
        """Create bounding box around the list of division `-`. Limit
        the box to the left side, cause boundingbox is used from whole
        line but we want to highlight the last character."""
        boundings = [item[1] for item in items]
        x0, y0, x1, y1 = boundings[0]
        x0 = x1 - 20  # limit bounding box to 20 width
        for x00, y00, x11, y11 in boundings[1:]:
            # center box
            x00 = x11 - 20
            x11 = x11 + 20
            x0 = min([x0, x00])
            x1 = max([x1, x11])
            y0 = min([y0, y00])
            y1 = max([y1, y11])
        return (x0, y0, x1, y1)

    for page in driver.lineendings:
        number = page.page
        failures = more_than_three(page.content)
        for failure in failures:
            bounding = merge_bounding(failure)
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=number,
            )
            linter(location=location)


SOLUTION_7005 = """\
Satzende vor Aufzählung fehlt

Der Übergang von Text zu Aufzählung sollte durch einen **:** verbunden \
werden. **{{text}}:**

Passen Sie gegebenenfalls den Text an.
"""


def check_7005_list_not_included(linter: callable, driver):

    def valid_inclusion(raw):
        if raw[-1] in ':.?;':
            # list is included due sentence ending before
            return True
        if texmex.is_listitem(raw):
            # do not check this inside a list
            return True
        return False

    for current in sandwich(
            driver.sentences,
            ending_valid=valid_inclusion,
            selector=texmex.is_listsepa,
    ):
        location = iamraw.Location.from_sentence(
            sentence=current[2],
            page=current[1],
        )
        linter(
            text=current[0],
            location=location,
        )


SOLUTION_7006 = """\
Satzende vor Aufzählung anpassen

Ein Doppelpunkt bindet die Liste besser ein. Ersetzen Sie **{{sign}}** \
durch einen Doppelpunkt und passen Sie gegebenfalls den Text \
**{{text}}** an.

TODO
"""


def check_7006_list_better_included(linter: callable, driver):

    def valid_inclusion(raw):
        if raw[-1] not in '.?;':
            # list is included due sentence ending before
            return True
        if texmex.is_listitem(raw):
            # do not check this inside a list
            return True
        return False

    for current in sandwich(
            driver.sentences,
            ending_valid=valid_inclusion,
            selector=texmex.is_listsepa,
    ):
        raw = current[0]
        location = iamraw.Location.from_sentence(
            sentence=current[2],
            page=current[1],
        )
        linter(
            text=raw,
            sign=raw[-1],
            location=location,
        )


SOLUTION_7010 = """\
Satzende vor Gleichung fehlt

Der Übergang von Text zur Gleichung sollte durch einen **:** verbunden. \
Passen Sie gegebenenfalls den Text an. **{{text}}:**
"""


def check_7010_formula_not_included(linter: callable, driver):
    # TODO: INCLUDE FORMULA, <NEWLINE> FORMULA, <NEWLINE>, ....
    sentences = driver.sentences
    for current in sandwich(
            sentences,
            ending_valid=lambda raw: raw[-1] in ':.?;',
            selector=texmex.is_formula,
    ):
        location = iamraw.Location.from_sentence(
            sentence=current[2],
            page=current[1],
        )
        linter(
            text=current[0],
            location=location,
        )


SOLUTION_7011 = """\
Satzende vor Gleichung anpassen

Ein Doppelpunkt bindet die Gleichung besser ein. Ersetzen Sie **{{sign}}** \
durch einen Doppelpunkt und passen Sie gegebenfalls den Text \
**{{text}}** an.
"""


def check_7011_formula_better_included(linter: callable, driver):
    # TODO: INCLUDE FORMULA, <NEWLINE> FORMULA, <NEWLINE>, ....
    sentences = driver.sentences
    for current in sandwich(
            sentences,
            ending_valid=lambda raw: raw[-1] not in '.?;',
            selector=texmex.is_formula,
    ):
        raw = current[0]
        location = iamraw.Location.from_sentence(
            sentence=current[2],
            page=current[1],
        )
        linter(
            text=raw,
            sign=raw[-1],
            location=location,
        )


def sandwich(sentences, ending_valid: callable, selector: callable):
    for current, after in zip(sentences[0:-1], sentences[1:]):
        if isinstance(current, iamraw.Headline):
            continue
        if isinstance(after, iamraw.Headline):
            continue
        if selector(current[0]):
            continue
        if not selector(after[0]):
            continue
        if ending_valid(current[0]):
            continue
        yield current


def create_driver(lineendings, sentences, pages: tuple = None):
    if utila.exists(lineendings):
        # TODO: REMOVE PYLINT LATER
        lineendings = textflow.features.lineending.load_lineendings(  # pylint:disable=E1123
            lineendings,
            pages=pages,
        )
    else:
        lineendings = []
    sentences = serializeraw.load_text(
        sentences,
        pages=pages,
    )
    sentences = decider_textflow.features.Sentences(sentences)  # pylint:disable=R0204
    result = protocol.driver(
        lineendings=lineendings,
        sentences=sentences,
    )
    return result
