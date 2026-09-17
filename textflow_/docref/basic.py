# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import textflow_.docref.matches

SOLUTION_7200 = """\
Referenz nicht gefunden

Der Abbildungs-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7200_figure_reference_exists(linter: callable, driver):
    matcher = textflow_.docref.matches.create_matcher(
        references=driver.ref_figure,
        iois=driver.caption_image,
    )
    validated = matcher.validate()
    for invalid in validated.invalid:
        page, data = invalid
        location = iamraw.Location.from_sentence(
            page=page,
            sentence=data.sentence,
        )
        linter(
            location=location,
            reference=data.raw,
        )


SOLUTION_E7201 = """\
Abbildung nicht referenziert

Im Text wurde kein Bezug auf die Abbildung **{{caption}}** gefunden. \
Überprüfen Sie, ob eine Erwähnung im Text nötig ist.
"""


def check_7201_figure_missing_intext_ref(linter: callable, driver):
    matcher = textflow_.docref.matches.create_matcher(
        references=driver.ref_figure,
        iois=driver.caption_image,
    )
    validated = matcher.validate()
    for invalid in validated.not_referenced:
        page, data = invalid
        location = iamraw.Location.from_page(page=page)
        linter(
            location=location,
            caption=data.raw,
        )


SOLUTION_7202 = """\
Referenz nicht gefunden

Der Tabellen-Verweis **{{reference}}** kann nicht gefunden werden.
"""


def check_7202_table_reference_exists(linter: callable, driver):
    matcher = textflow_.docref.matches.create_matcher(
        references=driver.ref_table,
        iois=driver.caption_table,
    )
    validated = matcher.validate()
    for invalid in validated.invalid:
        page, data = invalid
        location = iamraw.Location.from_sentence(
            page=page,
            sentence=data.sentence,
        )
        linter(
            location=location,
            reference=data.raw,
        )


SOLUTION_E7203 = """\
Tabelle nicht referenziert

Im Text wurde kein Bezug auf die Tabelle **{{caption}}** gefunden. \
Überprüfen Sie, ob eine Erwähnung im Text nötig ist.
"""


def check_7203_table_missing_intext_ref(linter: callable, driver):
    matcher = textflow_.docref.matches.create_matcher(
        references=driver.ref_table,
        iois=driver.caption_table,
    )
    validated = matcher.validate()
    for invalid in validated.not_referenced:
        page, data = invalid
        location = iamraw.Location.from_page(page=page)
        linter(
            location=location,
            caption=data.raw,
        )
