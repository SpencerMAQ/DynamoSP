# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

# py 3.6

# --------- CAUTION! -------- #

# DO NOT RUN WHILE DYNAMO IS RUNNING ANY SCRIPT AND USING
# ANY OF THE FILES!! MAY CAUSE FILES TO BECOME CORRUPT!

# Can be used if Dynamo is IDLE

# --------- CAUTION! -------- #


"""Patterned after Mostapha's copy_files.py
https://github.com/ladybug-tools/ladybug-dynamo/
blob/master/plugin/copy_files.py

# TODO: reverse the flow because Mostapha works from Github
# to the Dynamo PKG folder, I'll do the opposite (do this some time in the future)

# TODO (interesting)
# use this library instead (https://pypi.python.org/pypi/watchdog/0.5.4)
# to detect file changes, then run code as needed
# https://stackoverflow.com/questions/5738442/detect-file-change-without-polling
# or get the last modified time instead, use that to know if to replace file or not
# https://stackoverflow.com/questions/375154/how-do-i-get-the-time-a-file-was-last-modified-in-python

# TODO: Find out what happens if a file already exists,
# i.e. is it copied then replaced?
"""

import os
import shutil
import time


def copy_files(src, dst, dyf=False, nodesrc=True, hbsrc=True, dynamic=False):
    """Copies files from Dynamo packages folder (e.g. Faraday)
    into the git folder for version control

    The typical workflow would be to edit the python code inside github
    run this script to copy the .py files to the package folder
    Then rebuild the dyf files in Dynamo
    Lastly, recopy the dyf files from Package folder to Github folder

    Mode 1:     copy .py files from Github

    Args:
        src:        Package source
        dst:        Github destination repo folder
        dyf:        True to copy dyf files
        nodesrc:    copy files from Dynamo's extra folder to 'src'
        hbsrc:      ladybug source dode
        dynamic:    Script runs for 4 hours, automatically
                    checks if files have been modified
    """
    assert os.path.isdir(src)
    assert os.path.isdir(dst)

    os.chdir(src)

    # copy definitions from Dynamo to Github
    if dyf:
        src_dyfs = (f for f in os.listdir(r'dyf') if f.endswith('.dyf'))
        os.chdir(dst)
        dst_dyfs = (f for f in os.listdir(r'dyf') if f.endswith('.dyf'))
        for f in src_dyfs:
            # equal filenames
            if f in dst_dyfs:
                src_dyf_modf_time = os.path.getmtime(f)
                # lookup the same f name in dst_dyfs
                dest_f = dst_dyfs[list(dst_dyfs).index(f)]
                dst_dyf_modf_time = os.path.getmtime(dest_f)

                if src_dyf_modf_time > dst_dyf_modf_time:
                    shutil.copyfile(
                                    os.path.join(src, r'dyf\{}'.format(f)),
                                    os.path.join(dst, r'dyf')
                                    )
                    
            elif f not in dst_dyfs:
                shutil.copyfile(
                                os.path.join(src, r'dyf\{}'.format(f)),
                                os.path.join(dst, r'dyf')
                                )


    # direct way of checking if file was modified: os.path.getmtime

if __name__ == '__main__':
    """Script will run for a max time for 4 hrs, then will automatically
    kill itself
    
    Script copies changed files (depending on the direction specified)
    every 20 seconds
    """

    _src = r'D:\Libraries\Documents\GitHub\Faraday'
    _dst = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Faraday'

    first_called = time.time()
    while True:
        copy_files(_src, _dst)
        time.sleep(20)
        last_called = time.time()

        if last_called - first_called == 14400:
            break
