# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""Patterned after Mostapha's genDynamoPackage.py
https://github.com/ladybug-tools/ladybug-dynamo/
blob/master/resources/createpackage/genDynamoPackage.py"""

# TODO: not yet tested

import json
import os


__version__     = '0.0.1'
__py_version__  = 3.6


# definitions_path = path to dyf files
def create_pkg(definitions_path):
    faraday_data = {
                    'license':              'GPL-3.0',
                    'file_hash':            None,
                    'name':                 'Faraday',
                    'version':              '0.0.1',
                    'description':          'Collection of my Dynamo Scripts',
                    'group':                '',
                    'keywords':             ['faraday'],
                    'contents':             '',
                    'engine_version':       '1.3.1.1736',
                    'engine':               'dynamo',
                    'engine_metadata':      '',
                    'site_url':             'https://github.com/SpencerMAQ/Faraday',
                    'repository_url':       'https://github.com/SpencerMAQ/Faraday',
                    'contains_binaries':    False,
                    'node_libraries':       []
                    }
    contents = []
    # definition pattern:
    # " name - description" separated by ,"

    # return all files and folders (relative path as STRINGS)
    files = os.listdir(definitions_path)

    for f in files:
        #
        _fullpath = os.path.join(definitions_path, f)

        if not os.path.isfile(_fullpath):
            continue

        with open(_fullpath, 'r') as dyf:
            line = dyf.readline()       # only read the header

            # parse xml, 1:-1 removes the "" parentheses from the XML using list slicing
            # apparently, strip(") might also work?
            name        = line.split('Name=')[-1].split('Description')[0].strip().strip('"')
            description = line.split('Description=')[-1].split('ID')[0].strip().strip('"')
            contents.append(" " + name + " - " + description)

    faraday_data['contents'] = ",".join(contents)

    # os.path.dirname = gets parent directory where the JSON should be
    with open(os.path.join(os.path.dirname(definitions_path), 'pkg.json'), 'w') as pkg:
        json.dump(faraday_data,
                  pkg,
                  indent=4,
                  separators=(',', ': ')
                  )

if __name__ == '__main__':
    test_path = r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\packages\Faraday\dyf'
    # test_path   = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\definitions'
    # test_path2  = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\backup'
    # actual_path = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Faraday\dyf'

    create_pkg(test_path)