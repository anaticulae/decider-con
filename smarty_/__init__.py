# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

import decider_con
import smarty_.path

ROOT = decider_con.ROOT

__version__ = decider_con.__version__

PACKAGE = 'smarty_'
PROCESS = 'smarty_'

configos.cloud_lookup(PROCESS)
