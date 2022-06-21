# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import statistics

import configo
import utila

import decider_textflow.writing.utils


@dataclasses.dataclass
class WritingStatistics:
    words: int = None
    sentences: int = None

    word_avg: float = None
    sentence_avg: float = None

    word_min: int = None
    word_max: int = None

    sentence_min: int = None
    sentence_max: int = None


SENTENCE_LENGTH_MIN = configo.HV_INT_PLUS(default=7)


def determine(sentences) -> WritingStatistics:
    sentences = decider_textflow.writing.utils.determine_sentences(sentences)
    if not sentences:
        # no data given, skip analysis
        return None
    result = WritingStatistics()
    sento = []
    words = collections.defaultdict(int)
    for sentence in sentences:
        for word in sentence[0]:
            words[word] += 1
        sento.append(len(sentence[0]))
    result.words = sum(words.values())
    result.sentences = len(sento)

    result.word_min = sorted(words.keys(), key=len)[0]
    result.word_max = sorted(words.keys(), key=len)[-1]
    result.sentence_min = min(sento)
    result.sentence_max = max(sento)

    wordo = utila.flatten([[len(key)] * value for key, value in words.items()])
    result.word_avg = statistics.mean(wordo)
    result.sentence_avg = statistics.mean(sento)

    result.word_avg: float = utila.roundme(result.word_avg)
    result.sentence_avg: float = utila.roundme(result.sentence_avg)
    return result
