#!/usr/bin/env python3
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

# ------------------ CAUTION! ------------------ #

# DO NOT RUN WHILE DYNAMO IS RUNNING ANY SCRIPT AND USING
# ANY OF THE FILES!! MAY CAUSE FILES TO BECOME CORRUPT!

# Can be used if Dynamo is IDLE

# ------------------ CAUTION! ------------------ #

# TODO: Make this a PyQT script???
# TODO: (include in PyQt but already start including even w/o):
# print out which files would be changed if files already exist, ask for
# user verification

# TODO: test modes 2,3 before merging the branch

import os
import shutil
import time
import ctypes.wintypes

__version__     = '0.0.1'
__py_version__  = 3.6

# TODO: Test dynamic
# -------- SET THIS FIRST --------
MOTHER_MODE = 4     # 1: Dynamic,
                    # 2: nodesrc [.py], core[.py] (static), (Github to Dynamo)
                    # 3: dyf, static (most common)
                    # 4: Only print out what the directories are
mode_1, mode_2, mode_3, mode_4 = False, False, False, False

if MOTHER_MODE == 1:
    mode_1 = True

elif MOTHER_MODE == 2:
    mode_2 = True

elif MOTHER_MODE == 3:
    mode_3 = True

else:
    mode_4 = True

APPDATA = os.environ['APPDATA']
# USER_PATH 	= os.path.expanduser('~')	# TODO: Test @ home where Documents is @ D:\
# NOTE: os.path.expanduser won't get your Documents location if it was changed, therefore:
# https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path

CSIDL_PERSONAL      = 5  # My Documents
SHGFP_TYPE_CURRENT  = 0  # Get current, not default value
buf                 = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

DOCUMENTS_DIR   = buf.value

GITHUB_DIR      = os.path.join(DOCUMENTS_DIR, r'GitHub\Faraday')
DYNAMO_DIR      = os.path.join(APPDATA, r'Dynamo\Dynamo Revit\1.3\packages\Faraday')

if not os.path.exists(DYNAMO_DIR):
    os.makedirs(DYNAMO_DIR)

_src = GITHUB_DIR if (mode_1 or mode_2) else DYNAMO_DIR
_dst = DYNAMO_DIR if (mode_1 or mode_2) else GITHUB_DIR


# _src = r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\Github\Faraday' if (mode_1 or mode_2) else \
#         r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\packages\Faraday'
# _dst = r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\packages\Faraday' if (mode_1 or mode_2) else \
#         r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\Github\Faraday'


def copy_files(src, dst, base_src, base_dst, file_xtnsn):
    """Copies files from Dynamo packages folder (e.g. Faraday)
    into the git folder for version control

    The typical workflow would be to edit the python code inside github
    run this script to copy the .py files to the package folder
    Then rebuild the dyf files in Dynamo
    Lastly, recopy the dyf files from Package folder to Github folder

    Mode 1:     Dynamic mode
                copy .py (Faraday/src to ~extra/nodesrc) files from Github
                including Faraday/faradaycore to ~extra/faradaycore

    Mode 2:     Static mode
                copy .py (Faraday/src to ~extra/nodesrc) files from Github
                including Faraday/faradaycore to ~extra/faradaycore

    Mode 3:     Always Static
                copy all DYFs from Packages/Farad/dyf to Github/Faraday/dyf
                DON'T USE THIS MODE WITH DYNAMIC UPDATE!

    Args:
        src:            Package source
        dst:            Github destination repo folder
        base_src:       The sub folder or `src` that actually holds the files
        base_dst:       The sub folder of `dst` that actually holds the files
        file_xtnsn:     *.py or *.dyf
        dynamic:        Script runs for 4 hours, automatically
                        checks if files have been modified

    Returns:
        copied_files:   (String) A list of copied files
    """

    assert os.path.isdir(src)
    assert os.path.isdir(dst)

    os.chdir(src)
    src_files = (f for f in os.listdir(base_src) if f.endswith(file_xtnsn))

    os.chdir(dst)
    if not os.path.exists(os.path.join(dst, base_dst_fldr)):
        os.makedirs(os.path.join(dst, base_dst_fldr))
    # list -> so you can use 'in', because not available for tuples
    dst_files = list(f for f in os.listdir(base_dst_fldr) if f.endswith(file_xtnsn))

    copied_files = []

    for f in src_files:
        src_file_path = os.path.join(src, f'{base_src}/{f}')
        dst_path = os.path.join(dst, base_dst)

        # if file already exists at dst, compute modf time
        if f in dst_files:
            src_modf_time = os.path.getmtime(src_file_path)

            # lookup the same f name in dst_files
            dst_f = dst_files[list(dst_files).index(f)]
            dst_modf_time = os.path.getmtime(os.path.join(dst_path, dst_f))

            if src_modf_time > dst_modf_time:
                copied_file = shutil.copy2(src_file_path,
                                           dst_path)

                copied_files.append(os.path.basename(copied_file))

        elif f not in dst_files:
            copied_file = shutil.copy2(src_file_path,
                                       dst_path)

            copied_files.append(os.path.basename(copied_file))

    if _nodesrc:
        str_mode = 'nodesrc'

    elif _faradcore:
        str_mode = 'faradcore'

    else:
        str_mode = 'dyf'

    print(f'copied files in mode {str_mode}: {copied_files}')


if __name__ == '__main__':
    """Script will run for a max time for 4 hrs, then will automatically
    kill itself
    
    Script copies changed files (depending on the direction specified)
    every 20 seconds
    """

    mode_paths_dict =   {
        'dyf':      {
                        'base_src_fldr':    r'dyf',
                        'base_dst_fldr':    r'dyf',
                        'file_extn':        r'.dyf'
                    },

        'nodesrc':  {
                        'base_src_fldr':    r'src',
                        'base_dst_fldr':    r'extra\nodesrc',
                        'file_extn':        r'.py'
                     },

        'faradcore': {
                        'base_src_fldr':    r'faradaycore',
                        'base_dst_fldr':    r'extra\faradaycore',
                        'file_extn':        r'.py'
                    }
         }


    _dyf        = True if mode_3 else False
    _nodesrc    = False if mode_3 else True
    _faradcore  = False if mode_3 else True
    _dynamic    = True if mode_1 else False

    # -----------------------
    first_called = time.time()

    if mode_4:
        assert os.path.isdir(_src)
        assert os.path.isdir(_dst)
        print(f'src = {_src}, dst = {_dst}')

    else:
        while True:
            if _nodesrc:

                mode            = mode_paths_dict['nodesrc']

                base_src_fldr   = mode['base_src_fldr']
                base_dst_fldr   = mode['base_dst_fldr']
                file_xtn        = mode['file_extn']

                copy_files(src=_src,
                           dst=_dst,
                           base_src=base_src_fldr,
                           base_dst=base_dst_fldr,
                           file_xtnsn=file_xtn)

            if _faradcore:
                mode            = mode_paths_dict['faradcore']

                base_src_fldr   = mode['base_src_fldr']
                base_dst_fldr   = mode['base_dst_fldr']
                file_xtn        = mode['file_extn']

                copy_files(src=_src,
                           dst=_dst,
                           base_src=base_src_fldr,
                           base_dst=base_dst_fldr,
                           file_xtnsn=file_xtn)

            if _dyf:
                mode            = mode_paths_dict['dyf']

                base_src_fldr   = mode['base_src_fldr']
                base_dst_fldr   = mode['base_dst_fldr']
                file_xtn        = mode['file_extn']

                copy_files(src=_src,
                           dst=_dst,
                           base_src=base_src_fldr,
                           base_dst=base_dst_fldr,
                           file_xtnsn=file_xtn)


            if not _dynamic:
                break

            time.sleep(20)
            last_called = time.time()

            if last_called - first_called >= 14400:
                break
