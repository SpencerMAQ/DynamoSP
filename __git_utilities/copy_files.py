# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""Patterned after Mostapha's copy_files.py
https://github.com/ladybug-tools/ladybug-dynamo/
blob/master/plugin/copy_files.py

# TODO: reverse the flow because Mostapha works from Github
# to the Dynamo PKG folder, I'll do the opposite

# TODO: Find out what happens if a file already exists,
# i.e. is it copied then replaced?
"""

import os
import shutil


def copy_files(src, dst, dyf=True, nodesrc=True, hbsrc=True):
    """Copies files from Dynamo packages folder (e.g. Faraday)
    into the git folder for version control

    Args:
        src:        Package source
        dst:        Github destination repo folder
        dyf:        True to copy dyf files
        nodesrc:    copy files from Dynamo's extra folder to 'src'
        hbsrc:      ladybug source dode
    """
    assert os.path.isdir(src)
    assert os.path.isdir(dst)

    os.chdir(src)

    # copy definitions
    if dyf:
        dyfs = (f for f in os.listdir(r'plugin\dyf'))

if __name__ == '__main__':
    _src = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Faraday'
    _dst = r'D:\Libraries\Documents\GitHub\Faraday'

    copy_files(_src, _dst)