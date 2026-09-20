# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import germania
import iamraw
import texmex
import utilo

SENTENCE_LENGTH_MIN = configos.HV_INT_PLUS(default=7)


def determine_sentences(
    sentences,
    special_skip: bool = False,
) -> list:
    result = []
    for sentence in sentences:
        if isinstance(sentence, iamraw.Headline):
            continue
        txt = sentence[0]
        if len(txt) < SENTENCE_LENGTH_MIN:
            continue
        if special_skip and texmex.nosentence(txt):
            continue
        sento = word_tokenize(txt)
        if not sento:
            continue
        if len(sento) < 3:
            continue
        result.append((sento, sentence[1], sentence[2]))
    return result


def word_tokenize(txt: str) -> list:
    tokens = germania.word_tokenize(txt, validate_sentences=False)
    tokens = [item.lower() for item in tokens if isinstance(item, str)]
    tokens = [item for item in tokens if utilo.char_rate(item) == 1.0]
    tokens = [item for item in tokens if len(item) >= 2]
    return tokens
