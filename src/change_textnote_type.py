# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""Changes the TextNoteTypes of all TextNotes inside a VIEWSHEET
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
# TODO: create script that automatically copies files from Dynamo Folder
# to Git folder
# TODO: use scripts from utils

# from api_utils import *
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference('RevitNodes')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
import Revit

clr.ImportExtensions(Revit.Elements)

doc                 = DocumentManager.Instance.CurrentDBDocument
uidoc               = DocumentManager.Instance.CurrentUIDocument


toggle              = bool(IN[0])           # True = change types, False = view

active_view_only    = bool(IN[1])           # toggle: active view only

type_0_25           = UnwrapElement(IN[2])  # 0.25mm ISO
type_0_5            = UnwrapElement(IN[3])
type_1_0            = UnwrapElement(IN[4])
type_1_5            = UnwrapElement(IN[5])
type_2_0            = UnwrapElement(IN[6])
type_2_3            = UnwrapElement(IN[7])
type_3_5            = UnwrapElement(IN[8])

# -------------- Bold Types ------------- #

type_0_25_b         = UnwrapElement(IN[9])
type_0_5_b          = UnwrapElement(IN[10])
type_1_0_b          = UnwrapElement(IN[11])
type_1_5_b          = UnwrapElement(IN[12])
type_2_0_b          = UnwrapElement(IN[13])
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


SHOW NOTIFICATIONS FOR CHANGED TEXT
	> FROM WHAT TO WHAT (SIZE, FONT)
	> NUMBER OF CHANGED TEXT, UNCHANGED TEXT
"""

# TODO: (long-term): make the inputs more dynamo, (probably using exec)

# -------------- Road map  ------------- #

# -------------- Experimental  ------------- #
viewport_collector = view_toggle().OfCategory(BuiltInCategory.OST_Sheets).ToElementIds()

view_sheet_note_collector = view_toggle().OfCategory(BuiltInCategory.OST_TextNotes)

text_note_collector = []
for viewport in viewport_collector:



    inner_note_collector = FilteredElementCollector(doc, viewport.Id)       \
                                .OfCategory(BuiltInCategory.OST_TextNotes)
    for inner_note in inner_note_collector:
        text_note_collector.append(inner_note)


# text_note_collector = view_toggle().\
#                         OfCategory(BuiltInCategory.OST_TextNotes)

# -------------- Experimental  ------------- #

if toggle is True:

    unchanged_text = []

    num_of_elements_before = view_toggle().                             \
                                OfClass(clr.GetClrType(TextElement)).   \
                                ToElementIds().                         \
                                Count

    with Transaction(doc, 'FARADAY: Change Note Types DYNAMOREVAPI') as t:

        t.Start()

        for text in text_note_collector:

            text_note_type = text.TextNoteType

            text_size = text_note_type.get_Parameter(BuiltInParameter.TEXT_SIZE).AsDouble()
            text_size = UnitUtils.ConvertFromInternalUnits(text_size,
                                                           DisplayUnitType.DUT_MILLIMETERS)
            text_bold_param_original = text_note_type                                       \
                                        .get_Parameter(BuiltInParameter.TEXT_STYLE_BOLD)    \
                                        .AsInteger()
            type_list = IN[2:]
            text_note_font = text_note_type.get_Parameter(BuiltInParameter.TEXT_FONT).AsString()

            if ('ISOCPEUR' in text_note_font) and (0 <= text_size <= 4.3):
                unchanged_text.append('Text is already ISOCPEUR')
                continue

            if 0.1 <= text_size <= 0.45:
                # change size to 0.25
                if not text_bold_param_original:
                    text.TextNoteType = type_0_25
                elif text_bold_param_original:
                    text.TextNoteType = type_0_25_b
                # big problem with text_note_type.Name, apparently, can't access name in RevAPI
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )

            elif 0.45 < text_size <= 0.9:
                if not text_bold_param_original:
                    text.TextNoteType = type_0_5
                elif text_bold_param_original:
                    text.TextNoteType = type_0_5_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )


            elif 0.9 < text_size <= 1.4:
                if not text_bold_param_original:
                    text.TextNoteType = type_1_0
                elif text_bold_param_original:
                    text.TextNoteType = type_1_5_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )

            elif 1.4 < text_size <= 1.9:
                if not text_bold_param_original:
                    text.TextNoteType = type_1_5
                elif text_bold_param_original:
                    text.TextNoteType = type_1_5_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )

            elif 1.9 < text_size <= 2.2:
                if not text_bold_param_original:
                    text.TextNoteType = type_2_0
                elif text_bold_param_original:
                    text.TextNoteType = type_2_0_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )

            elif 2.2 < text_size <= 3.4:
                if not text_bold_param_original:
                    text.TextNoteType = type_2_3
                elif text_bold_param_original:
                    text.TextNoteType = type_2_3_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )


            elif 3.4 < text_size <= 4.3:
                if not text_bold_param_original:
                    text.TextNoteType = type_3_5
                elif text_bold_param_original:
                    text.TextNoteType = type_3_5_b
                unchanged_text.append(
                    'Size {} to 0.25 | From type {} to {}'.format(text_size,
                                                                  text_note_type,
                                                                  text.TextNoteType)
                )

            else:
                unchanged_text.append(
                    [text, 'Unchanged: probably too large, size={}'.format(text_size)]
                )

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
# Dynamo CALLS THIS A NEW TRANSACTION???!!

elif toggle is False:
    text_info_collector = []
    for text in text_note_collector:
        text_note_type = text.TextNoteType

        text_size = text_note_type.get_Parameter(BuiltInParameter.TEXT_SIZE).AsDouble()
        text_size = UnitUtils.ConvertFromInternalUnits(text_size,
                                                       DisplayUnitType.DUT_MILLIMETERS)

        text_note_font = text_note_type.get_Parameter(BuiltInParameter.TEXT_FONT).AsString()

        text_info_collector.append(
            'Id: {}, Size: {}, Font: {}'.format(text.Id,
                                                text_size,
                                                text_note_font)
        )

    OUT = text_info_collector
