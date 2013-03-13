'''
    HTML5.py

    Contains complex elements that take advantage of features unique to modern HTML5 browsers,
    and therefore will only work on more recent systems

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from . import Base, Display, Factory, Layout
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("HTML5")

class FileUploader(Layout.Vertical):
    """
        An HTML5 brower only file-uploader - allows dragging and dropping files to upload them. :: IN DEVELOPMENT ::
    """
    __slots__ = ('dropArea', 'dropLabel', 'preview', 'dropIndicator', 'files', 'statusBar')

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical._create(self, id, name, parent, **kwargs)
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
        """
            Adds the necessary javascript to set up the file uploader client-side.
        """
        return "WebElements.buildFileOpener('%s');" % self.fullId()

Factory.addProduct(FileUploader)
