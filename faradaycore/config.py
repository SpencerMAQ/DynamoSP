# Faraday: A Dynamo Plugin (GPL) started by Michael Spencer Quinto
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""Opens a PyQt form to configure
Faraday Preferences
"""


import json

def read_preferences():
    with open('faraday_pref.json', 'r') as fh:
        conf = json.loads()