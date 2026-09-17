# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import utilo

HURENKIND_BEFORE = configos.HV_INT_PLUS(default=120)

HURENKIND_LINEWIDTH = configos.HV_PERCENT_PLUS(default=90)

SECOND_FULL_LINE_DIFF_MAX = configos.HV_FLOAT_PLUS(default=5.0)


def hurenkinds(text, linewidth: float):  # pylint:disable=R1260
    hurenkind_maxwidth = linewidth * HURENKIND_LINEWIDTH
    for page, content in text:
        if len(content) < 2:
            continue
        if content[0] is None or content[1] is None:
            continue
        first_headline = isinstance(content[0], iamraw.Headline)
        second_headline = isinstance(content[1], iamraw.Headline)
        if first_headline and second_headline:
            continue
        if not first_headline:
            if content[0].bounding.y0 > HURENKIND_BEFORE:
                # this page does not start with text line, there is may a
                # figure, table or something before.
                continue
        if second_headline and not first_headline:
            if content[1].decoration is not None:
                # CHAPTER-X-Pattern
                # Title
                continue
            # hurenkind
            # TEXT -> HEADLINE
            location = iamraw.RangedLocation(page=page, line=0)
            rawline = content[0].text.strip()
            yield rawline, location
            continue
        if not first_headline and not second_headline:
            # no headlines, text only
            first_width = width(content[0])
            second_width = width(content[1])
            second_full_line = utilo.near(
                second_width,
                linewidth,
                diff=SECOND_FULL_LINE_DIFF_MAX,
            )
            if first_width <= hurenkind_maxwidth and second_full_line:
                # hurenkind
                # SHORT TEXT -> TEXT
                location = iamraw.RangedLocation(page=page, line=0)
                rawline = content[0].text.strip()
                yield rawline, location


def width(item):
    bounding = item.bounding
    return utilo.roundme(bounding.x1 - bounding.x0)
