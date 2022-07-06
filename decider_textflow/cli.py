# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_textflow

DESCRIPTION = ''

CONTENT_INPUT = [
    utila.ResultFile('headlines', 'result_result'),
    utila.ResultFile('rawmaker', 'oneline_text_text'),
    utila.ResultFile('rawmaker', 'oneline_text_positions'),
    utila.ResultFile('rawmaker', 'border_pages'),
    utila.ResultFile('groupme', 'footer_footerheader'),
]

WORKPLAN = [
    utila.create_step(
        'abbrev',
        [
            utila.ResultFile('reftable', 'abbrev_abbrev'),
            utila.ResultFile('words', 'abbreviation_detected'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'character',
        inputs=[
            utila.ResultFile('words', 'sentences_sentences'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'docref',
        inputs=[
            utila.ResultFile('docref', 'figure_parsed'),
            utila.ResultFile('docref', 'section_parsed'),
            utila.ResultFile('docref', 'table_parsed'),
            utila.ResultFile('caption', 'image_caption'),
            utila.ResultFile('caption', 'table_caption'),
            utila.ResultFile('words', 'sentences_sentences'),
            utila.ResultFile('headlines', 'result_result'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'lineending',
        inputs=[
            utila.ResultFile('textflow', 'lineending_lastchar'),
            utila.ResultFile('words', 'sentences_sentences'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'paragraph',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('doctextstyle', 'textstyle'),
            utila.ResultFile('magic', 'content_content'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'physical',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('magic', 'content_content'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'quotation',
        inputs=[
            utila.ResultFile('textflow', 'quotation_quotation'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'startend',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('magic', 'content_content'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'writing',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('words', 'sentences_sentences'),
            utila.ResultFile('groupme', 'pagenumbers_magic'),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    root, features = decider_textflow.ROOT, 'decider_textflow.features'
    hook = protocol.integrate(root=root, features=features)
    utila.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            name=decider_textflow.PROCESS,
            pages=True,
            version=decider_textflow.__version__,
        ),
    )
