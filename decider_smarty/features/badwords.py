# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_smarty.driver
import decider_smarty.utils


def work(
    avoid: str,
    improvement: str,
    phrases: str,
    pleonasma: str,
    reduce: str,
    pages: tuple = None,
) -> tuple[str, str]:
    driver = decider_smarty.driver.create(
        avoid,
        improvement,
        phrases,
        pleonasma,
        reduce,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_W8100 = """\
Umgangssprache erkannt

Vermeiden Sie **{{phrase}}** und ersetzen Sie diese durch eine \
förmlichere Formulierung.

{text/stilkunde/woerter/wortwahl}
"""


def check_8100_non_formal_speach(linter: callable, driver):
    for error in driver.phrases:
        location = decider_smarty.utils.create_location(error)
        better = f'({error.replacement})' if error.replacement else ''
        linter(location=location, phrase=error.raw, better=better)


SOLUTION_W8105 = """\
Pleonasma erkannt

Vermeiden Sie **{{phrase}}** und reduzieren Sie diesen auf das \
Wesentliche **{{better}}**.

{text/stilkunde/woerter/pleonasmen}
"""


def check_8105_pleonasms_detected(linter: callable, driver):
    for error in driver.pleonasma:
        location = decider_smarty.utils.create_location(error)
        better = f'({error.replacement})' if error.replacement else ''
        linter(location=location, phrase=error.raw, better=better)


SOLUTION_W8110 = """\
Unnötige Vorsilbe

Reduzieren Sie **{{phrase}}** indem Sie die unnötige Vorsilbe {{better}} \
entfernen.

TODO
"""


def check_8110_not_required_prefix(linter: callable, driver):
    for error in driver.reduce:
        location = decider_smarty.utils.create_location(error)
        better = f'({error.replacement})' if error.replacement else ''
        linter(location=location, phrase=error.raw, better=better)


SOLUTION_W8115 = """\
Ungenaue Formulierung erkannt

Die Formulierung **{{phrase}}** ist sehr unkonret. Besser ist **{{better}}**. \
{{hint}}
"""


def check_8115_required_improvement(linter: callable, driver):
    for error in driver.improvement:
        location = decider_smarty.utils.create_location(error)
        better = f'({error.replacement})' if error.replacement else '???'
        hint = f'({error.hint})' if error.hint else ''
        linter(
            location=location,
            phrase=error.raw,
            better=better,
            hint=hint,
        )


SOLUTION_W8120 = """\
Adjektiv verbessern

Die Formulierung **{{phrase}}** ist sehr unkonret. Besser ist **{{better}}**.
"""


def check_8120_better_adjective(linter: callable, driver):
    for error in driver.avoid:
        location = decider_smarty.utils.create_location(error)
        better = f'({error.replacement})' if error.replacement else '???'
        linter(
            location=location,
            phrase=error.raw,
            better=better,
        )
