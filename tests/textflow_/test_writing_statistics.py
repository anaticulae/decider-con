# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import textflow_.features
import textflow_.writing.statistics


def create_sentences(
    pdf,
    pages: tuple = None,
) -> textflow_.features.Sentences:
    utilotest.fixture_requires(pdf)
    source = hoverpower.link(pdf)
    headlines = serializeraw.load_headlines(source, pages=pages)
    words = serializeraw.load_text(
        content=source,
        headlines=headlines,
        pages=pages,
    )
    sentences = textflow_.features.Sentences(words)
    return sentences


def test_statistics():
    sentences = create_sentences(hoverpower.MASTER110_PDF)
    stats = textflow_.writing.statistics.determine(sentences)
    assert stats.words
    assert stats.word_min
