# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textflow.features
import decider_textflow.writing.statistics


def create_sentences(
    pdf,
    pages: tuple = None,
) -> decider_textflow.features.Sentences:
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    headlines = serializeraw.load_headlines(source, pages=pages)
    words = serializeraw.load_text(
        content=source,
        headlines=headlines,
        pages=pages,
    )
    sentences = decider_textflow.features.Sentences(words)
    return sentences


def test_statistics():
    sentences = create_sentences(power.MASTER110_PDF)
    stats = decider_textflow.writing.statistics.determine(sentences)
    assert stats.words
    assert stats.word_min
