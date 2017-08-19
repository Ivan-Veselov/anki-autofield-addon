from anki.hooks import addHook
from aqt import mw

gSourceFieldName = "Example [source]"
gOpenedFieldName = "Example [opened]"
gClozeFieldName = "Example [cloze]"

def onEditorFocusLost(aFlag, aNote, aFieldIndex):
    fieldNames = mw.col.models.fieldNames(aNote.model())
    
    if fieldNames[aFieldIndex] != gSourceFieldName:
        return aFlag

    if gOpenedFieldName in fieldNames:
        aNote[gOpenedFieldName] = aNote[gSourceFieldName]
        aFlag = True

    if gClozeFieldName in fieldNames:
        aNote[gClozeFieldName] = aNote[gSourceFieldName]
        aFlag = True
    
    return aFlag

addHook('editFocusLost', onEditorFocusLost)
