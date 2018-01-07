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
from Autodesk.Revit.Exceptions import ArgumentException
from RevitServices.Persistence import DocumentManager
import Revit

from System.Collections.Generic import List
# https://msdn.microsoft.com/en-us/library/bb896387%28v=vs.110%29.aspx?f=255&MSPPError=-2147217396
from System import Type

clr.ImportExtensions(Revit.Elements)

doc                 = DocumentManager.Instance.CurrentDBDocument
uidoc               = DocumentManager.Instance.CurrentUIDocument

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


# -------------- Utilities ------------- #

class MyFailureHandler(IFailuresPreprocessor):
    def processFailures(failures_accessor):
        failuresAccessor.DeleteAllWarnings()

        return FailureProcessingResult.Continue

num_of_elements_before = FilteredElementCollector(doc).             \
                            OfClass(clr.GetClrType(TextElement)).   \
                            ToElementIds().                         \
                            Count

# -------------- Utilities ------------- #


view_multi_class_list = List[Type]()
view_multi_class_list.Add(clr.GetClrType(ViewDrafting))
view_multi_class_list.Add(clr.GetClrType(ViewPlan))
view_multi_class_list.Add(clr.GetClrType(ViewSection))

view_multi_class_filter = ElementMulticlassFilter(view_multi_class_list)

view_id_collector = FilteredElementCollector(doc).                  \
                    WherePasses(view_multi_class_filter).           \
                    ToElementIds()

text_note_collector = []
for view_id in view_id_collector:

    '''ArgumentException:
    viewId is not a view. -or- viewId is not valid for element iteration, 
    because it has no way of representing drawn elements. 
    Many view templates will fail this check.
    
    Probably because the Dynamo Script was catching Sections that 
    DON'T even exist, so I place it in a try-except instead
    '''

    # NOTE: ActiveView only works if you actually go inside the viewport
    # i.e., not just the sheet
    try:
        '''Toggle active view only
        and entire doc
        '''
        if active_view_only:
            inner_note_collector = FilteredElementCollector(doc, doc.ActiveView.Id) \
                                    .OfCategory(BuiltInCategory.OST_TextNotes)      \
                                    .ToElements()

            for inner_note in inner_note_collector:
                text_note_collector.append(inner_note)

            # stop outer iteration, i.e. you only need elements from ActiveView
            break

        else:
            inner_note_collector = FilteredElementCollector(doc, view_id)           \
                .OfCategory(BuiltInCategory.OST_TextNotes)                          \
                .ToElements()

            for inner_note in inner_note_collector:
                text_note_collector.append(inner_note)

    except ArgumentException:
        continue


if toggle is True:

    unchanged_text = []

    with Transaction(doc, 'Change Note Types DYNAMOREVAPI') as t:

        t.Start()
        # fail_opt = t.GetFailureHandlingOptions()
        # fail_opt.SetFailuresPreprocessor(MyFailureHandler())
        # t.SetFailureHandlingOptions(fail_opt)

        for text in text_note_collector:

            text_note_type = text.TextNoteType

            text_size = text_note_type.get_Parameter(BuiltInParameter.TEXT_SIZE).AsDouble()
            text_size = UnitUtils.ConvertFromInternalUnits(text_size,
                                                           DisplayUnitType.DUT_MILLIMETERS)

            type_list = IN[2:]

            # cancel if the TextNoteType is already ISOCPEUR AND if size within 0.1 - 4.3
            # if ((text_note_type == type_2 or text_note_type == type_3_5) and
            #         (0 <= text_size <= 4.2)):
            # TODO: not yet tested
            if (text_note_type in type_list) and (0 <= text_size <= 4.3):
                continue

            if 0.1 <= text_size <= 0.45:
                # change size to 0.25
                text.TextNoteType = type_0_25
                # unchanged_text.append([text, 'Change to 0.25 from {}'.format(text_size)])

            elif 0.45 < text_size <= 0.9:
                text.TextNoteType = type_0_5

            elif 0.9 < text_size <= 1.4:
                text.TextNoteType = type_1_0

            elif 1.4 < text_size <= 1.9:
                text.TextNoteType = type_1_5

            elif 1.9 < text_size <= 2.2:
                text.TextNoteType = type_2

            elif 2.2 < text_size <= 3.4:
                text.TextNoteType = type_2_3

            elif 3.4 < text_size <= 4.3:
                text.TextNoteType = type_3_5

            else:
                # append the UNchanged textNotes for viewing in Dynamo
                unchanged_text.append([text, 'Unchanged: probably too large, size={}'.format(text_size)])
                # symbols.append(text.Symbol)

        num_of_elements_after = FilteredElementCollector(doc).          \
                                OfClass(clr.GetClrType(TextElement)).   \
                                ToElementIds().                         \
                                Count

        # assert that num of TextNotes is the same before and after for entire doc
        if num_of_elements_before != num_of_elements_after:
            t.RollBack()
            OUT = 'Error Occurred, Some items were deleted'

        else:
            t.Commit()
            OUT = unchanged_text

        uidoc.RefreshActiveView()




# just display the TextNotes if toggle = False
elif toggle is False:
    OUT = [text.ToDSType(False) for text in text_note_collector]
    # OUT = text_note_collector.ToElementIds().Count
    uidoc.RefreshActiveView()
