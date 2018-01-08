# Faraday: A Dynamo Plugin (GPL) started by Michael Spencer Quinto
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""Changes the TextNoteTypes of all TextNotes inside the document
provided that the TextNotes are inside any of the following View Classes:
    ViewDrafting
    ViewPlan
    ViewSection
    Args:
        _run:           (bool) True to change the Note Types,
                        False to simply view the items
        _active_or_doc: (bool) True to change only for the active view,
                        False to change for entire doc
        _type1:         (TextNoteType) first basis, i.e. other note types
                        will be changed to this
    Returns:
        OUT:            if _run = True, all unchanged TextNotes with their Id
                        if _run = False, all TextNotes inside the doc
"""

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference('RevitNodes')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
import Revit

clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument

# True = change types, False = view
toggle              = bool(IN[0])

# toggle: active view only
active_view_only    = bool(IN[1])

# 0.25mm ISO
type_0_25           = UnwrapElement(IN[2])

# 0.5mm ISO
type_0_5            = UnwrapElement(IN[3])

# 1.0mm ISO
type_1_0            = UnwrapElement(IN[4])

# 1.5mm ISO
type_1_5            = UnwrapElement(IN[5])

# 2.0mm ISO
type_2              = UnwrapElement(IN[6])

# 2.3mm ISO (from 2.5)
type_2_3            = UnwrapElement(IN[7])

# 3.5mm ISO (from 4.0)
type_3_5            = UnwrapElement(IN[8])

# -------------- Bold Types ------------- #

type_0_25_b         = UnwrapElement(IN[9])
type_0_5_b          = UnwrapElement(IN[10])
type_1_0_b          = UnwrapElement(IN[11])
type_1_5_b          = UnwrapElement(IN[12])
type_2_b            = UnwrapElement(IN[13])
type_2_3_b          = UnwrapElement(IN[14])
type_3_5_b          = UnwrapElement(IN[15])


# -------------- Bold Types ------------- #


# -------------- Utilities ------------- #


# NOTE: ActiveView only works if you actually go inside the viewport
# i.e., not just the sheet
def view_toggle():
    """if True: run only for active view, False: entire doc"""

    # FilteredElementCollector also takes in ICollection of ElementIds
    return FilteredElementCollector(doc, doc.ActiveView.Id)     \
        if active_view_only is True                             \
        else FilteredElementCollector(doc)


class MyFailureHandler(IFailuresPreprocessor):
    def processFailures(failures_accessor):
        failuresAccessor.DeleteAllWarnings()

        return FailureProcessingResult.Continue


# -------------- Utilities ------------- #


# -------------- Road map  ------------- #

"""
2018_01_008 - CHANGE TEXT EVEN IF YOU ARE AT VIEWHSEET LEVEL
I.E. GET ALL VIEWPORTS AND ALL ELEMENTS INSIDE VIEWPORTS

fOR vIEW ELEMENTS MODE - SHOW ALL THE FONTS

SHOW NOTIFICATIONS FOR CHANGED TEXT
	> FROM WHAT TO WHAT (SIZE, FONT)
	> NUMBER OF CHANGED TEXT, UNCHANGED TEXT
"""

# TODO: (long-term): make the inputs more dynamo, (probably using exec)

# -------------- Road map  ------------- #


text_note_collector = view_toggle().\
                        OfCategory(BuiltInCategory.OST_TextNotes)


if toggle is True:

    unchanged_text = []

    num_of_elements_before = view_toggle().                             \
                                OfClass(clr.GetClrType(TextElement)).   \
                                ToElementIds().                         \
                                Count

    with Transaction(doc, 'Change Note Types DYNAMOREVAPI') as t:

        t.Start()

        for text in text_note_collector:

            text_note_type = text.TextNoteType
            text_size_param = BuiltInParameter.TEXT_SIZE

            text_size = text_note_type.get_Parameter(text_size_param).AsDouble()
            text_size = UnitUtils.ConvertFromInternalUnits(text_size,
                                                           DisplayUnitType.DUT_MILLIMETERS)
            text_bold_param_original = text_note_type \
                                        .get_Parameter(BuiltInParameter.TEXT_STYLE_BOLD) \
                                        .AsInteger()
            type_list = IN[2:]
            text_note_font = text_note_type.get_Parameter(BuiltInParameter.TEXT_FONT).AsString()

            # cancel if the TextNoteType is already ISOCPEUR AND if size within 0.1 - 4.3
            if ('ISOCPEUR' in text_note_font) and (0 <= text_size <= 4.3):
                unchanged_text.append('Text is already ISOCPEUR')
                continue

            if 0.1 <= text_size <= 0.45:
                # change size to 0.25
                if not text_bold_param_original:
                    text.TextNoteType = type_0_25
                elif text_bold_param_original:
                    text.TextNoteType = type_0_25_b

            elif 0.45 < text_size <= 0.9:
                if not text_bold_param_original:
                    text.TextNoteType = type_0_5
                elif text_bold_param_original:
                    text.TextNoteType = type_0_5_b


            elif 0.9 < text_size <= 1.4:
                if not text_bold_param_original:
                    text.TextNoteType = type_1_0
                elif text_bold_param_original:
                    text.TextNoteType = type_1_5_b

            elif 1.4 < text_size <= 1.9:
                if not text_bold_param_original:
                    text.TextNoteType = type_1_5
                elif text_bold_param_original:
                    text.TextNoteType = type_1_5_b

            elif 1.9 < text_size <= 2.2:
                if not text_bold_param_original:
                    text.TextNoteType = type_2
                elif text_bold_param_original:
                    text.TextNoteType = type_2_b

            elif 2.2 < text_size <= 3.4:
                if not text_bold_param_original:
                    text.TextNoteType = type_2_3
                elif text_bold_param_original:
                    text.TextNoteType = type_2_3_b


            elif 3.4 < text_size <= 4.3:
                if not text_bold_param_original:
                    text.TextNoteType = type_3_5
                elif text_bold_param_original:
                    text.TextNoteType = type_3_5_b

            else:
                unchanged_text.append([text, 'Unchanged: probably too large, size={}'.format(text_size)])
                # symbols.append(text.Symbol)

        num_of_elements_after = view_toggle().                          \
                                OfClass(clr.GetClrType(TextElement)).   \
                                ToElementIds().                         \
                                Count

        # assert that num of TextNotes is the same before and after
        if num_of_elements_before != num_of_elements_after:
            t.RollBack()
            OUT = 'Error Occurred, Some items were deleted'
            uidoc.RefreshActiveView()

        else:
            t.Commit()
            OUT = unchanged_text
            uidoc.RefreshActiveView()

# Note to self: ToDSType may be causing accidental deletion of the Texts
# because maybe they're 'OWNBED by Dynamo????' (not really sure)
elif toggle is False:
    OUT = text_note_collector
