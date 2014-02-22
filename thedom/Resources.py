'''
    Resources.py

    Contains elements that enable use of external resources such as CSS files

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

import types

from . import DOM, Base, ClientSide, Factory
from .DOM import H2, Link, Script
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("Resources")


class ResourceFile(Base.Node):
    """
        Enables you to add resource files (javascript, css, etc..) to a page
    """
    __slots__ = ('resourceFile', 'fileName', 'resourceFile', 'resourceType')
    properties = Base.Node.properties.copy()
    properties['file'] = {'action':'setFile'}
    properties['media'] = {'action':'attribute'}
    displayable = False

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.Node._create(self, id, name)
        self.resourceFile = self.addChildElement(Base.TextNode())
        self.setFile("")

    def shown(self):
        """
            Resource files are never visible
        """
        return False

    def setFile(self, fileName):
        """
            Sets the location of the resource file, and determines the resource type from that:
                fileName - the disk name of the file.
        """
        self.fileName = fileName

        extension = fileName.split("?")[0][-3:]
        if ":" in fileName:
            rel, href = fileName.split(":")
            resource = Link()
            resource.setProperties((('rel', rel), ('src', href)))
            self.resourceType = rel
        elif extension == ".js":
            resource = Script()
            resource.setProperties((('src', fileName), ))
            self.resourceType = "javascript"
        elif extension == "css":
            resource = Link()
            resource.setProperties((('rel', 'stylesheet'), ('type','text/css'), ('href', fileName)))
            self.resourceType = "css"
        elif extension == "png":
            resource = Link()
            resource.setProperties((('rel', 'icon'), ('type','image/png'), ('href', fileName)))
            self.resourceType = "favicon"
        else:
            resource = H2()
            resource.addChildElement(Base.TextNode("Invalid Resource: %s" % fileName))
            self.resourceType = None

        self.resourceFile = self.resourceFile.replaceWith(resource)

Factory.addProduct(ResourceFile)


class ScriptContainer(DOM.Script):
    """
        All scripts should be stored in a Script Box object
    """
    __slots__ = ('_scripts', 'usedObjects')
    displayable = False
    properties = DOM.Script.properties.copy()
    properties['script'] = {'action':'addScript'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.Node._create(self)
        self.attributes['language'] = 'javascript'
        self.attributes['type']  = 'text/javascript'
        self._scripts = []

    def content(self, formatted=False, *args, **kwargs):
        """
            Overrides the base content method to return the javascript associated with the scriptcontainer
        """
        scriptContent = ";".join([str(script) for script in self.scripts()])

        return scriptContent

    def addScript(self, script):
        """
            Adds a script to the container
        """
        if not script in self._scripts:
            self._scripts.append(script)

    def removeScript(self, script):
        """
            Removes a script that has been passed into the container
        """
        if script in self._scripts:
            self._scripts.remove(script)

    def shown(self):
        """
            Script containers are never visible
        """
        return False

    def scripts(self):
        """
            Returns a list of all passed in scripts
        """
        return self._scripts

Factory.addProduct(ScriptContainer)
