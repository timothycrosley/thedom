'''
    Name:
        Base.py

    Description:
        The BaseElements used by WebElements

'''

import re
import types

import DictUtils
import ToClientSide
from Connectable import Connectable
from IteratorUtils import Queryable
from MethodUtils import acceptsArguments, CallBack
from StringUtils import interpretAsString

try:
    from collections import OrderedDict
except ImportError:
    from DictUtils import OrderedDict

BLOCK_TAGS = ('address', 'blockquote', 'center', 'dir', 'div', 'dl', 'fieldset', 'form', 'h1',
              'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'isindex', 'menu', 'noframes', 'noscript', 'ol',
              'p', 'pre', 'table', 'ul', 'dd', 'dt', 'frameset', 'li', 'tbody', 'td', 'tfoot', 'th',
              'thead', 'tr')

def addChildProperties(propertiesDict, classDefinition, accessor):
    for propertyName, propertyDict in classDefinition.properties.iteritems():
        propertyDict = propertyDict.copy()
        propertyDict['action'] = accessor + "." + propertyDict['action']
        propertyDict['name'] = propertyDict.get('name', propertyName)
        propertiesDict[accessor + "." + propertyName] = propertyDict


class WebElement(Connectable):
    """
        The base WebElement which all custom WebElements should extend.
    """
    displayable = True
    tagSelfCloses = False
    tagName = ""
    allowsChildren = True
    _prefix = None
    signals = ['hidden', 'shown', 'beforeToHtml', 'childAdded', 'editableChanged']
    properties = OrderedDict()
    properties['style'] = {'action':'setStyleFromString'}
    properties['class'] = {'action':'addClassesFromString'}
    properties['javascriptEvents'] = {'action':'addJavascriptEventsFromDictionary'}
    properties['hide'] = {'action':'call', 'type':'bool'}
    properties['widthPreference'] = {'action':'classAttribute'}
    properties['alignPreference'] = {'action':'classAttribute'}
    properties['stylePreference'] = {'action':'setStylePreferenceFromString'}
    properties['title'] = {'action':'attribute'}
    properties['lang'] = {'action':'attribute'}
    properties['key'] = {'action':'classAttribute'}
    properties['validator'] = {'action':'classAttribute'}
    properties['uneditable'] = {'action':'call', 'name':'__setUneditable__', 'type':'bool'}

    def __init__(self, id=None, name=None, parent=None):
        """
            Initiates a WebElement object
            (if no name is passed in it will default to id)
        """
        Connectable.__init__(self)

        self.id = id
        self.name = name or id
        self.parent = parent

        self.style = {}
        self.classes = set()
        self.attributes = {}

        self.childElements = []
        self.addChildElementsTo = self

    def jsId(self):
        """
            Returns an id that can be used client side to access the object.
        """
        return self.fullId()

    def reset(self):
        """
            clears the element of all children
        """
        self.childElements = []

    def hide(self):
        """
            Makes the element invisible to the user
        """
        if not self.style.get('display', '') == 'none':
            self.style['display'] = "none"
            self.emit("hidden")

    def show(self):
        """
            Ensures that the element is visible to the user
        """
        if not self.style.get('display', '') == 'block':
            self.style['display'] = "block"
            self.emit("shown")

    def shown(self):
        """
            Returns True if the element is visible
        """
        if self.style.get('display', "") == "none":
            return False

        return True

    def fullName(self):
        """
            Returns the fullname of the element(prefix + name) this is the identifier that will
            make its way to the html output
        """
        if self.name and self.name != '':
            if self.prefix():
                returned_name = self.prefix() + self.name
            else:
                returned_name = self.name
        else:
            returned_name = ''

        return returned_name

    def fullId(self):
        """
            Returns the fullid of the element(prefix + id) this is the identifier that will make
            its way to the html output
        """
        if self.id and self.id != '':
            returned_id = self.id
            if self.prefix():
                returned_id = self.prefix() + returned_id
        else:
            returned_id = ''

        return returned_id

    def allChildren(self):
        """
            Returns all children, including children of children, in a list
        """
        children = []
        for child in self:
            children.append(child)
            children.extend(child.allChildren())

        return children

    def query(self):
        """
            Returns a queryable list of all children, allowing you to perform django style queries to find an element
        """
        return Queryable(self.allChildren())

    def getChildElementsWithClass(self, className):
        """
            Returns all elements with className specified
        """
        childrenWithClass = []
        for child in self.childElements:
            if child.hasClass(className):
                childrenWithClass.append(child)
            childrenWithClass.extend(child.getChildElementsWithClass(className))

        return childrenWithClass

    def getChildElementsWithName(self, name):
        """
            Returns all elements with the name specified
        """
        childrenWithName = []
        for child in self.childElements:
            if child.name == name:
                childrenWithName.append(child)
            childrenWithName.extend(child.getChildElementsWithName(name))

        return childrenWithName

    def getChildElementsWithTagName(self, tagName):
        """
            Returns all elements with the tagName specified
        """
        childrenWithTagName = []
        for child in self.childElements:
            if child.tagName == tagName:
                childrenWithTagName.append(child)
            childrenWithTagName.extend(child.getChildElementsWithTagName(tagName))

        return childrenWithTagName

    def getChildElementWithId(self, elementId):
        """
            Returns all elements with the id specified
        """
        childrenWithId = None
        for child in self:
            if child.id == elementId:
                return child
            nestedChild = child.getChildElementWithId(elementId)
            if nestedChild:
                return nestedChild

    def prefix(self):
        """
            Returns the prefix set for this element or the first parent element with one set
        """
        if self._prefix == None and self.parent:
            prefix = self.parent.prefix()
        elif self._prefix == " ":
            return ''
        else:
            prefix = self._prefix or ''

        return prefix

    def setPrefix(self, prefix):
        """
            Sets the elements idPrefix (a sort of section identifier that will be placed before
                                        all ids to ensure they are unique):
                prefix - the string that will be placed before all ids/names
        """
        self._prefix = prefix

    def moveElement(self, childElement, putAfter):
        self.childElements.remove(childElement)
        elementIndex = self.childElements.index(putAfterElement)
        self.childElements.insert(elementIndex, putAfterElement)

    def addChildElement(self, childElement, ensureUnique=True):
        """
           Add a child element within this element
            for example:
                container.toHtml() ==
                    <div></div>
                container.addChildElement(TextArea())
                <div><textarea></textarea></div>:

                childElement - the element to add
                ensureUnique - if set to True and the element already has a parent: the element
                               will be removed from its prev parent before being added
        """
        if type(childElement) == type:
            childElement = childElement(parent=self)

        if self.addChildElementsTo.allowsChildren:
            if(ensureUnique and childElement.parent):
                childElement.parent.removeChild(childElement)
            childElement.parent = self.addChildElementsTo
            self.addChildElementsTo.childElements.append(childElement)
            self.addChildElementsTo.emit('childAdded', childElement)

            scriptTemp = getattr(childElement, '__scriptTemp__', None)
            if scriptTemp:
                for script in scriptTemp:
                    self.addScript(script)

            objectTemp = getattr(childElement, '__objectTemp__', None)
            if objectTemp:
                for objectWithScripts in objectTemp:
                    self.addJSFunctions(objectWithScripts)

            return childElement
        else:
            return False

    def indentationLevel(self):
        """
            Returns a number representing the number of parent elements
        """
        if self.parent:
            return self.parent.indentationLevel() + 1
        else:
            return 0

    def replaceWith(self, replacementElement):
        """
            Replace this webElement in the tree with another:
                replacementElement - the element to replace it with
        """
        if self.parent:
            index = self.parent.childElements.index(self)
            self.parent.childElements[index] = replacementElement
            replacementElement.parent = self.parent
            return replacementElement
        else:
            return Invalid()

    def remove(self):
        """
            Deletes this element (requires a parent element)
        """
        if self.parent:
            self.parent.removeChild(self)
            return True
        return False

    def validators(self, useFullId=True):
        """
            Returns a list of all validators associated with this element and all child elements:
                useFullId - if set to True the validators are set against the prefix + id
        """
        validatorDict = {}
        validator = getattr(self, 'validator', None)
        if self.editable() and validator:
            if useFullId:
                validatorId = self.fullId()
            else:
                validatorId = self.id

            if not validatorId and self.name:
                if useFullId:
                    validatorId = self.fullName()
                else:
                    validatorId = self.name

            validatorDict[validatorId] = validator

        for child in self.childElements:
            validatorDict.update(child.validators(useFullId))

        return validatorDict

    def hasClass(self, className):
        """
            Returns true if the elements classes includes className:
                className - the class name to look for
        """
        return className in self.classes

    def addClass(self, className):
        """
            Adds a class to the element if it does not already exist:
                className - the name of the class to add
        """
        self.classes.add(className)

    def chooseClass(self, classes, choice):
        """
            Lets you choose one class out of a list of class choices
        """
        for className in classes:
            self.removeClass(className)
        self.addClass(choice)

    def setClasses(self, classes):
        """ Replace all current classes with a list of classes """
        self.classes = set(classes)
        self.attributes['class'] = self.classes

    def removeClass(self, className):
        """
            Removes a class from the element if it exists:
                className - the name of the class to remove
        """
        if self.hasClass(className):
            self.classes.remove(className)

    def editable(self):
        """
            Returns true if the input-type field in the element are editable
        """
        editable = getattr(self, '_editable', None)
        if editable == None:
            if self.parent:
                return self.parent.editable()
            else:
                return True

        return editable

    def setEditable(self, editable):
        """
            Changes the elements editable state:
                editable - setting this to True would allow input fields to be user-editable
        """
        self._editable = editable
        self.emit('editableChanged', editable)

    def __setUneditable__(self):
        self.setEditable(False)

    def scriptContainer(self):
        """
            Returns the root script container
        """
        if self.parent:
            return self.parent.scriptContainer()

        return getattr(self, '__scriptContainer__', False)

    def setScriptContainer(self, scriptContainer):
        """
            Sets the container where scripts should be stored:
                scriptContainer - the scriptContainer instance
        """
        if self.parent:
            self.parent.setScriptContainer(scriptContainer)
        else:
            self.__scriptContainer__ = scriptContainer
            if scriptContainer and scriptContainer != []:
                self.__insertTemporaryScripts()

    def runClientSide(self, python):
        return self.addScript(ToClientSide.convert(python))

    def dontRunClientSide(self, python):
        return self.removeScript(ToClientSide.convert(python))

    def addScript(self, script):
        """
            Adds a script to the script contianer set on the element:
                script - the script text or function to add
        """
        if self.scriptContainer():
            self.scriptContainer().addScript(script)
        elif self.parent:
            self.parent.addScript(script)
        else:
            self.__scriptTemp__ = getattr(self, '__scriptTemp__', [])
            if not script in self.__scriptTemp__:
                self.__scriptTemp__.append(script)

    def removeScript(self, script):
        """
            Removes a script from the scriptContainer associated with this element:
                script - the script text or function to remove
        """
        if self.scriptContainer():
            self.scriptContainer().removeScript(script)
        elif self.parent:
            self.parent.removeScript(script)
        else:
            scriptTemp = getattr(self, '__scriptTemp__', None)
            if scriptTemp and script in scriptTemp:
                scriptTemp.remove(script)

    def addJSFunctions(self, objectType):
        """
            Adds all static scripts associated with a webElement class:
                objectType - the non-instanciated webElement class
        """
        if self.scriptContainer():
            self.scriptContainer().addJSFunctions(objectType)
        elif self.parent:
            self.parent.addJSFunctions(objectType)
        else:
            self.__objectTemp__ = getattr(self, '__objectTemp__', [])
            self.__objectTemp__.append(objectType)

    def __insertTemporaryScripts(self):
        """
            Moves scripts that were added to the WebElement but not a scriptContainer over to
            the set scriptContainer
        """
        scriptTemp = getattr(self, '__scriptTemp__', None)
        if scriptTemp:
            for script in scriptTemp:
                self.addScript(script)
            self.__scriptTemp__ = []

        objectTemp = getattr(self, '__objectTemp__', [])
        if objectTemp:
            for objectType in objectTemp:
                self.addJSFunctions(objectType)
            self.__objectTemp__ = []

    def addClientSideEvent(self, event, python):
        self.addJavascriptEvent(event, ToClientSide.convert(python))

    def removeClientSideEvent(self, event, python=None):
        self.removeJavascriptEvent(event, python and ToClientSide.convert(python) or None)

    def addJavascriptEvent(self, event, javascript):
        """
            Adds a clientside action to be done on event:
                event - the name of the event to connect the javascript to (such as onclick)
                javascript - the script text or function to call on event
        """
        if type(event) in (types.ListType, types.TupleType):
            for eventName in event:
                self.attributes.setdefault(eventName, []).append(javascript)
        else:
            self.attributes.setdefault(event, []).append(javascript)

    def removeJavascriptEvent(self, event, javascript=None):
        """
            Removes actions associated with a client side event:
                event - the name of the event to remove actions from
                javascript - the specific action to remove(if not set all actions are removed)
        """
        if javascript:
            self.attributes[event].remove(javascript)
        elif self.attributes.has_key(event):
            self.attributes.pop(event)

    def javascriptEvent(self, event):
        """
            Returns the action associated with a particular client-side event:
                event - the name of the client side event
        """
        return interpretAsString(self.attributes.get(event, None))

    def removeChild(self, child):
        """
            Removes a child webElement:
                child - the element to remove
        """
        if child in self.childElements:
            self.childElements.remove(child)
            child.parent = None
            return True

        return False

    def startTag(self):
        """
            Returns the elements html start tag,
                for example '<span class="whateverclass">'
        """
        if not self.tagName:
            return u''

        self.attributes['name'] = self.fullName()
        self.attributes['id'] = self.fullId()
        self.attributes['class'] = self.classes
        self.attributes['style'] = self.style
        startTag = "<" + self.tagName + " "
        for key, value in self.attributes.iteritems():
            value = interpretAsString(value)
            if value:
                if value == '<BLANK>':
                    value = ""

                if value == '<EMPTY>':
                    startTag += key + " "
                else:
                    startTag += key + '="' + value.replace('"', '&quot;') + '" '

        if self.tagSelfCloses:
            startTag += '/'
        else:
            startTag = startTag[:-1]
        startTag += '>'

        return unicode(startTag)

    def endTag(self):
        """
            Returns the elements html end tag, for example '</span>'
        """
        if self.tagSelfCloses or not self.tagName:
            return u''

        return unicode("</" + self.tagName + ">")

    def content(self, formatted=False):
        """
            returns the elements html content
            (the html bettween startTag and endTag)
        """
        elementContent = []
        for element in self.childElements:
            if type(element) in (types.FunctionType, types.MethodType):
                currentElement = element()
            else:
                currentElement = element

            elementContent.append(currentElement.toHtml(formatted=formatted))
        if formatted:
            return "\n".join(elementContent)
        else:
            return ''.join(elementContent)

    def insertVariables(self, variableDict=None):
        """
            Populate webElement and child webElements with (id/name/key):value dictionary:
                variableDict - the dictionary to use to populate the elements
        """
        if variableDict == None:
            variableDict = {}

        for child in self.childElements:
            child.insertVariables(variableDict)

    def exportVariables(self, exportedVariables=None, flat=False):
        """
            Export WebElement input field values as a nested key:value dictionary:
                exportedVariables - the dictionary to add exported variables to
        """
        if exportedVariables == None:
            exportedVariables = {}

        for child in self.childElements:
            child.exportVariables(exportedVariables, flat)

        return exportedVariables

    def clearFromRequest(self, reqDict):
        """
            Removes variables pointing to this element or child elements from a request dictionary:
                reqDict - the dictionary to remove childElement values from
        """
        if self.id:
            reqDict.pop(self.id, '')
            reqDict.pop(self.fullId(), '')
        if self.name:
            reqDict.pop(self.name, '')
            reqDict.pop(self.fullName() , '')

        for child in self.childElements:
            child.clearFromRequest(reqDict)

    @staticmethod
    def __getStyleDictFromString(styleString):
        styleDict = {}

        styleDefinitions = styleString.split(';')
        for definition in styleDefinitions:
            if definition:
                name, value = definition.split(':')
                styleDict[name.strip()] = value.strip()

        return styleDict

    def setStyleFromString(self, string):
        """
            Updates the style dictionary based on a html style string
        """
        self.style.update(self.__getStyleDictFromString(string))

    def setStylePreferenceFromString(self, string):
        """
            Updates the style preference dictionary based on a html style string
        """
        if not hasattr(self, 'stylePreference'):
            self.stylePreference = {}
        self.stylePreference.update(self.__getStyleDictFromString(string))

    def addClassesFromString(self, string):
        """
            Adds classes based on a html type class string
        """
        classes = string.split(' ')
        for className in classes:
            if className:
                self.addClass(className)

    def addJavascriptEventsFromDictionary(self, dictionary):
        """
            Adds javascript events based on a dictionary
        """
        for key, value in dictionary.iteritems():
            self.addJavascriptEvent(key, value)

    def setProperty(self, name, value):
        """
            Sets the property of single element - as defined in the elements property dictionary
        """
        propertyDict = self.properties[name]
        propertyAction = propertyDict['action']
        propertyActions = propertyAction.split('.')
        propertyAction = propertyActions.pop(-1)
        propertyName = propertyDict.get('name', name)

        objectWithProperty = self
        for attributeName in propertyActions:
            objectWithProperty = objectWithProperty.__getattribute__(attributeName)

        if propertyAction == "classAttribute":
            objectWithProperty.__setattr__(propertyName, value)
        elif propertyAction == "attribute":
            objectWithProperty.attributes[propertyName] = value
        elif propertyAction == "javascriptEvent":
            objectWithProperty.addJavascriptEvent(propertyName, value)
        elif propertyAction == "call":
            if value:
                objectWithProperty.__getattribute__(propertyName)()
        elif not hasattr(objectWithProperty, propertyAction):
            print("Trying to set " + propertyName + " using " + propertyAction + " but no" +
                    " such method or attribute exists on " + objectWithProperty.__class__.__name__)
        else:
            objectWithProperty.__getattribute__(propertyAction)(value)

    def setProperties(self, valueDict):
        """
            Loads element attributes from dictionary - using the property dictionary defined for the element
        """
        for propertyName, propertyValue in valueDict.iteritems():
            if propertyValue != None and self.properties.has_key(propertyName):
                self.setProperty(propertyName, propertyValue)

    def toHtml(self, formatted=False):
        """
           Returns the element(including child elements) as standard html
        """

        self.emit("beforeToHtml")

        html = []
        startTag = self.startTag() or ''
        if startTag:
            html.append(startTag)

        content = self.content(formatted=formatted)
        if content:
            if formatted:
                for line in content.split("\n"):
                    html.append(" " + line)
            else:
                html.append(content)

        endTag = self.endTag() or ''
        if endTag:
            html.append(endTag)

        if formatted:
            html = "\n".join(html)
        else:
            html = "".join(html)

        return html

    def isBlockElement(self):
        """
            Returns true if the elements will render as an HTML block type
        """
        if self.tagName in BLOCK_TAGS or self.hasClass("WBlock"):
            return True
        return False

    def __iter__(self):
        return self.childElements.__iter__()

    def __contains__(self, element):
        return element in self.childElements

    def __getitem__(self, index):
        return self.childElements.__getitem__(index)

    def __setitem__(self, index, value):
        return self.childElements.__setitem__(index, value)

    def __delitem__(self, index):
        return self.childElements.__delitem__(index)

    def count(self):
        """
            Returns the number of child elements
        """
        return len(self.childElements)

    def __isub__(self, element):
        self.removeChild(element)
        return self

    def __iadd__(self, element):
        self.addChildElement(element)
        return self

    def __str__(self):
        return self.toHtml(formatted=True)

    def __representSelf__(self):
        representation = self.__class__.__name__ + "("
        attributes = []
        if self.id:
            attributes.append("id='%s'" % self.id)
        if self.name:
            attributes.append("name='%s'" % self.name)
        representation += ", ".join(attributes)
        representation += ")"

        return representation

    def __repr__(self):
        representation = [self.__representSelf__()]
        for child in self:
            for index, line in enumerate(repr(child).split("\n")):
                if index == 0:
                    representation.append("|---" + line)
                else:
                    representation.append("|  " + line)
        return "\n".join(representation)


class Invalid(WebElement):
    """
        An Invalid WebElement - used generally to show that a desired element failed to load
    """
    allowsChildren = False

    def __init__(self, id=None, name=None, parent=None):
        WebElement.__init__(self, id, name, parent)
        self.tagName = "h2"

    def setProperties(self, valueDict):
        pass

    def content(self, formatted=False):
        """
            Overrides content to return 'Invalid element' string
        """
        return "Invalid Element"


class TextNode(object):
    """
        Defines the most basic concept of an html node - does not have the concept of children only of producing html
        should only be used internally or for testing objects
    """
    _text = ''
    parent = None

    def __init__(self, text=None):
        if text:
            self.setText(text)

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text

    def toHtml(self, *args, **kwargs):
        return unicode(self.text())

    def insertVariables(self, *args, **kwargs):
        pass

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.text()) + ")"


class TemplateElement(WebElement):
    """
        A template WebElement is a web element that uses a template for its presantation and
        structure
    """
    factory = None
    template = None

    def __init__(self, id=None, name=None, parent=None, template=None, factory=None):
        WebElement.__init__(self, id, name, parent)
        self.tagName = 'div'

        if template:
            self.template = template

        if factory:
            self.factory = factory

        accessors = {}
        instance = self.factory.buildFromDictionary(self.template, accessors=accessors, parent=self)
        for accessor, element in accessors.iteritems():
            if hasattr(self, accessor):
                raise ValueError("The accessor name or id of the element has to be unique and can not be the same as a"
                                 " base webelement attribute."
                                 "Failed on adding element with id or accessor '%s'." % accessor)

            self.__setattr__(accessor, element)

        self.addChildElement(instance)

