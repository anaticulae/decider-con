# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import protoerror
import serializeraw
import utilo

import textflow_.utils


def create_driver(  # pylint:disable=R0913,R0914
    headlines,
    text,
    textpositions,
    sizeandborders,
    headerfooter,
    lists=None,
    magiccontent=None,
    textstyle=None,
    magicvalid=None,
    quotations=None,
    words=None,
    pagenumbers_magic=None,
    pages=None,
):
    assert magiccontent is None or isinstance(magiccontent, str), 'require path'
    if magicvalid is None:
        magicvalid = iamraw.TEXTUAL  # pylint:disable=E1101
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    navigators = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborder=sizeandborders,
        headerfooter=headerfooter,
        pages=pages,
    )
    if not navigators:
        utilo.error('no navigators given')
        return None
    lists = serializeraw.load_lists(lists, pages=pages) if lists else []
    if not headlines:
        utilo.error('no headlines given')
    if utilo.exists(magiccontent):
        magiccontent = serializeraw.load_magic_types(magiccontent, pages=pages)
    else:
        magiccontent = None
    chunks = textflow_.utils.text_chunks(
        headlines,
        navigators,
    )
    nomagic = textflow_.utils.text_chunks(
        headlines,
        navigators,
        magiccontent=magiccontent,
        magicvalid=magicvalid,
    )
    if utilo.exists(quotations):
        quotations = serializeraw.load_quotations(
            quotations,
            pages=pages,
        )
    else:
        # empty quotations
        # Hint: Empty list is required to avoid failing later algorithms.
        quotations = []
    sentences = []
    if words:
        words = serializeraw.load_text(
            words,
            headlines,
            pages=pages,
        )
        sentences: Sentences = Sentences(words)
    if pagenumbers_magic and utilo.exists(pagenumbers_magic):
        pagenumbers_magic = serializeraw.load_pagenumbers_magic(
            pagenumbers_magic,
            pages=pages,
        )
    else:
        pagenumbers_magic = None
    if textstyle:
        return protoerror.driver(
            text_chunks=chunks,
            nomagic_text_chunks=nomagic,
            doctextstyle=textstyle,
            quotations=quotations,
            sentences=sentences,
            navigators=navigators,
            headlines_confidence=confidence(headlines),
            pagenumbers_magic=pagenumbers_magic,
        )
    return protoerror.driver(
        text_chunks=chunks,
        nomagic_text_chunks=nomagic,
        quotations=quotations,
        sentences=sentences,
        navigators=navigators,
        headlines_confidence=confidence(headlines),
        pagenumbers_magic=pagenumbers_magic,
    )


def confidence(headlines) -> float:
    headlines_confidence = 1.0
    if not headlines:
        return headlines_confidence
    try:
        # TODO: REMOVE LATER AFTER UPGRADING IAMRAW
        headlines_confidence = headlines.confidence
        if headlines_confidence is None:
            return 1.0
    except AttributeError:
        utilo.error('require headlines.confidence, use 1.0')
    return headlines_confidence


class Sentences:

    def __init__(self, words):
        self.content = []
        for contenttext in words:
            for textsection in contenttext.content:
                # yield headline
                if textsection.headline and textsection.headline.container != -1:
                    # TODO: IS HEADLINE IMPORTANT? THIS MAY PRODUCE AN ERROR LATER?
                    self.content.append(textsection.headline)
                merged = list(
                    zip(
                        textsection.content,
                        textsection.pages,
                        range(len(textsection.pages)),
                    ))
                self.content.extend(merged)

    def __getitem__(self, index):
        return self.content[index]


class SentenceLookup:

    def __init__(self, words):
        self.content = collections.defaultdict(list)
        for contenttext in words:
            for textsection in contenttext.content:
                merged = list(
                    zip(
                        textsection.content,
                        textsection.pages,
                        range(len(textsection.pages)),
                    ))
                for sentence, page, _ in merged:
                    self.content[page].append(sentence)
        # enable KeyError
        self.content: dict = dict(self.content)

    def __call__(self, page, sentence) -> str:
        return self.content[page][sentence]
