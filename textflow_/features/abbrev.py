# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Text Behavior
==========================

This module verifies the detected abbreviation in textual flow.

TODO:

* No abbreviation at sentence start
* Insert `Festabstand` between characters
* No Linebreak inside abbreviation
* Ensure no artikel before abbreviation: " S.5. Bd. 6" but "die Seite 5,
  der Band 8"

[Source DUDEN]
"""

import itertools

import iamraw
import protoerror
import serializeraw
import utilo


def work(abbreviations: str, text: str) -> tuple[str, str]:
    if not utilo.exists(abbreviations):
        utilo.error(f'no abbreviation table: {abbreviations}, '
                    'skip abbreviation_text')
        return protoerror.RESULT_EMPTY

    abbreviations = serializeraw.load_abbreviation_table(abbreviations)
    text = serializeraw.load_text_abbreviations(text)
    driver = protoerror.driver(
        abbr_table=abbreviations,
        abbr_text=text,
    )
    result = protoerror.run(
        __name__,
        driver=driver,
    )
    return result


SOLUTION_E5100 = """\
Abkürzung wurde vor der Definition benutzt

Die Abkürzung "{{short}}" wurde auf Seite {{before_page}}, Satz \
{{before_sentence}} benutzt bevor sie auf Seite {{definition_page}}, \
Satz {{definition_sentence}} definiert wurde.

Definieren Sie die Abkürzung an der ersten Stelle des Gebrauchs.

{text/abkuerzung#abkurzung}
"""


def check_5100_used_before_defined(linter: callable, driver):
    # TODO: Use table to verify lintings?
    flat = utilo.flatten_content(driver.abbr_text)
    grouped = itertools.groupby(flat, key=lambda x: x.short)
    for key, values in grouped:
        values = list(values)
        if len(values) == 1:
            continue
        if values[0].description is not None:
            # abbreviation is defined at first occurrence
            continue
        defined_later = [
            item for item in values[1:] if item.description is not None
        ]
        if not any(defined_later):
            # abbreviation is nowhere defined
            continue
        for item in defined_later:
            linter(
                short=key,
                before_page=values[0].position.page,
                before_sentence=values[0].position.sentence,
                definition_page=item.position.page,
                definition_sentence=item.position.page,
            )


SOLUTION_E5110 = """\
Abkürzung wurde nicht im Text verwerdet

Die Abkürzung "{{short}}" konnte nicht im Text gefunden werden.
"""


def check_5110_unused_abbreviation(linter: callable, driver):
    table: iamraw.AbbreviationResult = driver.abbr_table
    text: iamraw.ExtractedTextAbbreviations = driver.abbr_text
    flat = utilo.flatten_content(text)
    unique = {item.short for item in flat}
    for item in table:
        if item.short in unique:
            continue
        linter(short=item.short)
