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
import iamraw
import protocol
import utila

import decider_chapter.document


def work(intro: str) -> protocol.ResultType:
    intro = chapter.serialize.load_chapter_introinfo(intro)
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

MIN_TOKEN_OCCURRENCE = 3  # TODO: HOLY VALUE


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
    start = len(intro.start) >= MIN_TOKEN_OCCURRENCE
    goal = len(intro.goal) >= MIN_TOKEN_OCCURRENCE
    method = len(intro.method) >= MIN_TOKEN_OCCURRENCE
    limit = len(intro.limit) >= MIN_TOKEN_OCCURRENCE
    structure = len(intro.structure) >= MIN_TOKEN_OCCURRENCE

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
