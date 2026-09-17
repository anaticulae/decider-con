# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import serializeraw

import textflow_.docref.basic
import textflow_.docref.style


def work(  # pylint:disable=W0613
    ref_figure: str,
    ref_section: str,
    ref_table: str,
    caption_image: str,
    caption_table: str,
    sentences: str,
    headlines: str,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = create_driver(**locals())
    result = protoerror.run(
        modulename=[
            textflow_.docref.basic,
            textflow_.docref.style,
        ],
        driver=driver,
    )
    return result


def create_driver(
    ref_figure: str,
    ref_section: str,
    ref_table: str,
    caption_image: str,
    caption_table: str,
    sentences: str,
    headlines: str,
    pages: tuple = None,
) -> 'Driver':
    ref_figure = serializeraw.load_docref(ref_figure, pages=pages)
    ref_section = serializeraw.load_docref(ref_section, pages=pages)
    ref_table = serializeraw.load_docref(ref_table, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    sentences = serializeraw.load_text(
        sentences,
        headlines=headlines,
        pages=pages,
    )
    caption_image = serializeraw.load_captions(caption_image, pages=pages)
    caption_table = serializeraw.load_captions(caption_table, pages=pages)
    # prepare
    driver = protoerror.driver(
        ref_figure=ref_figure,
        ref_section=ref_section,
        ref_table=ref_table,
        headlines=headlines,
        sentences=sentences,
        caption_image=caption_image,
        caption_table=caption_table,
    )
    return driver
