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