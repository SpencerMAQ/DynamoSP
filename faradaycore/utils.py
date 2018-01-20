# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
# TODO:
Logging utils
timer for how long a function takes
subprocess.Popen
os.path.join
"""

import logging
import os
import sys
import subprocess

from uuid import uuid4
from functools import wraps
from time import time

from api_utils import doc, DB

PIPE = subprocess.PIPE

'''
# TODO: create utilities for calling
Python 3 code (e.g. PyQt)
'''


# patterned from ladybug-tools: dynosaur
def unit_conversion():
    """Convert RevitAPI units (typically feet) to Project units
    (typically mm)"""
    doc_units   = doc.GetUnits()
    length_unit = doc_units.GetFormatOptions(DB.UnitType.UT_Length).DisplayUnits

    return DB.UnitUtils.ConvertFromInternalUnits(1.0, length_unit)


def run_python_3(command='py', stdin=None,
                 stdout=PIPE, stderr=None,
                 shell=False):
    """Runs python 3 strings, e.g. PyQt5
    using subprocess.
    By default, stdout=PIPE, i.e. returns the output
    """
    # TODO: use this instead
    # https://stackoverflow.com/questions/17665124/call-python3-code-from-python2-code
    # idea: open a temp file for writing, save as .py, execute the code in Popen, delete the file, use uuid
    # to ensure no conflicts with other filenames

    # get shortened version
    __temp_py_filename = str(uuid4()).split('-')[0]

    # py3 = subprocess.Popen(command,stdin=stdin,stdout=stdout,stderr=stderr,shell=shell)
    py3 = subprocess.Popen('py')
    # return py3.communicate()
