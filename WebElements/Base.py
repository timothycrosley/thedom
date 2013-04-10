'''
    Base.py

    This library defines the most basic (abstract) Web Element from which all other elements are derived

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

import re
import cgi
from types import FunctionType

from . import ClientSide, DictUtils, ToClientSide
from .Connectable import Connectable
from .IteratorUtils import Queryable
from .MethodUtils import acceptsArguments, CallBack
from .MultiplePythonSupport import *
from .StringUtils import interpretAsString, listReplace
from itertools import chain


class Settings(object):
    STATIC_URL = ""
    INDENTATION = " "
    BLOCK_TAGS = ('address', 'blockquote', 'center', 'dir', 'div', 'dl', 'fieldset', 'form', 'h1',
                'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'isindex', 'menu', 'noframes', 'noscript', 'ol',
                'p', 'pre', 'table', 'ul', 'dd', 'dt', 'frameset', 'li', 'tbody', 'td', 'tfoot', 'th',
                'thead', 'tr')

def addChildProperties(propertiesDict, classDefinition, accessor):
    """
        Modifies the passed in propertiesDict to contain the properties of a child element of class type
        classDefinition, with the accessor referring to the name of the attribute on self that will hold the child
        instance. Accessing the properties is then done in the form of [accessor]s.[childElement's property].
    """
    for propertyName, propertyDict in iteritems(classDefinition.properties):
        propertyDict = propertyDict.copy()
        propertyDict['action'] = accessor + "." + propertyDict['action']
        propertyDict['name'] = propertyDict.get('name', propertyName)
        propertiesDict[accessor + "." + propertyName] = propertyDict

def autoAddScript(function):
    """
        Returns a decorator function that will automatically add it's result to the element's script container.
    """
    def autoAdd(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        if isinstance(result, ClientSide.Script):
            self(result)
            return result
        else:
            return ClientSide.Script(ClientSide.var(result))
    return autoAdd


class AutoAddScripts(type):
    """
        Modifies the client side object to automatically addScripts when methods are called, unless the scripts are
        later taken by a javascript event (basically adds the autoAddScript decorator to every method in the class)
    """
    def __new__(cls, name, bases, dct):
        for name, attribute in dct.items():
            if name in ("serverside", "id") or name.startswith("_") or type(attribute) != FunctionType:
                continue

            dct[name] = autoAddScript(attribute)

        return type.__new__(cls, name, bases, dct)

AutoAddScripts = AutoAddScripts('AutoAddScripts', (object, ), {})


class WebElement(Connectable):
    """
        The base WebElement which all custom WebElements should extend.
    """
    __slots__ = ('_tagName', '_prefix', '__scriptTemp__', '__objectTemp__', 'validator', '_editable',
                 '__scriptContainer__', 'id', 'name', 'parent', '_style', '_classes', '_attributes',
                 '_childElements', 'addChildElementsTo', 'key', '_tagSelfCloses', '_clientSide')
    tagSelfCloses = False
    allowsChildren = True
    displayable = True
    signals = ['hidden', 'shown', 'rendering', 'childAdded', 'editableChanged']
    properties = {}
    properties['style'] = {'action':'setStyleFromString'}
    properties['class'] = {'action':'addClassesFromString'}
    properties['javascriptEvents'] = {'action':'addJavascriptEventsFromDictionary'}
    properties['hide'] = {'action':'call', 'type':'bool'}
    properties['title'] = {'action':'attribute'}
    properties['lang'] = {'action':'attribute'}
    properties['key'] = {'action':'classAttribute'}
    properties['validator'] = {'action':'classAttribute'}
    properties['uneditable'] = {'action':'call', 'name':'__setUneditable__', 'type':'bool'}
    properties['contenteditable'] = {'action':'attribute'}
    properties['draggable'] = {'action':'attribute'}
    properties['hidden'] = {'action':'attribute', 'type':'bool'}
    properties['hidden'] = {'action':'attribute', 'type':'bool'}
    properties['tabindex'] = {'action':'attribute', 'type':'int'}
    properties['accesskey'] = {'action':'attribute'}
    tagName = ""

    class ClientSide(AutoAddScripts):
        """
            Defines the client side behavior, and actions of an element
        """
        __slots__ = ('serverSide',)

        def __init__(self, element):
            self.serverSide = element

        def on(self, event, action):
            """
                Attaches a client side action to be performed every time event occurs.
            """
            if type(action) in (list, tuple):
                action = ClientSide.Script(";".join([ClientSide.var(actionScript) for actionScript in action]))
            return ClientSide.addEvent(self, event, ClientSide.eventHandler(action))

        def onKey(self, key, action, direction="up"):
            """
                Attaches a client side action to be performed every time a key is pressed on the element.
            """
            with self.evt.keyCode.IF.IS(key) as eventHandler:
                eventHandler(action)

            return self.on('key' + direction, eventHandler)

        @property
        def id(self):
            """
                Returns what the element's id will be by the time it is rendered on the client's browser.
            """
            return self.serverSide.fullId()

        def __call__(self, script):
            self.serverSide.addScript(script)
            return script

        def assign(self, name, var):
            """
                Assigns a variable to the stack client-side, which is then accessible from the ClientSide object
                by doing self.[name].
            """
            return ClientSide.assign(name, var)

        def __getattr__(self, name):
            return ClientSide.Script(name)

        def alert(self, message):
            """
                Pops-up an alert window with the text contained in message.
            """
            return ClientSide.call("alert", message)

        def log(self, message):
            """
                Logs message client-side viewable from common debuggers (such as firebug).
            """
            return ClientSide.call("console.log", message)

        def get(self):
            """
                Returns an element retrieved based upon it's id or unique name
            """
            return ClientSide.get(self)

        def forEach(self, arrayOfItems, callBack):
            """
                Calls callback against each item in arrayOfItems.
            """
            return ClientSide.forEach(arrayOfItems, callBack)

        def onEach(self, arrayOfItems, callBack):
            """
                Returns an array where each element of arrayOfItems has been modified by callBack.
            """
            return ClientSide.onEach(arrayOfItems, callBack)

        def sortElements(self, elements):
            """
                Returns a sorted copy of elements.
            """
            return ClientSide.sortElements(elements)

        def sortUnique(self, elements):
            """
                Returns a unique sorted copy of elements.
            """
            return ClientSide.sortUnique(elements)

        def getChildrenByTagNames(self, tagNames, unsorted=True):
            """
                Returns an array of elements that are children of self and have one of the defined tagNames.
                Setting unsorted to False will sort the array before returning it.
            """
            return ClientSide.getElementsByTagNames(tagNames, parentElement=self, unsorted=unsorted)

        def getChildrenByCondition(self, conditional, stopOnFirstMatch=False):
            """
                Returns all child elements of self that pass the conditional. If stopOnFirstMatch is true
                it will only return the first matching element - without testing the rest.
            """
            return ClientSide.getByCondition(conditional, self, stopOnFirstMatch)

        def getChildrenByClassName(self, className):
            """
                Returns all child elements that include className.
            """
            return ClientSide.getElementsByClassName(className, self)

        def getChildByClassName(self, className):
            """
                Returns the first child element that includes className.
            """
            return ClientSide.getElementByClassName(className, self)

        def getChildrenByAttribute(self, attributeName, attributeValue):
            """
                Returns all children that have attributeName set to attributeValue.
            """
            return ClientSide.getChildrenByAttribute(self,  attributeName, attributeValue)

        def getChildByAttribute(self, attributeName, attributeValue):
            """
                Returns the first child that has attributeName set to attributeValue.
            """
            return ClientSide.getChildByAttribute(self, attributeName, attributeName)

        def getChildrenByName(self, name):
            """
                Returns all children with the have the name specified.
            """
            return ClientSide.getChildrenByName(self, name)

        def getChildByName(self, name):
            """
                Returns the first child element with the name specified.
            """
            return ClientSide.getChildByName(self, name)

        def populate(self, fieldDict):
            """
                Populates all child element inputs with the data defined in fieldDict, where fieldDict is
                an id:value dictionary.
            """
            return ClientSide.populate(fieldDict)

        def pixelsToLeft(self):
            """
                Returns the number of pixels to the left of this element.
            """
            return ClientSide.pixelsToLeft(self)

        def pixelsAbove(self):
            """
                Returns the number of pixels above this element.
            """
            return ClientSide.pixelsAbove(self)

        def setAbsoluteRelativeToParent(element, pixelsDown=0, pixelsToRight=0, parentElement=None):
            """
                Places the element at an exact pixel location on the display, relative to the defined parentElements
                location.
            """
            return ClientSide.setAbsoluteRelativeToParent(self, pixelsDown, pixelsToRight, parentElement)

        def fellowChild(self, parentClass, childClass):
            """
                Returns the first element that is both a common child of the first parent element that includes
                parentClass, and includes childClass.
            """
            return ClientSide.fellowChild(self, parentClass, childClass)

        def firstChild(self):
            """
                Returns the first child element.
            """
            return ClientSide.firstChild(self)

        def lastChild(self):
            """
                Returns the last child element.
            """
            return ClientSide.lastChild(self)

        def nextSibling(self):
            """
                Returns the next element that has the same parent.
            """
            return ClientSide.nextSibling(self)

        def prevSibling(self):
            """
                Returns the previous defined element that shares the same parent.
            """
            return ClientSide.prevSibling(self)

        def setPrefix(self, prefix):
            """
                Set's the prefix of the element, updating the id of itself and all child elements to include it.
            """
            return ClientSide.setPrefix(self, prefix)

        def parentWithClass(self, className, giveUpAtClass=False):
            """
                Returns the first parent element that includes className unless it reaches a parent that includes
                giveUpAtClass.
            """
            return ClientSide.parent(self, className, giveUpAtClass)

        def clearChildren(self, replacement=None):
            """
                Removes all child elements, optionally replacing them with replacement.
            """
            return ClientSide.clearChildren(self, replacement)

        def childElements(self):
            """
                Returns an array of child elements.
            """
            return ClientSide.childElements(self)

        def peer(self, className):
            """
                Returns the first element that shares the same parent and includes className.
            """
            return ClientSide.peer(self, className)

        def peers(self, className):
            """
                Returns the first element that shares the same parent and includes className.
            """
            return ClientSide.peers(self, className)

        def stealClassFromPeer(self, className):
            """
                Adds className after removing the class from any element that shares the same parent.
            """
            return ClientSide.stealClassFromPeer(self, className)

        def stealClassFromFellowChild(self, parentClass, className):
            """
                Adds className after removing the class from any element that shares the same grandparent.
            """
            return ClientSide.stealClassFromFellowChild(self, parentClass, className)

        def toggleVisiblity(self):
            """
                Toggles whether or not the element can be seen.
            """
            return WebElements.toggleVisiblity(self)

        def hideClass(self, className):
            """
                Hides child elements that include className.
            """
            return ClientSide.hideClass(className, self)

        def showClass(self, className):
            """
                Shows child elements that include className.
            """
            return ClientSide.showClass(className, self)

        def buildThrobber(self):
            """
                Returns a DOM image object with the throbber image as it's source.
            """
            return ClientSide.buildThrobber()

        def show(self):
            """
                Makes the element visible.
            """
            return ClientSide.show(self)

        def hide(self):
            """
                Makes the element invisible.
            """
            return ClientSide.hide(self)

        def shown(self):
            """
                Returns True if the element is visible, False if it is not.
            """
            return ClientSide.elementShown(self)

        def replace(self, newElement):
            """
                Replaces this element in it's parent's hierarchy with newElement.
            """
            return ClientSide.replace(self, newElement)

        def remove(self):
            """
                Completely removes the element.
            """
            return ClientSide.remove(self)

        def clear(self):
            """
                Removes all children from the element.
            """
            return ClientSide.clear(self)

        def addHtml(self, html):
            """
                Adds basic html to the element.
            """
            return ClientSide.addHtml(self, html)

        def move(self, to):
            """
                Removes the element from it's current location, adding it to 'to'.
            """
            return ClientSide.move(self, to)

        def copy(self, to, incrementId=False):
            """
                Adds a copy of the element to 'to'.
            """
            return ClientSide.copy(self, to, incrementId)

        def contains(self, text, subtext, caseSensitive=False):
            """
                Returns True if text contains subtext.
            """
            return ClientSide.contains(text, subtext, caseSensitive)

        def startsWith(self, text, subtext, caseSensitive=False):
            """
                Returns True if text starts-with subtext.
            """
            return ClientSide.startsWith(text, subtext, caseSensitive)

        def addPrefix(self, prefix):
            """
                Adds a prefix to the element and all child elements.
            """
            return ClientSide.addPrefix(self, prefix)

        def removeDuplicates(self, array):
            """
                Returns an array without any duplicate items.
            """
            return ClientSide.removeDuplicates(array)

        def getElementsByValue(self, value):
            """
                Returns all elements that have their value attribute set to the defined value.
            """
            return ClientSide.getElementByValue(self, value)

        def getElementByInnerHTML(self, html):
            """
                Returns the first element whose rendered html directly matches that defined.
            """
            return ClientSide.getElementByInnerHTML(self, html)

        def replaceAll(string, toReplace, replacement):
            """
                Replaces all instances of toReplace with replacement within the string.
            """
            return ClientSide.replaceAll(string, toReplace, replacement)

        def classes(self):
            """
                Returns an array of all classes included in the element.
            """
            return ClientSide.classes(self)

        def hasClass(self, className):
            """
                Returns True if the element includes className.
            """
            return ClientSide.hasClass(self, className)

        def setClasses(self, classList):
            """
                Overrides the classes included on the element to classList.
            """
            return ClientSide.setClasses(self, classList)

        def removeClass(self, className):
            """
                Removes the class className from the element.
            """
            return ClientSide.removeClass(self, className)

        def addClass(self, className):
            """
                Adds the class className to the element.
            """
            return ClientSide.addClass(self, className)

        def removeFromArray(self, arrayOfItems, toRemove):
            """
                Returns an array void of toRemove.
            """
            return ClientSide.removeFromArray(arrayOfItems, toRemove)

        def chooseClass(self, classes, choice):
            """
                Updates the element to only include the choice class and remove any of the other defined classes.
            """
            return ClientSide.chooseClass(self, classes, choice)

        def redraw(self):
            """
                Removes and then reinserts the element client-side to force a redraw.
            """
            return ClientSide.redraw(self)

        def strip(self, string):
            """
                Strips the defined string of leading and/or trailing white-space.
            """
            return ClientSide.strip(string)

        def stripLeadingZeros(self, string):
            """
                Strips any zeros that are placed at the beginning of string.
            """
            return ClientSide.stripLeadingZeros(string)

        def inList(self, array, value):
            """
                Returns true if value is contained in array.
            """
            return ClientSide.inList(array, value)

        def appendOnce(self, array, item):
            """
                Adds item to the array only if it is not yet included.
            """
            return ClientSide.appendOnce(array, item)

        def combine(self, array1, array2):
            """
                Returns an array that contains all items defined in array1 and array2.
            """
            return ClientSide.combine(array1, array2)

        def suppress(self, attribute):
            """
                Suppresses an event on the element from occurring by renaming it.
            """
            return ClientSide.suppress(self, attribute)

        def unsuppress(self, attribute):
            """
                Allows an event that had previously been suppressed, to be handled correctly again.
            """
            return ClientSide.unsuppress(self, attribute)

        def closeMenu(self):
            """
                Closes the currently open drop-down menu.
            """
            return ClientSide.closeMenu()

        def openPopup(self, url, width=700, height=700, normal=False, windowTitle="_blank", options=None):
            """
                Opens a popup window to url, with the specified width, height and title.
            """
            return ClientSide.openPopup(url, width, height, normal, windowTitle, options)

        def scrolledToBottom(self):
            """
                Returns True if the user has scrolled to the bottom of the viewport.
            """
            return ClientSide.scrolledToBottom(self)

        def toggleClass(self, className):
            """
                Toggles whether or not the specified className is included on the element.
            """
            return ClientSide.toggleClass(self, className)

        def getNotificationPermission(self):
            """
                Requests permissions from the user to send them notifications.
            """
            return ClientSide.getNotificationPermission()

        def showNotification(self, title, content, icon="images/info.png"):
            """
                Shows a notifications to the user, where title is the subject and content is the message.
            """
            return ClientSide.showNotification(title, content, icon)

        def stopOperation(self, event):
            """
                Stops the specified event from occurring.
            """
            return ClientSide.stopOperation(event)

        def serialize(self):
            """
                Serializes the values contained in all child inputs into an id:value dictionary.
            """
            return ClientSide.serialize(self)

        def serializeElements(self, elements):
            """
                Serializes all defined elements into an id:value dictionary.
            """
            return ClientSide.serializeElements(self, elements)

        def serializeAll(self):
            """
                Serializes the entire page into an id:value dictionary.
            """
            return ClientSide.serializeAll(self)

        def confirm(self, message, action):
            """
                Prompts the user to confirm message then performs the specified action.
            """
            return ClientSide.confirm(message, action)

        def callOpener(self, method):
            """
                When called from a popup this will execute the specified method from the parent window.
            """
            return ClientSide.callOpener(method)

        def updateParent(self):
            """
                Tells any parent windows to update themselves, as newer data is available.
            """
            return ClientSide.updateParent()

        def focus(self, selectText=False):
            """
                Sets focus onto the element, optionally selecting already inputed text.
            """
            return ClientSide.focus(self, selectText)

        def redirect(self, to):
            """
                Redirects to the defined URL.
            """
            return ClientSide.redirect(to)

        def expandTemplate(self, template, valueDictionary):
            """
                Expands a python style template, client-side.
            """
            return ClientSide.expandTemplate(template, valueDictionary)

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Connectable.__init__(self)
        self._create(id, name, parent, **kwargs)
        if kwargs:
            self.setProperties(kwargs)

    def _create(self, id=None, name=None, parent=None, **kwargs):
        """
            Sets up the WebElement instance, adding any child elements and defining any attributes.
            (if no name is passed in it will default to id)
        """
        self._tagName = self.__class__.tagName
        self._tagSelfCloses = self.tagSelfCloses
        self._prefix = None

        self.id = id
        self.name = name or id
        self.parent = parent
        self.key = None

        self._style = None
        self._classes = None
        self._attributes = None
        self._clientSide = None

        self._childElements = None
        self.addChildElementsTo = self

        self.__scriptTemp__ = None
        self.__scriptContainer__ = None
        self.__objectTemp__ = None
        self._editable = None
        self.validator = None

    @property
    def attributes(self):
        """
            Returns the element's attributes (creating them on-demand in a lazy fashion)
        """
        if self._attributes is None:
            self._attributes = {}

        return self._attributes

    @property
    def classes(self):
        """
            Returns the element's classes (creating them on-demand in a lazy fashion)
        """
        if self._classes is None:
            self._classes = set([])

        return self._classes

    @property
    def style(self):
        """
            Returns the element's style dictionary (creating it on-demand in a lazy fashion)
        """
        if self._style is None:
            self._style = {}

        return self._style

    @property
    def childElements(self):
        """
            Returns the children of the element (creating them on-demand in a lazy fashion)
        """
        if self._childElements is None:
            self._childElements = []

        return self._childElements

    @childElements.setter
    def childElements(self, childElements):
        """
            Sets the child elements of this element
        """
        if not childElements:
            self._childElements = None
        else:
            self._childElements = childElements

    @property
    def clientSide(self):
        """
            Returns the element's client side controller (creating it on-demand in a lazy fashion)
        """
        if self._clientSide is None:
            self._clientSide = self.ClientSide(self)
        return self._clientSide

    def reset(self):
        """
            clears the element of all children
        """
        self._childElements = []

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
            if not type(child) == TextNode:
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
            if child._tagName == tagName:
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

    def errors(self):
        """
            Returns all errors present and visible within this element
        """
        return self.query().filter(classes__contains="WError", shown=True)

    def prefix(self):
        """
            Returns the prefix set for this element or the first parent element with one set
        """
        if self._prefix is None and self.parent:
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
        """
            Changes the rendering order of the element, placing it right after 'putAfter'.
        """
        self.childElements.remove(childElement)
        elementIndex = self.childElements.index(putAfterElement)
        self.childElements.insert(elementIndex, putAfterElement)

    def addChildElement(self, childElement, ensureUnique=True):
        """
           Add a child element within this element
            for example:
                container.toHTML() ==
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

            if not type(childElement) == TextNode:
                scriptTemp = childElement.__scriptTemp__
                if scriptTemp:
                    for script in scriptTemp:
                        self.addScript(script)

                objectTemp = childElement.__objectTemp__
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
        validator = self.validator
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

        for child in (child  for child in self.childElements if type(child) != TextNode):
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
        self._classes = set(classes)
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
        editable = self._editable
        if editable is None:
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

        return self.__scriptContainer__

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

        return scriptContainer

    def runClientSide(self, python):
        """
            Converts the python code directly to client-side code :: FEATURE STILL IN DEVELOPMENT ::
        """
        return self.addScript(ToClientSide.convert(python))

    def dontRunClientSide(self, python):
        """
            Removes the defined client side python code so it wont be executed :: FEATURE STILL IN DEVELOPMENT ::
        """
        return self.removeScript(ToClientSide.convert(python))

    def addScript(self, script):
        """
            Adds a script to the script contianer set on the element:
                script - the script text or function to add
        """
        scriptContainer = self.scriptContainer()
        if hasattr(script, 'container'):
            script.container = scriptContainer or self
        if scriptContainer:
            scriptContainer.addScript(script)
        elif self.parent:
            self.parent.addScript(script)
        else:
            self.__scriptTemp__ = self.__scriptTemp__ or []
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
            scriptTemp = self.__scriptTemp__
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
            self.__objectTemp__ = self.__objectTemp__ or []
            self.__objectTemp__.append(objectType)

    def __insertTemporaryScripts(self):
        """
            Moves scripts that were added to the WebElement but not a scriptContainer over to
            the set scriptContainer
        """
        scriptTemp = self.__scriptTemp__
        if scriptTemp:
            for script in scriptTemp:
                self.addScript(script)
            self.__scriptTemp__ = []

        objectTemp = self.__objectTemp__ or []
        if objectTemp:
            for objectType in objectTemp:
                self.addJSFunctions(objectType)
            self.__objectTemp__ = []

    def addClientSideEvent(self, event, python):
        """
            Attaches python code to be executed client-side when even occurs :: FEATURE STILL IN DEVELOPMENT ::
        """
        self.addJavascriptEvent(event, ToClientSide.convert(python))

    def removeClientSideEvent(self, event, python=None):
        """
            Removes previously attached python code from an event :: FEATURE STILL IN DEVELOPMENT ::
        """
        self.removeJavascriptEvent(event, python and ToClientSide.convert(python) or None)

    def addJavascriptEvent(self, event, javascript):
        """
            Adds a clientside action to be done on event:
                event - the name of the event to connect the javascript to (such as onclick)
                javascript - the script text or function to call on event
        """
        if hasattr(javascript, 'claim'):
            javascript = javascript.claim() + ";"
        if type(event) in (list, tuple):
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
        elif event in self.attributes:
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
        if not self._tagName:
            return u('')

        nativeAttributes = (('name', self.fullName()),
                            ('id', self.fullId()),
                            ('class', self._classes),
                            ('style', self._style),)
        startTag = "<" + self._tagName + " "

        attributes = nativeAttributes
        if self._attributes is not None:
            attributes = chain(attributes, iteritems(self.attributes))
        for key, value in attributes:
            value = interpretAsString(value)
            if value:
                if value == '_BLANK_':
                    value = ""

                if value == '_EMPTY_':
                    startTag += key + " "
                else:
                    startTag += key + '="' + value.replace('"', '&quot;') + '" '

        if self._tagSelfCloses:
            startTag += '/'
        else:
            startTag = startTag[:-1]
        startTag += '>'

        return unicode(startTag)

    def endTag(self):
        """
            Returns the elements html end tag, for example '</span>'
        """
        if self._tagSelfCloses or not self._tagName:
            return u('')

        return unicode("".join(("</", self._tagName, ">")))

    def content(self, formatted=False, *args, **kwargs):
        """
            returns the elements html content
            (the html bettween startTag and endTag)
        """
        if self._childElements is None:
            return ''

        elements = [element.toHTML(formatted=formatted, *args, **kwargs) for element in self.childElements]
        if formatted:
            return "\n".join([(self._tagName and Settings.INDENTATION or '') +
                               line for line in "\n".join(elements).split("\n") if line])
        else:
            return ''.join(elements)

    def insertVariables(self, variableDict=None):
        """
            Populate webElement and child webElements with (id/name/key):value dictionary:
                variableDict - the dictionary to use to populate the elements
        """
        if variableDict is None:
            variableDict = {}

        for child in self.childElements:
            child.insertVariables(variableDict)

    def exportVariables(self, exportedVariables=None, flat=False):
        """
            Export WebElement input field values as a nested key:value dictionary:
                exportedVariables - the dictionary to add exported variables to
        """
        if exportedVariables is None:
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

        for child in (child for child in self.childElements if type(child) != TextNode):
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
        for key, value in iteritems(dictionary):
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
        elif propertyAction == "send":
            objectWithProperty.__getattribute__(propertyName)(name, value)
        elif not hasattr(objectWithProperty, propertyAction):
            print("Trying to set " + propertyName + " using " + propertyAction + " but no" +
                    " such method or attribute exists on " + objectWithProperty.__class__.__name__)
        else:
            objectWithProperty.__getattribute__(propertyAction)(value)

    def setProperties(self, properties):
        """
            Loads element properties from a list of property name to value tuples
        """
        if isinstance(properties, dict):
            properties = iteritems(properties)

        for propertyName, propertyValue in properties:
            if propertyValue is not None and propertyName in self.properties:
                self.setProperty(propertyName, propertyValue)

    def _render(self):
        """
            Performs actions that need to be preformed at rendering time
        """
        self.emit("rendering")

    def toHTML(self, formatted=False, *args, **kwargs):
        """
           Returns the element(including child elements) as standard html
        """
        self._render()

        data = (self.startTag() or '', self.content(formatted, *args, **kwargs), self.endTag() or '')

        if formatted:
            html = "\n".join([data for data in data if data])
        else:
            html = "".join(data)

        return html

    def isBlockElement(self):
        """
            Returns true if the elements will render as an HTML block type
        """
        if self._tagName in Settings.BLOCK_TAGS or self.hasClass("WBlock"):
            return True
        return False

    def sanitize(self, inputValue):
        """
            Sanitizes direct user input, to protect against XSS attacks.
        """
        if type(inputValue) not in (str, unicode):
            return inputValue

        return cgi.escape(inputValue)

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
        return self.toHTML(formatted=True)

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
    __slots__ = ()
    tagName = "h2"
    allowsChildren = False

    def setProperties(self, valueDict):
        """
            Overrides the behavior of setProperties on invalid elements to do nothing.
        """
        pass

    def content(self, formatted=False, *args, **kwargs):
        """
            Overrides content to return 'Invalid element' string
        """
        return "Invalid Element"


class TextNode(object):
    """
        Defines the most basic concept of an html node - does not have the concept of children only of producing html
        should only be used internally or for testing objects
    """
    __slots__ = ('_text', 'parent')
    displayable = True
    tagName = ''
    _tagName = ''

    def __init__(self, text='', parent=None):
        self.setText(text)
        self.parent = parent

    def setText(self, text):
        """
            Sets the text associated with the text node.
        """
        self._text = text

    def text(self):
        """
            Returns the text associated with the text node.
        """
        return self._text

    def shown(self):
        """
            Text node elements are always visible
        """
        return True

    def toHTML(self, *args, **kwargs):
        """
            Returns the rendered html text node (simply a unicode version of the text).
        """
        return unicode(self.text())

    def insertVariables(self, *args, **kwargs):
        """
            Overrides insertVariables to do nothing when called on a text node.
        """
        pass

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.text()) + ")"

    def replaceWith(self, replacementElement):
        """
            Replaces this text node with a webelement
        """
        if self.parent:
            index = self.parent.childElements.index(self)
            self.parent.childElements[index] = replacementElement
            replacementElement.parent = self.parent
            return replacementElement
        else:
            return Invalid()


class TemplateElement(WebElement):
    """
        A template WebElement is a web element that uses a template for its presentation and
        structure
    """
    factory = None
    template = None

    def __init__(self, id=None, name=None, parent=None, template=None, factory=None, **kwargs):
        WebElement.__init__(self, id, name, parent, **kwargs)

        if template:
            self.template = template

        if factory:
            self.factory = factory

        accessors = {}
        instance = self.factory.buildFromTemplate(self.template, accessors=accessors, parent=self)
        for accessor, element in iteritems(accessors):
            if hasattr(self, accessor):
                raise ValueError("The accessor name or id of the element has to be unique and can not be the same as a"
                                 " base webelement attribute."
                                 "Failed on adding element with id or accessor '%s'." % accessor)

            self.__setattr__(accessor, element)

        self.addChildElement(instance)

