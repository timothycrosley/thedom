#!/usr/bin/python
"""
   Name:
       Resources

   Description:
       Elements that allow you to use external resources

"""

import types

import Base
import Factory
from MethodUtils import CallBack
from StringUtils import interpretAsString

Factory = Factory.Factory(Base.Invalid, name="Resources")


class ResourceFile(Base.WebElement):
    """
        Enables you to add resource files (javascript, css, etc..) to a page
    """
    tagName = 'link'
    properties = Base.WebElement.properties.copy()
    properties['file'] = {'action':'setFile'}
    properties['media'] = {'action':'attribute'}
    displayable = False

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name)
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
        self.textBeforeChildren = ""

        extension = fileName.split("?")[0][-3:]
        if ":" in fileName:
            rel, href = fileName.split(":")
            self.tagName = "link"
            self.attributes['src'] = href
            self.attributes['rel'] = rel
            self.resourceType = rel
            self.tagSelfCloses = True
        elif extension == ".js":
            self.tagName = "script"
            self.attributes['src'] = fileName
            self.resourceType = "javascript"
            self.tagSelfCloses = False
        elif extension == "css":
            self.tagName = "link"
            self.attributes['rel'] = "stylesheet"
            self.attributes['type'] = "text/css"
            self.attributes['href'] = fileName
            self.resourceType = "css"
            self.tagSelfCloses = True
        elif extension == "png":
            self.tagName = "link"
            self.attributes['rel'] = "icon"
            self.attributes['type'] = "image/png"
            self.attributes['href'] = fileName
            self.resourceType = "css"
            self.tagSelfCloses = True
        else:
            self.tagName = "h2"
            self.textBeforeChildren = "Invalid Resource: %s" % fileName
            self.resourceType = None
            self.tagSelfCloses = False

Factory.addProduct(ResourceFile)


class ScriptContainer(Base.WebElement):
    """
        All scripts should be stored in a Script Box object
    """
    displayable = False
    tagName = "script"
    properties = Base.WebElement.properties.copy()
    properties['script'] = {'action':'addScript'}

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self)
        self.attributes['language'] = 'javascript'
        self.attributes['type']  = 'text/javascript'
        self._scripts = []
        self.usedObjects = []

    def content(self, variableDict=None, formatted=False):
        """
            Overrides the base content method to return the javascript associated with the scriptcontainer
        """
        scriptContent = ""
        for script in self.scripts():
            scriptContent += interpretAsString(script) + "\n"

        for objectType in self.usedObjects:
            for function in objectType.jsFunctions:
                scriptContent += self.jsFunctionAsString(getattr(objectType,
                                                                 function))

        return scriptContent

    def addJSFunctions(self, objectType):
        """
            Adds all jsFunction scripts set on the passed in class
        """
        if not objectType in self.usedObjects:
            self.usedObjects.append(objectType)

    def jsFunctionAsString(self, jsFunction):
        """
            Creates and returns a jsFunction implementation based on a pased in python function representation
        """
        methodName = jsFunction.__name__
        attributes = list(jsFunction.func_code.co_varnames)
        attributes.reverse()

        if jsFunction.func_defaults:
            methodDefaults = list(jsFunction.func_defaults)
        else:
            methodDefaults = []

        methodDefaults.reverse()

        defaults = {}
        for index, default in enumerate(methodDefaults):
            if type(default) in types.StringTypes:
                default = "'" + default + "'"
            else:
                default = interpretAsString(default)
            defaults[attributes[index]] = default

        attributeValues = {}
        for attribute in attributes:
            if defaults.get(attribute, None) == None:
                attributeValues[attribute] = None

        attributes.reverse()
        script = ["\nfunction %s(%s)" % (methodName, ', '.join(attributes))]
        script.append("{")
        for var, default in defaults.iteritems():
            script.append("\tif(%s == null) var %s = %s;" % (var, var, default))

        for var in attributes:
            if var.startswith("element"):
                script.append('\tvar %s = JUGetElement(%s);' % (var, var))
        script.append(interpretAsString(jsFunction(**attributeValues)))
        script.append("}\n")

        return "\n".join(script)

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
