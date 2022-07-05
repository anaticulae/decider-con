# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import protocol
import serializeraw
import texmex
import utila

MORETHAN = 10


def work(
    sentences: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    sentences = serializeraw.load_text(
        sentences,
        pages=pages,
    )
    driver = protocol.driver(sentences=sentences)
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


def check_character(linter, driver, regex):
    for page in utila.flatten_content(driver.sentences):
        sentences, pagenumbers = page.content, page.pages
        for sentence, pagenumber in zip(sentences, pagenumbers):
            if texmex.nosentence(sentence):
                # do not judge list, formula etc.
                continue
            # TODO: SUPPORT MULTIPLE ERRORS IN ONE LINE
            matched = regex.finditer(sentence)
            if not matched:
                continue
            for match in matched:
                # TODO: ADJUST LINE LATER
                location = iamraw.RangedLocation(
                    page=pagenumber,
                    line=0,
                    char=match.start(),
                    char_end=match.end(),
                )
                linter(
                    location=location,
                    text=utila.extract_match(match),
                )


SOLUTION_7650 = """\
Unzuläßiges Leerzeichen vor Komma

Ungültiges Leerzeichen vor einem Komma erkannt.

{darstellung/satzzeichen#komma}
"""

SPACE_BEFORE_COMMA = utila.compiles(r'\s+\,')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7650_space_before_comma(linter: callable, driver):
    """\
    >>> message('space before , comma', 7650)
    1
    """
    check_character(linter, driver, SPACE_BEFORE_COMMA)


SOLUTION_7651 = """\
Fehlendes Leerzeichen nach Komma

Fehlendes Leerzeichen nach einem Komma erkannt.

{darstellung/satzzeichen#komma}
"""

# TODO: ADD RISE to DISTINGUISH OF NORMAL NUMBERS
MISSING_SPACE_AFTER_COMMA = utila.compiles(r'\,[a-zA-Z]{3,}')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7651_missing_space_after_comma(linter: callable, driver):
    """\
    >>> message('hightnote: ,10', 7651)
    0
    >>> message('normal text: this is helmut,space missing', 7651)
    1

    # TODO: REQUIRE FORMULA CHECKER, USE MAGIC LINE/CONTENT?
    >>> message('Einführung von nmot,t = Tmot,t/TfB = 12 zusätzlichen')
    0
    """
    check_character(linter, driver, MISSING_SPACE_AFTER_COMMA)


SOLUTION_7652 = """\
Unzuläßiges Leerzeichen vor eckiger Klammer

Ungültiges Leerzeichen vor einer eckigen Klammer erkannt.

{darstellung/satzzeichen#klammer}
"""

SPACE_BEFORE_SQUARE_BRACKET = utila.compiles(r"""
    [^\[\s]     # no open square bracket or space
    \s+         # white space(s) before closing bracket
    \]          # close with square bracket
""")


@protocol.disable_perpage(morethan=MORETHAN)
def check_7652_space_before_square_bracket(linter: callable, driver):
    """\
    >>> message('[Jens ] space inside author reference', 7652)
    1
    >>> message('[] [ ] [  ] [   ] replace with [...]', 7652)
    0
    """
    check_character(linter, driver, SPACE_BEFORE_SQUARE_BRACKET)


SOLUTION_7653 = """\
Unzuläßiges Leerzeichen nach eckiger Klammer

Ungültiges Leerzeichen nach einer eckigen Klammer erkannt.
"""

SPACE_AFTER_SQUARE_BRACKET = utila.compiles(r"""
    \[          # start with open square bracket
    \s+?        # one or more space after open square bracket
    (?!\s*\])   # do not end with spaces and ] to distinguish from
                # [ ] error message
""")


@protocol.disable_perpage(morethan=MORETHAN)
def check_7653_space_after_square_bracket(linter: callable, driver):
    """\
    >>> message('[ Jens] space inside author reference', 7653)
    1
    >>> message('[  DoubleSpace]', 7653)
    1
    >>> message('[   ] [  ] [ ] replace with [...]', 7653)
    0
    """
    check_character(linter, driver, SPACE_AFTER_SQUARE_BRACKET)


SOLUTION_7654 = """\
Leerzeichen vor Semikolon

Unzuläßiges Leerzeichen vor Semikolon erkannt.

{darstellung/satzzeichen#semikolon}
"""

SPACE_BEFORE_SEMICOLON = utila.compiles(r'\s+\;')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7654_space_before_semicolon(linter: callable, driver):
    check_character(linter, driver, SPACE_BEFORE_SEMICOLON)


SOLUTION_7655 = """\
Fehlendes Leerzeichen nach Semicolon

Fehlendes Leerzeichen nach Semicolon erkannt.

{darstellung/satzzeichen#semikolon}
"""

MISSING_SPACE_AFTER_SEMICOLON = utila.compiles(r'\;[^\s]')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7655_missing_space_after_semicolon(linter: callable, driver):
    check_character(linter, driver, MISSING_SPACE_AFTER_SEMICOLON)


SOLUTION_7656 = """\
Fehlerhaftes Auslassungszeichen

Gefunden **[ ]** ersetzen Sie es durch **[...]**

{darstellung/satzzeichen#auslassungspunkte}
"""

MISSING_DOTS_BETWEEN_ANGLE_BRACKETS = utila.compiles(r'\[\s*\]')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7656_missing_dots_between_brackets(linter: callable, driver):
    """\
    >>> message('[] replace with [...]', 7656)
    1
    >>> message('[  ] replace with [...]', 7656)
    1
    """
    check_character(linter, driver, MISSING_DOTS_BETWEEN_ANGLE_BRACKETS)


SOLUTION_7659 = """\
Falscher Komparativ

**{{text}}**.

Siehe Duden:

* 5-mal
* 4-silbig
* 100-prozentig
* 1-zeilig

{darstellung/satzzeichen#divis}
"""

NUMBER_MAL = utila.compiles(r"""
    \d{1,3}
    [ ]?
    [-]?
    [ ]?
    [x]
    [ ]{1,3}
    (wenig|weniger|mehr)
""")


def check_7659_invalid_comparativ_mal(linter: callable, driver):
    """\
    >>> message('7x weniger Impressionen pro Follower und 11 x mehr Klicks', 7659)
    2
    """
    check_character(linter, driver, NUMBER_MAL)


SOLUTION_7660 = """\
Bindestrich zwischen Ziffer und 'mal' fehlt.

Siehe Duden:

* 2-mal
* fünfhundert Mal
* ein Dutzend Mal

Hinweis: Ziffern werden bei exakten Werten verwendet - ausgeschrieben \
wird die Zahl wenn sie eine ungefähre Zahl beinhaltet.

{darstellung/satzzeichen#divis}
"""

MISSING_MINUS_BETWEEN_VALUE_AND_SIGN = utila.compiles(r'\d{1,4}(mal)')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7660_missing_minus_value_and_sign(linter: callable, driver):
    """Number in combination with `mal` is connected with minus. But
    `zweihundert Mal` is correct, no minus is needed.

    >>> message('300mal ist nicht so gut wie 600-mal', 7660)
    1
    """
    check_character(linter, driver, MISSING_MINUS_BETWEEN_VALUE_AND_SIGN)


SOLUTION_7661 = """\
Schrägstrich: Überflüssiges Leerzeichen

Vor und nach einem Schrägstrich wird kein Leerzeichen gesetzt.

{darstellung/satzzeichen#schragstrich}
"""

SPACE_BEFORE_OR_AFTER_SLASH = utila.compiles(r'([ ]\/[ ]|[ ]\/|\/[ ])')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7661_space_before_or_after_slash(linter: callable, driver):
    r"""\
    >>> message('Europäischen Gemeinschaften (Beutler / Bieber / Pipkorn / Streil 2001).', 7661)
    3
    >>> message('Bitte wählen Mann/ Frau., 7661')
    1
    >>> message('dieser bei 1.44/1.63, den Mittelaltrigen bei 0.72/0.483', 7661)
    0
    >>> message('no/\nnewline problem.', 7661)
    0
    """
    check_character(linter, driver, SPACE_BEFORE_OR_AFTER_SLASH)


SOLUTION_7662 = """\
Fehlendes Leerzeichen nach Paragraf

Zwischen Paragrafzeichen und der Paragrafnummer wird ein Festabstand gesetzt.

{darstellung/satzzeichen#paragrafzeichen}
"""

SPACE_AFTER_PARAGRAPH = utila.compiles(r'§\d+[a-z]?')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7662_space_after_paragraph(linter: callable, driver):
    """\
    >>> message('StVG §24c „ […] wer in der Probezeit nach §2a oder vor', 7662)
    2
    >>> message('um eine Straftat nach § 316, welches', 7662)
    0
    """
    # TODO: LINT MORE PARAGRAPH §301.223.232 for example
    check_character(linter, driver, SPACE_AFTER_PARAGRAPH)


SOLUTION_7663 = """\
Bindestrich fehlt

Siehe Duden:

* vierjährig
* 4-jährig
* Fünfjähriger
* die 4- bis 5-Jährigen

{darstellung/satzzeichen#divis}
"""

MISSING_MINUS_BETWEEN = utila.compiles(r'\d{1,5}(jährig)(en){0,1}')


@protocol.disable_perpage(morethan=MORETHAN)
def check_7663_missing_minus_number_jaehrig(linter: callable, driver):
    """\
    >>> message('25jährigen und die ab 69jährigen in Unfälle verwickelt waren.', 7663)
    2
    """
    check_character(linter, driver, MISSING_MINUS_BETWEEN)


SOLUTION_7665 = """\
Unnötige Genauigkeit

Zahlen geschrieben als Ziffern symbolisieren eine exakte Genauigkeit. \
Diese Genauigkeit wird durch den Zusatz **circa, ca. oder etwa** \
relativiert. Schreiben Sie die Zahl aus um dies deutlich zu machen.

{darstellung/schreibweise#zahlen}
"""

WRONG_ACCURACY = utila.compiles(r'(etwa|circa|\bca\.?\b)[ ]{0,4}\d+')

# def check_7665_wrong_accuracy(linter: callable, driver):
#     """\
#     >>> message('Etwa 1000 Einwohner wohnen hier. Circa 12 Menschen wohnen hier.', 7665)
#     2
#     """
#     TODO: INVESTIGATE LATER
#     check_character(linter, driver, WRONG_ACCURACY)

SOLUTION_7666 = """\
Überflüßiges Leerzeichen

vor hochgestellter Zahl **{{text}}**.

{darstellung/satzzeichen}
"""

HIGHNOTE_SPACE_BEFORE = utila.compiles(r'[ ]{1,4}{{hn:\d{1,4}:nh}}')


def check_7666_highnote_space_error(linter: callable, driver):
    """\
    >>> message('Dies ist eine Fußnote{{hn:3:nh}}', 7666)
    0
    >>> message('Dies ist eine Fußnote  {{hn:3:nh}}', 7666)
    1
    >>> message('hinaus. {{hn:60:nh}}')
    1
    """
    check_character(linter, driver, HIGHNOTE_SPACE_BEFORE)


SOLUTION_7667 = """\
Überflüßiges Leerzeichen

nach hochgestellter Zahl **{{text}}**.

{darstellung/satzzeichen}
"""

HIGHNOTE_SPACE_TOO_MANY_AFTER = utila.compiles(r'{{hn:\d{1,4}:nh}}[ ]{2,6}')


def check_7667_highnote_space_error(linter: callable, driver):
    """\
    >>> message('Dies ist eine Fußnote{{hn:4:nh}}   zu viel Platz danach.', 7667)
    1
    """
    check_character(linter, driver, HIGHNOTE_SPACE_TOO_MANY_AFTER)


def message(lines: list, msgid=None, page=0):
    if isinstance(lines, str):
        lines = [lines]
    sentences = [
        iamraw.PageContentText(
            page=page,
            content=[
                iamraw.TextSection(
                    content=lines,
                    pages=[page] * len(lines),
                )
            ],
        )
    ]
    driver = protocol.driver(sentences=sentences)
    user, _ = protocol.run(
        __name__,
        driver=driver,
    )
    result = serializeraw.load_findings(user, msgid)
    return len(result)
