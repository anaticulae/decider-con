# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import chapter.serialize
import configo
import iamraw
import protocol
import utila

import decider_chapter.document


def work(introx: str) -> protocol.ResultType:
    intro = chapter.serialize.load_chapter_introinfo(introx)
    driver = protocol.driver(intro=intro)
    document = decider_chapter.document.document()
    user, developer = protocol.run(
        __name__,
        driver=driver,
        document=document,
    )
    return user, developer


SOLUTION_6500 = """\
Einleitung unvollständig

Überprüfen Sie die Einleitung und achten darauf dass der Bereich: \
**{{topic}}** ausreichend dargestellt ist.

Siehe optimaler Aufbau:
{aufbau_gliederung/kapitel1}

TODO: ADD AI-USED HINT
"""

TOKEN_OCCURRENCE_MIN = configo.HV_INT_PLUS(default=3)


@protocol.nodiss
@protocol.nobook
@protocol.nosmall
def check_6500_intro_complete(linter: callable, driver):
    intro = driver.intro
    if driver.intro.pagestart is None:
        # TODO: CHANGE TO COMMON ERROR MESSAGE
        utila.error('no intro loaded - could not check 6500')
        return
    # 'start', 'goal', 'method', 'limit', 'structure'
    start = len(intro.start) >= TOKEN_OCCURRENCE_MIN
    goal = len(intro.goal) >= TOKEN_OCCURRENCE_MIN
    method = len(intro.method) >= TOKEN_OCCURRENCE_MIN
    limit = len(intro.limit) >= TOKEN_OCCURRENCE_MIN
    structure = len(intro.structure) >= TOKEN_OCCURRENCE_MIN

    location = iamraw.Location.from_page(page=driver.intro.pagestart)
    linter = functools.partial(linter, location=location)
    if not start:
        linter(topic='Hinführung zum Thema')
    if not goal:
        linter(topic='Ziel der Arbeit')
    if not method:
        linter(topic='Beschreibung der Methodik')
    if not limit:
        linter(topic='Abgrenzung der Arbeit')
    if not structure:
        linter(topic='Aufbau der Arbeit')
