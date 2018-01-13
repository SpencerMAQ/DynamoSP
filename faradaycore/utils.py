# Faraday: A Dynamo Plugin (GPL) started by Michael Spencer Quinto
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

PIPE = subprocess.PIPE

'''
# TODO: create utilities for calling
Python 3 code (e.g. PyQt)
'''


def run_python_3(command, stdin=None,
                 stdout=PIPE, stderr=None,
                 shell=False):
    """Runs python 3 strings, e.g. PyQt5
    using subprocess.
    By default, stdout=PIPE, i.e. returns the output
    """
    py3 = subprocess.Popen(command,stdin=stdin,stdout=stdout,stderr=stderr,shell=shell)
    py3.communicate()
