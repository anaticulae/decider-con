# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import textflow_

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'abbrev',
        [
            utilo.ResultFile('reftable', 'abbrev_abbrev'),
            utilo.ResultFile('words', 'abbreviation_detected'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'character',
        inputs=[
            utilo.ResultFile('words', 'sentences_sentences'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'docref',
        inputs=[
            utilo.ResultFile('docref', 'figure_parsed'),
            utilo.ResultFile('docref', 'section_parsed'),
            utilo.ResultFile('docref', 'table_parsed'),
            utilo.ResultFile('caption', 'image_caption'),
            utilo.ResultFile('caption', 'table_caption'),
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('headlines', 'result_result'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'lineending',
        inputs=[
            utilo.ResultFile('textflow', 'lineending_lastchar'),
            utilo.ResultFile('words', 'sentences_sentences'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'paragraph',
        inputs=[
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('doctextstyle', 'textstyle'),
            utilo.ResultFile('magic', 'content_content'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'physical',
        inputs=[
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('magic', 'content_content'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'quotation',
        inputs=[
            utilo.ResultFile('textflow', 'quotation_quotation'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'startend',
        inputs=[
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('magic', 'content_content'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'writing',
        inputs=[
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('groupme', 'pagenumbers_magic'),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    root, features = textflow_.ROOT, 'textflow_.features'
    hook = protoerror.integrate(
        root=root,
        features=features,
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            name=textflow_.PROCESS,
            pages=True,
            version=textflow_.__version__,
        ),
    )
