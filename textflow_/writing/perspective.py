# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import utilo

INVALID_PERSPECTIVE = utilo.splititems('wir man ich')


def invalid(words) -> list:
    # TODO: REPLACE WITH EXTERNAL METHOD
    words = [word for word in words if isinstance(word, str)]
    words = [word for word in words if word.lower() in INVALID_PERSPECTIVE]
    return words


def sentence_start(sentences: list, window: int = 3):
    result = []
    for sentence in sentences:
        result.append((sentence[0][0:window], sentence[1], sentence[2]))
    return result


def repeating_sentence_start(sentences, window: int = 3):
    result = []
    before = []
    for current in sentences:
        current = current[0][0:window], current[1], current[2]
        if not before:
            before = [current]
            continue
        if before[-1][0] == current[0]:
            # same start as before
            before.append(current)
            continue
        if len(before) > 1:
            result.append(before)
        before = [current]
    # equal sentences on document end
    if len(before) > 1:
        result.append(before)
    return result


def repeating_sentence(sentences, window: int = 3, occurence_min=2):
    # TODO: EXCLUDE OVERLAPPING?
    collected = collections.defaultdict(list)
    for current in sentences:
        txt = ' '.join(current[0][0:window])
        collected[txt].append(current[1:3])
    result = []
    for key, values in collected.items():
        if len(values) >= occurence_min:
            result.append((key, values))
    return result
