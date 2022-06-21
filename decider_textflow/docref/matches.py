# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
IoI: Item of interest

>>> matcher = ReferenceMatcher()
>>> matcher.add_ioi(page=10, number=15, raw='Figure 15: The mother of Susej')
>>> matcher.add_ioi(page=12, number=16, raw='Figure 16: The brother of Sesom')
>>> matcher.add_ioi(page=5, number='3.1', raw='Abbildung 3.1: Man oh man, was schreibe ich hier?')

The holiest mother can be see in Fig. 15.
>>> matcher.add_reference(5, 15, 'in Fig. 15.', sentence=3, char=31)

Missing fig reference
>>> matcher.add_reference(4, 20, 'in Fig. 20.', sentence=1, char=1)
>>> matcher.match()
([(5, IntextRef(ref='15', raw='in Fig. 15.', sentence=3, char=31))],\
 [(4, IntextRef(ref='20', raw='in Fig. 20.', sentence=1, char=1))],\
 [(12, IoI(number='16', raw='Figure 16: The brother of Sesom', page=12)),\
 (5, IoI(number='3.1', raw='Abbildung 3.1: ...', page=5))])

>>> matcher.validate()
ReferenceMatched(not_referenced=[(12, IoI(number='16'...)), (5, IoI(number='3.1'...))],\
 invalid=[(4, IntextRef(ref='20', raw='in Fig. 20.', sentence=1, char=1))],\
 backward=[],\
 good=[(5, IntextRef(ref='15', raw='in Fig. 15.', sentence=3, char=31))])
"""

import collections
import dataclasses

import utila


@dataclasses.dataclass
class ReferenceMatched:
    # ioi not referenced
    not_referenced: list = dataclasses.field(default_factory=list)
    # no ioi detected
    invalid: list = dataclasses.field(default_factory=list)
    # reference page before
    backward: list = dataclasses.field(default_factory=list)
    # valid reference
    good: list = dataclasses.field(default_factory=list)


IntextRef = collections.namedtuple('IntextRef', 'ref raw sentence char')

IoI = collections.namedtuple('IoI', 'number, raw, page')


class ReferenceMatcher:

    def __init__(self):
        self.iois = collections.defaultdict(list)
        self.iois_page = dict()
        self.references = collections.defaultdict(list)

    def add_ioi(self, page: int, number: str, raw: str = None):
        number = str(number)
        ioi = IoI(number, raw, page)
        if number in [ioi.number for ioi in self.iois[page]]:
            utila.error(f'duplicated ioi number: {number} on page {page}')
        self.iois[page].append(ioi)
        self.iois_page[number] = page

    def add_reference(
        self,
        page: int,
        ref: str,
        raw: str = None,
        sentence: int = None,
        char: int = None,
    ):
        ref = str(ref)
        data = IntextRef(ref, raw, sentence, char)
        self.references[page].append(data)

    def find_dynamic_ref(self, page: int) -> str:
        """Look forward to detect a reference which is mean by the user.

        # TODO: IMPROVE SEARCHER
        PROBLEM:

        ```
            Siehe naechste Abbildung
            <Image>
            Siehe Abbildung danach
            <Image>

            Second reference on a single page will detect the first one.
        ```
        """
        # look 3 pages a head
        for _ in range(3):
            if not page in self.iois:
                page += 1
                continue
            first = self.iois[page][0]
            return first.number
        return None

    def validate(self) -> ReferenceMatched:
        matched, not_matched, not_referenced = self.match()
        backward = []
        for match in matched:
            page = match[0]
            reference = match[1][0]
            if page <= self.iois_page[reference]:
                # reference before ioi, everything fine here
                continue
            # reference after occurence
            backward.append(match)
        good = [item for item in matched if item not in backward]
        result = ReferenceMatched(
            not_referenced=not_referenced,
            invalid=not_matched,
            backward=backward,
            good=good,
        )
        return result

    def match(self):
        iois = utila.flat([(page, value)
                           for value in values]
                          for page, values in self.iois.items())
        todos = utila.flat([(page, value)
                            for value in values]
                           for page, values in self.references.items())
        matched, not_matched, referenced = [], [], []
        while todos:
            todo = todos.pop()
            done = False
            for ioi in iois:
                ioi_ref = ioi[1].number
                if ioi_ref == todo[1].ref:
                    matched.append(todo)
                    referenced.append(ioi)
                    done = True
                    break
            if not done:
                not_matched.append(todo)
        not_referenced = [item for item in iois if item not in referenced]
        return matched, not_matched, not_referenced


def create_matcher(references, iois) -> ReferenceMatcher:
    result = ReferenceMatcher()
    for ioi in utila.flatten_content(iois):
        result.add_ioi(page=ioi.pdfpage, number=ioi.number, raw=ioi.raw)
    for reference in references:
        for start, raw in zip(reference.marked, reference.raw):
            test = raw.lower()
            if 'folgend' in test or 'unten' in test:
                ref = result.find_dynamic_ref(reference.page)
                if ref is None:
                    utila.error(f'could not find forward ref: {reference}')
                    continue
            else:
                ref = parse_reference(raw)
            # TODO: CHAR IS NOT WORD
            result.add_reference(
                page=reference.page,
                ref=ref,
                raw=raw,
                sentence=reference.sentence,
                char=start,
            )
    return result


LEVEL = utila.compiles(r"""
    (
        \d{1,2}
        (\.\d{1,3}){0,3}
        \.{0,1}
    )
""")


def parse_reference(raw: str) -> str:
    parsed = LEVEL.search(raw)
    if not parsed:
        utila.error(f'invalid reference: {raw}')
        return None
    result = parsed[0]
    return result
