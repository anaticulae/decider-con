# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import decider_textflow.docref.matches

SOLUTION_7230 = """\
Rückwärtsreferenz Abbildung

Die Referenz **{{intext}}** auf Seite {{page}} verweist auf eine \
davorliegende Abbildung.

Verbessern Sie die innere Logik/Argumentation des Textes und verwenden \
Sie nur Referenzen nach vorne um ein besseres Verständnis der Arbeit zu \
erreichen.

Tipp: Dies vermeidet auch ständiges hin- und herblättern.
"""


def check_7230_figure_backward_reference(linter: callable, driver):
    matcher = decider_textflow.docref.matches.create_matcher(
        references=driver.ref_figure,
        iois=driver.caption_image,
    )
    validated = matcher.validate()
    for backward in validated.backward:
        page, data = backward
        location = iamraw.Location.from_page(page=page)
        linter(
            intext=data.raw,
            page=page,
            location=location,
        )


SOLUTION_7231 = """\
Rückwärtsreferenz Tabelle

Die Referenz **{{intext}}** auf Seite {{page}} verweist auf eine \
davorliegende Tabelle.

Verbessern Sie die innere Logik/Argumentation des Textes und verwenden \
Sie nur Referenzen nach vorne um ein besseres Verständnis der Arbeit zu \
erreichen.

Tipp: Dies vermeidet auch ständiges hin- und herblättern.
"""


def check_7231_table_backward_reference(linter: callable, driver):
    matcher = decider_textflow.docref.matches.create_matcher(
        references=driver.ref_table,
        iois=driver.caption_table,
    )
    validated = matcher.validate()
    for backward in validated.backward:
        page, data = backward
        location = iamraw.Location.from_page(page=page)
        linter(
            intext=data.raw,
            page=page,
            location=location,
        )
