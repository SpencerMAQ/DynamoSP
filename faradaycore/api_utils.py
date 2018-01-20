# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
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
clr.AddReference('ProtoGeometry')
clr.AddReference('DSCoreNodes')

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
import Revit as Revit
import System as System
import Autodesk.DesignScript.Geometry as GEO
import DSCore as DSCore

from RevitServices.Persistence import DocumentManager as DM
from RevitServices.Transactions import TransactionManager as TM

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(System.Linq)

doc     = DM.Instance.CurrentDBDocument
uiapp   = DM.Instance.CurrentUIApplication
app     = uiapp.Application
uidoc   = DM.Instance.CurrentUIDocument

class Transaction:
    """Automatically wraps Transactions in
    t.Start() and t.Commit(), and automates
    t.Rollback() on exceptions

    Args:
        _doc        = Revit Document
        name        = Transaction name
        production  = (boolean) [default = True] used for debugging purposes,
                        if set to True, will always do Rollback(), i.e. production code
                        if set to False, Rollback() will not be called
    """
    def __init__(self,
                 __doc=doc,
                 name='',
                 production=True):
        if not name:
            raise ValueError('Please provide a transaction name')
        self.transaction = DB.Transaction(__doc, name)
        self.production = production

    def __enter__(self):
        self.transaction.Start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.production and exc_type:
            self.transaction.RollBack()
        else:
            self.transaction.Commit()
