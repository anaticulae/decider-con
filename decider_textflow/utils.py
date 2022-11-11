# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import operator

import iamraw
import texmex
import texmex.style
import utila


def text_chunks(  # pylint:disable=R0912,R0914,R1260,W0613
    headlines,
    navigators,
    magiccontent: list = None,
    sync: bool = False,
    yieldnone: bool = False,
    magicvalid=None,
) -> list:
    """\
    yieldnone yield none-TextInfo-elements with None
    """
    if not magicvalid:
        magicvalid = [iamraw.PageContentType.TEXT]
    magiccontent = magiccontent if magiccontent else []
    # TODO: SO BAD
    headlines = utila.flat(headlines)
    visited = utila.Single()
    flat = []
    for headline in headlines:
        # mark contaienr id as visited
        for container in containers(headline.container):
            visited.contains((headline.page, container))
        position = (
            headline.page,
            container_start(headline.container),
        )
        flat.append((*position, headline))
    for magicpage in magiccontent:
        for line, content in magicpage.content:
            location = (magicpage.page, line)
            if content in magicvalid:
                # Do not skip valid magic content, Text for example
                continue
            if visited.contains(location):
                continue
            flat.append((*location, None))
    for navigator in navigators:
        for index, line in enumerate(navigator):
            location = (navigator.page, index)
            if visited.contains(location):
                continue
            flat.append((*location, line))
    # sort by page and line
    flat = sorted(flat, key=operator.itemgetter(0, 1))
    if sync:
        # TODO: WHY SHOULD WE DO THIS?
        # TODO: ADD DOCU HERE
        while flat and not isinstance(flat[0][2], iamraw.Headline):
            # sync to first headline
            flat = flat[1:]
    if yieldnone:
        flat = [
            item if isinstance(item[2], texmex.style.TextInfo) else
            (item[0], item[1], None) for item in flat
        ]
    return flat


def container_start(item):
    with contextlib.suppress(TypeError):
        return item[0]
    return item


def containers(item) -> tuple:
    with contextlib.suppress(TypeError):
        return tuple(range(item[0], item[1] + 1))
    return (item,)


def page_chunks(items):
    if not items:
        return []
    result = []
    page = None
    for item in items:
        if item[0] != page:
            result.append([item[0], [item[2]]])
            page = item[0]
        else:
            result[-1][1].append(item[2])
    return result
