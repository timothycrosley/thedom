"""
    Contains elements that only work in HTML5 compatible browsers
"""

import Factory
from WebElements import Display
from WebElements import Layout
from MethodUtils import CallBack

Factory = Factory.Factory("HTML5")

class FileUploader(Layout.Vertical):
    __slots__ = ('dropArea', 'dropLabel', 'preview', 'dropIndicator', 'files', 'statusBar')

    def __init__(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical.__init__(self, id, name, parent, **kwargs)
        self.addClass("WDropArea")
        self.addClass("WEmpty")

        self.statusBar = self.addChildElement(Layout.Horizontal(id + "StatusBar"))
        self.statusBar.addClass("WStatusBar")
        self.statusBar.hide()

        self.dropIndicator = self.statusBar.addChildElement(Display.Image())
        self.dropIndicator.setProperty('src', 'images/throbber.gif')
        self.dropIndicator.addClass("WDropIndicator")

        self.dropLabel = self.statusBar.addChildElement(Display.Label(id + "DropLabel"))
        self.dropLabel.setText("Drop Files Here")
        self.dropLabel.addClass("WDropLabel")

        self.files = self.addChildElement(Layout.Horizontal(id + "Files"))
        self.files.addClass("WFiles")

        baseFile = self.files.addChildElement(Layout.Vertical(id + "File"))
        baseFile.addClass("WFile")
        imageContainer = baseFile.addChildElement(Layout.Box())
        imageContainer.addClass("WImageContainer")
        preview = imageContainer.addChildElement(Display.Image())
        preview.addClass("WThumbnail")
        name = baseFile.addChildElement(Display.Label())
        name.addClass("WFileName")
        baseFile.hide()

        self.addScript(CallBack(self, 'jsConnections'))

    def jsConnections(self):
        return "WebElements.buildFileOpener('%s');" % self.jsId()

Factory.addProduct(FileUploader)