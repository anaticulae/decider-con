# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import protocol
import utila


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
