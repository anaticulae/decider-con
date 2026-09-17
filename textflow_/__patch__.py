# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

TEXTUAL = {
    # iamraw.PageContentType.CAPTION,
    # iamraw.PageContentType.TABLE,
    iamraw.PageContentType.BLOCKQUOTE,
    iamraw.PageContentType.FORMULA,
    iamraw.PageContentType.LIST,
    iamraw.PageContentType.TEXT,
}

iamraw.TEXTUAL = TEXTUAL
