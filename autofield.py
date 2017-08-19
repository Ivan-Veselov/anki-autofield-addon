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

def editorInit(self, *args, **kwargs):
    QShortcut(QKeySequence(gShortcutKey), self.widget, activated = lambda: self.web.eval("wrap('[[', ']]');"))

addHook('editFocusLost', onEditorFocusLost)
Editor.__init__ = wrap(Editor.__init__, editorInit)
