import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitNodes')
import Revit

clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument

# True = change types, False = view
toggle = bool(IN[0])

# toggle: active view only
active_view_only = bool(IN[1])

# 0.25mm ISO
type_0_25 = UnwrapElement(IN[2])

# 0.5mm ISO
type_0_5 = UnwrapElement(IN[3])

# 1.0mm ISO
type_1_0 = UnwrapElement(IN[4])

# 1.5mm ISO
type_1_5 = UnwrapElement(IN[5])

# 2.0mm ISO
type_2 = UnwrapElement(IN[6])

# 2.3mm ISO (from 2.5)
type_2_3 = UnwrapElement(IN[7])

# 3.5mm ISO (from 4.0)
type_3_5 = UnwrapElement(IN[8])


# -------------- Utilities ------------- #


# NOTE: ActiveView only works if you actually go inside the view?
# not just the sheet?
def view_toggle():
    """if True: run only for active view, False: entire doc"""
    return FilteredElementCollector(doc, doc.ActiveView.Id)     \
        if active_view_only is True                             \
        else FilteredElementCollector(doc)


class MyFailureHandler(IFailuresPreprocessor):
    def processFailures(failures_accessor):
        # doc = failures_accessor.GetDocument()
        failuresAccessor.DeleteAllWarnings()

        return FailureProcessingResult.Continue


# -------------- Utilities ------------- #


# -------------- To Do List  ------------- #

# TODO: Check the API for methods for going inside vieports of ViewSheets
# class: ViewSheet
# or use a FilteredElementCollector().OfClass(Viewport)

# idea:
# for viewport in viewport_collector:
# 	FilteredElementCOllector(doc, viewport.Id) would return the elements inside

# -------------- To Do List  ------------- #

# limit to active view first
# TODO: VERY IMPORTANT: LIMIT ONLY TO VIEWS which are not sheets

text_note_collector = view_toggle(). \
    OfCategory(BuiltInCategory.OST_TextNotes)

if toggle is True:

    unchanged_text = []

    num_of_elements_before = view_toggle().     \
        OfClass(clr.GetClrType(TextElement)).   \
        ToElementIds().                         \
        Count

    with Transaction(doc, 'Change Note Types DYNAMOREVAPI') as t:

        t.Start()
        # fail_opt = t.GetFailureHandlingOptions()
        # fail_opt.SetFailuresPreprocessor(MyFailureHandler())
        # t.SetFailureHandlingOptions(fail_opt)

        for text in text_note_collector:

            text_note_type = text.TextNoteType
            text_size_param = BuiltInParameter.TEXT_SIZE

            text_size = text_note_type.get_Parameter(text_size_param).AsDouble()
            text_size = UnitUtils.ConvertFromInternalUnits(text_size,
                                                           DisplayUnitType.DUT_MILLIMETERS)

            # cancel if the TextNoteType is already ISOCPEUR AND if size within 0.1 - 4.2
            if ((text_note_type == type_2 or text_note_type == type_3_5) and
                    (0 <= text_size <= 4.2)):
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




# just display the TextNotes if toggle = False
elif toggle is False:
    OUT = [text.ToDSType(False) for text in text_note_collector]
    # OUT = text_note_collector.ToElementIds().Count
