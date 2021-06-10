# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import itertools
import os
import sys

import protocol
import utila


def document() -> protocol.Document:
    documents = selected()
    result = load_document(documents)
    return result


def selected() -> list:
    argv = sys.argv
    inputs = []
    for cmd, parameter in itertools.zip_longest(argv, argv[1:]):
        # TODO: REPLACE WITH PYTHON
        if cmd.startswith('-i='):
            splitted = cmd.split('-i=')
            inputs.append(splitted[1])
            continue
        if cmd.startswith('--input='):
            splitted = cmd.split('--input=')
            inputs.append(splitted[1])
            continue
        if cmd not in ('-i', '--input'):
            continue
        inputs.append(parameter)
    if not inputs:
        inputs = [os.getcwd()]
    return inputs


def load_document(inpaths) -> protocol.Document:
    inpaths = [inpaths] if isinstance(inpaths, str) else inpaths
    for path in inpaths:
        path = os.path.join(path, 'pdfinfo.yaml')
        if not os.path.exists(path):
            continue
        loaded = utila.yaml_from_raw_or_path(path)
        result = protocol.Document(pages=int(loaded['pages']),)
        return result
    return None
