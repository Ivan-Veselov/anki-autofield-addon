import sys # for debug purpose
import re

from aqt.qt import *

from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor
from anki.hooks import wrap

gSourceFieldSuffix = "[source]"
gOpenedFieldSuffix = "[opened]"
gClozeFieldSuffix = "[cloze]"

gSyntaxPattetn = r'\[\[(.*?)\]\]'

gShortcutKey = "F12"

def updateDstField(aNote, aSourceFieldValue, aFieldName, aReplacement):
    if not aFieldName in mw.col.models.fieldNames(aNote.model()):
        return False
    
    newValue = re.sub(gSyntaxPattetn,
                      r'<font color="#0000ff"><b>' + aReplacement + r'</b></font>',
                      aSourceFieldValue)

    result = aNote[aFieldName] != newValue
    aNote[aFieldName] = newValue
    return result

def onEditorFocusLost(aFlag, aNote, aFieldIndex):
    fieldName = mw.col.models.fieldNames(aNote.model())[aFieldIndex]

    if not fieldName.endswith(gSourceFieldSuffix):
        return aFlag

    fieldPrefix = fieldName[:-len(gSourceFieldSuffix)]
    aFlag |= updateDstField(aNote, aNote[fieldName], fieldPrefix + gOpenedFieldSuffix, r'\1')
    aFlag |= updateDstField(aNote, aNote[fieldName], fieldPrefix + gClozeFieldSuffix, r'[...]')

    return aFlag

def editorInit(self, *args, **kwargs):
    QShortcut(QKeySequence(gShortcutKey), self.widget, activated = lambda: self.web.eval("wrap('[[', ']]');"))

addHook('editFocusLost', onEditorFocusLost)
Editor.__init__ = wrap(Editor.__init__, editorInit)
