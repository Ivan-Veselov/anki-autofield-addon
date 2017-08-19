import sys # for debug purpose
import re

from aqt.qt import *

from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor
from anki.hooks import wrap

gSourceFieldName = "Example [source]"
gOpenedFieldName = "Example [opened]"
gClozeFieldName = "Example [cloze]"

gSyntaxPattetn = r'\[\[(.*?)\]\]'

gShortcutKey = "F12"

def updateDstField(aNote, aFieldName, aReplacement):
    if not aFieldName in mw.col.models.fieldNames(aNote.model()):
        return False
    
    newValue = re.sub(gSyntaxPattetn,
                      r'<font color="#0000ff"><b>' + aReplacement + r'</b></font>', #tune
                      aNote[gSourceFieldName])

    result = aNote[aFieldName] != newValue
    aNote[aFieldName] = newValue
    return result

def onEditorFocusLost(aFlag, aNote, aFieldIndex):
    fieldNames = mw.col.models.fieldNames(aNote.model())
    
    if fieldNames[aFieldIndex] != gSourceFieldName:
        return aFlag

    aFlag |= updateDstField(aNote, gOpenedFieldName, r'\1')
    aFlag |= updateDstField(aNote, gClozeFieldName, r'[...]')

    return aFlag

def editorInit(self, *args, **kwargs):
    QShortcut(QKeySequence(gShortcutKey), self.widget, activated = lambda: self.web.eval("wrap('[[', ']]');"))

addHook('editFocusLost', onEditorFocusLost)
Editor.__init__ = wrap(Editor.__init__, editorInit)
