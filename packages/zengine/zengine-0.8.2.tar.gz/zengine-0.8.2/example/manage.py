# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from zengine.management_commands import *
environ['PYOKO_SETTINGS'] = 'example.settings'
if __name__ == '__main__':
    ManagementCommands()
