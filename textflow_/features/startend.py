# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Hurenkind: Single Line at Page Start
Schusterjunge: Single Line at Page End
"""

import statistics

import configos
import iamraw
import protoerror
import utilo

import textflow_.features
import textflow_.startend.hurenkind
import textflow_.utils


def work(
    headlines: str,
    text: str,
    textpositions: str,
    sizeandborders: str,
    headerfooter: str,
    magiccontent: str,
    pages: tuple = None,
) -> tuple[str, str]:
    driver = textflow_.features.create_driver(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        pages=pages,
    )
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_7620 = """\
Einsame Zeile am Seitenanfang

Seite beginnt mit einsamer Zeile:

**{{rawline}}**.

{darstellung/schriftbild#hurenkind}
"""

HURENKIND_HEADLINES_CONFIDENCE_MIN = configos.HV_PERCENT_PLUS(default=80)


def check_7620_lonely_page_start(linter: callable, driver):  # pylint:disable=R1260
    """\
    This check requires a high headline confidence to avoid a lot of
    false postive headlines detected as `Hurenkind`.

    TODO: USE SENTENCE END SIGN TO REDUCE FALSE POSITIVE RATE.
    """
    if driver.headlines_confidence is None:
        protoerror.skip_method('headline confidence is None')
        return
    if driver.headlines_confidence < HURENKIND_HEADLINES_CONFIDENCE_MIN:
        protoerror.skip_method('headlines confidence too '
                               f'low: {driver.headlines_confidence}')
        return
    linewidth = textwidth(driver.text_chunks)
    if linewidth is None:
        protoerror.skip_method('empty linewidth')
        return
    text = textflow_.utils.page_chunks(driver.nomagic_text_chunks)
    for hurenkind in textflow_.startend.hurenkind.hurenkinds(
            text,
            linewidth,
    ):
        rawline, location = hurenkind
        linter(
            rawline=rawline,
            location=location,
        )


SOLUTION_7621 = """\
Schusterjunge: Einsame Zeile am Seitenende

{darstellung/schriftbild#schusterjunge}
"""

SOLUTION_7625 = """\
Seitenanfang: Seite beginnt nicht mit Text

Die Grafik/Tabelle etc. sollte in den Text eingebunden werden und nicht \
direkt am Seitenanfang stehen.

{darstellung/schriftbild#seitenanfang}
"""

# TODO: ADD SUPPORT FOR TEXT ABOVE IMAGES/TABLE etc.

FAILSTART_MAX = configos.HV_INT_PLUS(default=100)

FAILSTART_HEADLINE_MAX = configos.HV_INT_PLUS(default=150)


def check_7625_empty_start(linter: callable, driver):
    text = textflow_.utils.page_chunks(driver.nomagic_text_chunks)
    startend = page_startend(text)
    if startend is None:
        protoerror.skip_method('could not detect start/end')
        return
    start, _ = startend
    for page, content in text:
        navigator = utilo.select_page(driver.navigators, page=page)
        if navigator is None:
            # may a headline error
            utilo.error(f'missing navigator: {page}')
            continue
        if valid_pagestart(
                content,
                start=start,
                navigator=navigator,
        ):
            continue
        location = iamraw.Location.from_sentence(
            sentence=0,
            page=page,
        )
        linter(location=location)


def valid_pagestart(content, start: float, navigator) -> bool:
    if page_empty(content):
        return True
    first = content[0]
    if isinstance(first, iamraw.Headline):
        startindex = first.container
        if isinstance(startindex, tuple):
            startindex = startindex[0]
        # TODO: REMOVE AFTER IMPROVING HEADLINE DATA STRUCTURE
        first = navigator[startindex]
        failstart = start + FAILSTART_HEADLINE_MAX
        if first.bounding.y0 <= failstart:
            return True
        return False
    if not content[0]:
        # page starts with math, table etc.
        return False
    # TODO: HANDLE SINGLE ITEM ON PAGE
    # page starts with content, table, caption etc. will yield none
    failstart = start + FAILSTART_MAX
    if first.bounding.y0 <= failstart:
        return True
    return False


def page_empty(content) -> bool:
    if all(item is None for item in content):
        # not all content is replaced with magic data, therefore None
        return True
    return False


SOLUTION_7626 = """\
Seitenende: Seite endet nicht mit Text

"""

# def check_7626_empty_end(linter: callable, driver):
#     # TODO: DO WE REQUIRE THIS TEST OR IS IT SOLVED VIA 7625?
#     pass


def textwidth(chunks) -> float:
    result = []
    for _, __, item in chunks:
        if item is None:
            continue
        if isinstance(item, iamraw.Headline):
            continue
        result.append(width(item))
    if not result:
        utilo.debug('could not determine textwidth, no text chunks collected')
        return None
    result = utilo.mode(result)
    return result


STARTEND_PAGES_MIN = configos.HV_INT_PLUS(default=5)


def page_startend(items):  # pylint:disable=R1260
    if len(items) < STARTEND_PAGES_MIN:
        utilo.error(f'disable `startend`: too few pages {len(items)}')
        return None
    start, end = [], []
    for _, content in items:
        if not content:
            continue
        first = content[0]
        if first is None:
            continue
        if not isinstance(first, iamraw.Headline):
            # TODO: ADD HEADLINE SUPPORT
            first = first.bounding.y0
            start.append(first)
        if len(content) == 1:
            continue
        last = content[-1]
        if last is None:
            continue
        if not isinstance(last, iamraw.Headline):
            # TODO: ADD HEADLINE SUPPORT
            last = last.bounding.y1
            end.append(last)
    try:
        start = utilo.mode(start)
        end = utilo.mode(end)
    except statistics.StatisticsError:
        utilo.error(f'disable `startend`: empty data {start} {end}')
        return None
    return start, end


def width(item):
    bounding = item.bounding
    return utilo.roundme(bounding.x1 - bounding.x0)
