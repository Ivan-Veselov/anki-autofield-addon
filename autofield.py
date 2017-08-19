import re

from anki.hooks import addHook
from aqt import mw

gSourceFieldName = "Example [source]"
gOpenedFieldName = "Example [opened]"
gClozeFieldName = "Example [cloze]"

gSyntaxPattetn = r'\[\[(.*?)\]\]'

def onEditorFocusLost(aFlag, aNote, aFieldIndex):
    fieldNames = mw.col.models.fieldNames(aNote.model())
    
    if fieldNames[aFieldIndex] != gSourceFieldName:
        return aFlag

    if gOpenedFieldName in fieldNames:
        aNote[gOpenedFieldName] = re.sub(gSyntaxPattetn,
                                        r'<font color="#0000ff"><b>\1</b></font>',
                                        aNote[gSourceFieldName])
        aFlag = True

    if gClozeFieldName in fieldNames:
        aNote[gClozeFieldName] = re.sub(gSyntaxPattetn,
                                        r'<font color="#0000ff"><b>[...]</b></font>',
                                        aNote[gSourceFieldName])
        aFlag = True
    
    return aFlag

addHook('editFocusLost', onEditorFocusLost)
