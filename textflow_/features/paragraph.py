# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import protoerror
import serializeraw
import utilo

import textflow_.features

TEXTUAL = {
    iamraw.PageContentType.TEXT,
    iamraw.PageContentType.BLOCKQUOTE,
}


def work(
    headlines: str,
    text: str,
    textpositions: str,
    sizeandborders: str,
    headerfooter: str,
    textstyle: str,
    magiccontent: str,
    pages: tuple = None,
) -> tuple[str, str]:
    textstyle = serializeraw.load_doctextstyle(textstyle)
    driver = textflow_.features.create_driver(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        textstyle=textstyle,
        magicvalid=TEXTUAL,
        pages=pages,
    )
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_7630 = """\
Paragraph zu kurz

Der Abschnitt umfasst nur {{lines}} Zeilen und sollte überarbeitet werden.

{aufbau_gliederung/absatz}
"""

PARAGRAPH_TOO_SHORT = configos.HV_INT_PLUS(default=3)

TEXT_WIDTH_MIN = configos.HV_INT_PLUS(default=35)


def check_7630_paragraph_too_short(linter: callable, driver):
    textstyle = driver.doctextstyle

    if textstyle.text_alignment == 0:  # pylint:disable=C2001
        # not justified
        return
    if textstyle.text_width is None:
        utilo.debug('no textstyle.text_width, disable 7630')
        return
    min_textwidth = textstyle.text_width - TEXT_WIDTH_MIN
    collected = []
    for page, line, item in driver.nomagic_text_chunks:
        # TODO: USE VISITOR PATTERN
        if isinstance(item, iamraw.PageList):
            # TODO: THINK ABOUT WHAT WE CAN CHECK
            # no check before list starts.
            collected = []
            continue
        if isinstance(item, iamraw.Headline):
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = ranged_location(collected)
                linter(location=location, lines=len(collected))
            collected = []
            continue
        if item is None:
            collected = []
            continue
        line_width = width(item)
        if line_width <= min_textwidth:
            collected.append((page, line, item))
            too_short = 2 <= len(collected) <= PARAGRAPH_TOO_SHORT
            if too_short:
                location = ranged_location(collected)
                linter(location=location, lines=len(collected))
            collected = []
        else:
            collected.append((page, line, item))


def ranged_location(collected) -> iamraw.RangedLocation:
    location = iamraw.RangedLocation(
        page=collected[0][0],
        page_end=collected[-1][0],
        line=collected[0][1],
        line_end=collected[-1][1],
    )
    return location


def width(item):
    bounding = item.bounding
    return utilo.roundme(bounding.x1 - bounding.x0)
