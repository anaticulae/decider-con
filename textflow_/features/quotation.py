# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import german
import iamraw
import konrad.quotation.german
import protoerror
import serializeraw

CITATION_LENGTH_MAX = configos.HV_INT_PLUS(default=50)

# TODO: SENTENCE END
# Ich kann mit Jugendlichen einen Spielplatz planen, aber nicht große europäische Politik machen.“.


def work(text: str, pages: tuple) -> protoerror.ResultType:
    quotations = serializeraw.load_quotations(
        text,
        pages=pages,
    )
    driver = protoerror.driver(quotations=quotations)
    result = protoerror.run(
        __name__,
        driver=driver,
    )
    return result


SOLUTION_7100 = """\
Nicht geschlossenes Zitat

Satz **{{sentence}}** enthält eine ungerade Anzahl von Anführungszeichen.

{darstellung/satzzeichen#anfuhrungszeichen}
"""


def check_7100_german_quote_not_closed(linter: callable, driver):
    for quote in driver.quotations:
        tokens = german.split_token(quote.sentence)
        if not german.isger(tokens):
            continue
        validated = konrad.quotation.german.double_quotation_closed(tokens)
        if validated:
            continue
        location = iamraw.Location.from_sentence(
            page=quote.page,
            sentence=quote.index,
        )
        linter(
            location=location,
            sentence=quote.sentence,
        )


SOLUTION_7101 = """\
Doppelte Anführungszeichen im Zitat

Satz **{{sentence}}** enthält doppelte Anführungszeichen im Zitat. Ersetzen \
Sie diese doppelten Anführungszeichen durch einfache Anführungszeichen.

{darstellung/satzzeichen#anfuhrungszeichen}
"""


def check_7101_german_quote_double_quote_inside(linter: callable, driver):
    for quote in driver.quotations:
        tokens = german.split_token(quote.sentence)
        if not german.isger(tokens):
            continue
        validated = konrad.quotation.german.double_quotation_closed(tokens)
        if not validated:
            continue
        if konrad.quotation.german.no_double_quotes_inside_double(tokens):
            continue
        location = iamraw.Location.from_sentence(
            page=quote.page,
            sentence=quote.index,
        )
        linter(
            location=location,
            sentence=quote.sentence,
        )


SOLUTION_7105 = """\
Zitat beginnt mit Auslassungszeichen

Am Zitatanfang **{{sentence}}** sind keine Auslassungszeichen [...] nötig.

TODO: ADD LINK
"""

QUOTATION_SIGNS = '„‚’"”“'  # TODO: REPLACE WITH MORE GENERAL PLACE


def check_7105_quote_starts_with_omission_sign(linter: callable, driver):
    """Sentence starts with [...]

    >>> message('„[...] Zitat darf nicht [...] mit Auslassung starten.“', 7105)
    1

    # support english later
    # >>> message('  „  [...] spaces are fine', 7105)
    >>> message('  „  [...] Leerzeicehn sind akzeptabel', 7105)
    1
    """
    for quote in driver.quotations:
        tokens = german.split_token(quote.sentence)
        if not german.isger(tokens):
            continue
        if len(tokens) < 2:
            continue
        if '[...]' not in ''.join(tokens):
            continue
        if tokens[0] not in QUOTATION_SIGNS:
            continue
        if tokens[1] not in '[...] [] ...'.split():
            continue
        location = iamraw.Location.from_sentence(
            page=quote.page,
            sentence=quote.index,
        )
        linter(
            location=location,
            sentence=quote.sentence,
        )


SOLUTION_7110 = """\
Zitat zu lang

Das Zitat **{{sentence}}** sollte verkürzt werden. Konzentrieren Sie \
sich auf den wichtigen Teil des Zitats und stellen Sie die eigene \
Denkleistung in den Vordergrund.

{text/zitat#umfang}
"""


def check_7110_max_citation_length(linter: callable, driver):
    for quote in driver.quotations:
        tokens = german.split_token(quote.sentence)
        if len(tokens) <= CITATION_LENGTH_MAX:
            continue
        location = iamraw.Location.from_sentence(
            page=quote.page,
            sentence=quote.index,
        )
        linter(
            location=location,
            sentence=quote.sentence,
        )


def message(quotation: str, msgid=None):
    driver = protoerror.driver(quotations=[
        iamraw.ExtractedQuotation(0, 0, quotation),
    ])
    user, _ = protoerror.run(modulename=__name__, driver=driver)
    result = serializeraw.load_findings(user, msgid)
    return len(result)
