# Faraday: A Dynamo Plugin (GPL) started by Michael Spencer Quinto
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitNodes')
clr.AddReference('RevitServices')
clr.AddReference('System.Core')

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
import Revit
import System

from RevitServices.Persistence import DocumentManager

doc     = DocumentManager.Instance.CurrentDBDocument
uidoc   = DocumentManager.Instance.CurrentUIDocument

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(System.Linq)


class Transaction:
    """Automatically wraps Transactions in
    t.Start() and t.Commit(), and automates
    t.Rollback() on exceptions

    Args:
        _doc = Revit Document
        name = Transaction name
    """
    def __init__(self, _doc=None, name=''):
        self.transaction = DB.Transaction(_doc, name)

    def __enter__(self):
        self.transaction.Start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.transaction.RollBack()
        else:
            self.transaction.Commit()