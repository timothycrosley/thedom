'''
    ClientSide.py

    Convenience python functions that return JavaScript code -
    including complete python bindings for WebElements.js

    NOTE: documentation for the binding functions is defined in WebElement.js and not as doc strings on the binding
    methods themselves.

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

import json

from .MultiplePythonSupport import *

class Script(object):
    __slots__ = ('content', 'container')

    def __init__(self, content, container=None):
        self.content = content
        self.container = container

    def check(self):
        return Block(self)

    def inlineFunction(self, accepts=()):
        return inlineFunction(self, accepts)

    def __str__(self):
        return self.content

    @property
    def length(self):
        return Script("%s.length" % var(self))

    def __enter__(self):
        self.content += "{"
        return self

    def __exit__(self, type, value, traceback):
        if self.content[-1] != "{":
            self.content += ";"
        self.content += "}"

    def push(self, value):
        return call(self.claim() + "." + push, value)

    def pop(self):
        return call(self.claim() + "." + pop)

    def __getitem__(self, key):
        return Script("%s[%s]" % (self.claim(), var(key)))

    def __getattr__(self, name):
        return Script("%s.%s" % (var(self), name))

    def __setattr__(self, name, value):
        if name in self.__class__.__slots__:
            return object.__setattr__(self, name, value)
        self.content = "%s.%s = %s" % (var(self), name, var(value))

    def __contains__(self, item):
        return Script(ClientSide.contains(self.claim(), var(item)))

    def __call__(self, other=None):
        if not other:
            return str(self)

        if self.content and self.content[-1] != "{":
            self.content += ";"
        self.content += var(other)
        return self

    def do(self, name=None, *args):
        return call(self.claim() + (name and "." + name or ""), *args)

    def RETURN(self, data=None):
        if data is not None:
            return self(Script("return %s" % var(data)))
        return Script("return %s" % var(self))

    @property
    def IF(self):
        return If(self)

    def claim(self):
        if self.container:
            self.container.removeScript(self)
        return self.content

    def copy(self):
        return self.__class__(self.claim())


class Keys(object):
    """
        Defines a mapping of all clientside keys to their int values
    """
    SPACE = 32
    ENTER = 13
    TAB = 9
    ESC = 27
    BACKSPACE = 8
    SHIFT = 16
    CONTROL = 17
    ALT = 18
    CAPSLOCK = 20
    NUMLOCK = 144
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40
    HOME = 36
    END = 35
    PAGE_UP = 33
    PAGE_DOWN = 34
    INSERT = 45
    DELETE = 46
    FUNCTIONS = [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123]
    NUMBERS = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]


class MessageTypes(object):
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    CLASS_MAP= {ERROR:'WError', INFO:'WInfo', WARNING:'WWarning', SUCCESS:'WSuccess'}
    CLASSES = Script("MessageTypes.CLASSES")
    CLASS_LIST = Script("MessageTypes.CLASS_LIST")


class If(object):
    __slots__ = ('script')

    def __init__(self, script):
        self.script = script

    @property
    def exists(self):
        return Script("if(%s)" % (var(self.script)))

    @property
    def notExists(self):
        return Script("if(!%s)" % (var(self.script)))

    def IS(self, other):
        return Script("if(%s === %s)" % (var(self.script), var(other)))

    def IS_NOT(self, other):
        return Script("if(%s !== %s)" % (var(self.script), var(other)))

    def __eq__(self, other):
        return Script("if(%s == %s)" % (var(self.script), var(other)))

    def __ne__(self, other):
        return Script("if(%s != %s)" % (var(self.script), var(other)))

    def __lt__(self, other):
        return Script("if(%s < %s)" % (var(self.script), var(other)))

    def __le__(self, other):
        return Script("if(%s <= %s)" % (var(self.script)), var(other))

    def __gt__(self, other):
        return Script("if(%s > %s)" % (var(self.script), var(other)))

    def __ge__(self, other):
        return Script("if(%s >= %s)" % (var(self.script), var(other)))


def var(variable):
    """
        returns a javascript representation of a variable
    """
    if isinstance(variable, Script):
        return variable.claim()
    if hasattr(variable, 'id'):
        return json.dumps(variable.id)
    if type(variable) in (list, tuple, set):
        return "[" + ",".join(var(item) for item in variable) + "]"
    if isinstance(variable, dict):
        return "{" + ",".join(["%s:%s," % (var(key), var(value)) for key, value in iteritems(variable)]) + "}"
    return json.dumps(variable)

def varList(*args):
    """
        returns a javascript representation of a list of arguments for passing into methods
    """
    return "(%s)" % ",".join([var(variable) for variable in args])

def call(functionName, *args):
    """
        returns a javascript representation of calling a method
    """
    return Script(functionName + varList(*args))

def inlineFunction(script, accepts=()):
    """
        returns a javascript inline function
    """
    return Script("function(%s){%s}" % (",".join(accepts), var(script)))

def check(script):
    """
        Creates a client side if conditional
    """
    return Script("if(%s)" % (var(script),))

def eventHandler(script):
    """
        returns a javascript inline function that takes an evt as its only argument
    """
    return inlineFunction(script, accepts=('evt',))

def assign(name, value):
    return Script("%s = %s" % (name, var(value)))

def regexp(value):
    return Script("/%s/" % (value.pattern, ))

THIS = Script("this")
DOCUMENT = Script("document")

### WebElements.js bindings follow - doc strings are contained within javascript code

def addEvent(element, eventType, handler):
    return call("WebElements.Events.addEvent", element, eventType, handler)

def removeEvent(element, eventType, handler):
    return call("WebElements.Events.removeEvent", element, eventType, handler)

def get(element):
    return call("WebElements.get", element)

def forEach(arrayOfItems, callBack):
    return call("WebElements.forEach", arrayOfItems, callBack)

def onEach(arrayOfItems, callBack):
    return call("WebElements.map", arrayOfItems, callBack)

def sortElements(elements):
    return call("WebElements.sortElements", elements)

def sortUnique(elements):
    return call("WebElements.sortUnique", elements)

def getElementsByTagNames(tagNames, parentElement=DOCUMENT, unsorted=True):
    return call("WebElements.getElementsByTagNames", tagNames, parentElement, unsorted)

def getByCondition(conditional, parentNode=DOCUMENT, stopOnFirstMatch=False):
    return call("WebElements.getByCondition", conditional, parentNode, stopOnFirstMatch)

def getValue(element):
    return call("WebElements.getValue", element)

def hideClass(className, parentNode=DOCUMENT):
    return call("WebElements.hideClass", className, parentNode)

def showClass(className, parentNode=DOCUMENT):
    return call("WebElements.showClass", className, parentNode)

def buildThrobber():
    return call("WebElements.buildThrobber")

def getElementsByClassName(className, parentNode=DOCUMENT, stopOnFirstMatch=False):
    return call("WebElements.getElementsByClassName", className, parentNode, stopOnFirstMatch)

def getElementByClassName(className, parentNode=DOCUMENT):
    return call("WebElements.getElementByClassName", className, parentNode)

def getChildrenByAttribute(parentNode, attributeName, attributeValue):
    return call("WebElements.getElementsByAttribute", parentNode, attributeName, attributeValue)

def getChildByAttribute(parentNode, attributeName, attributeValue):
    return call("WebElements.getChildByAttribute", parentNode, attributeName, attributeValue)

def getChildrenByName(parentNode, name):
    return call("WebElements.getChildrenByName", parentNode, name)

def getChildByName(parentNode, name):
    return call("WebElements.getChildByName", parentNode, name)

def populate(fieldDict):
    return call("WebElements.populate", fieldDict)

def countDown(label, seconds, action):
    return call("WebElements.countDown", label, seconds, action)

def abortCountDown(label):
    return call("WebElements.abortCountDown", label)

def pixelsToLeft(element):
    return call("WebElements.pixelsToLeft", element)

def pixelsAbove(element):
    return call("WebElements.pixelsAbove", element)

def setAbsoluteRelativeToParent(element, pixelsDown=0, pixelsToRight=0, parentElement=None):
    return call("WebElements.setAbsoluteRelativeToParent", element, pixelsDown, pixelsToRight, parentElement)

def displayDropDown(dropDown, parentElement=None):
    return call("WebElements.displayDropDown", dropDown, parentElement)

def toggleDropDown(dropDown, parentElement=None):
    return call("WebElements.toggleDropDown", dropDown, parentElement)

def openAccordion(accordionName):
    return call("WebElements.openAccordion", accordionName)

def fellowChild(element, parentClass, childClass):
    return call("WebElements.fellowChild", element, parentClass, childClass)

def firstChild(element):
    return call("WebElements.firstChild", element)

def lastChild(element):
    return call("WebElements.lastChild", element)

def nextSibling(element):
    return call("WebElements.next", element)

def prevSibling(element):
    return call("WebElements.prev", element)

def increment(element, max=None):
    return call("WebElements.increment", element, max)

def defincrement(element, min=None):
    return call("WebElements.deincrement", element, min)

def setPrefix(container, prefix):
    return call("WebElements.setPrefix", container, prefix)

def parent(element, className, giveUpAtClass=False):
    return call("WebElements.parent", className, giveUpAtClass)

def clearChildren(element, replacement=None):
    return call("WebElements.clearChildren", element, replacement)

def childElements(parentElement):
    return call("WebElements.childElements", parentElement)

def peer(element, className):
    return call("WebElements.peer", element, className)

def peers(element, className):
    return call("WebElements.peers", element, className)

def stealClassFromPeer(element, className):
    return call("WebElements.stealClassFromPeer", element, className)

def stealClassFromFellowChild(element, parentClassName, className):
    return call("WebElements.stealClassFromFellowChild", element, parentClassName, className)

def hide(element):
    return call("WebElements.hide", element)

def show(element):
    return call("WebElements.show", element)

def toggleVisibility(element):
    return call("WebElements.toggleVisibility", element)

def elementShown(element):
    return call("WebElements.elementShown", element)

def replace(element, newElement):
    return call("WebElements.replace", element, newElement)

def remove(element):
    return call("WebElements.remove", element)

def clear(element):
    return call("WebElements.clear", element)

def addOption(selectElement, optionName, optionValue=None):
    return call("WebElements.addOption", element, optionName, optionValue)

def addOptions(selectElement, options):
    return call("WebElements.addOptions", options)

def addHtml(element, html):
    return call("WebElements.addHtml", element, html)

def move(element, to):
    return call("WebElements.move", element, to)

def copy(element, to, incrementId=False):
    return call("WebElements.copy", element, to, incrementId)

def contains(text, subtext, caseSensitive=False):
    return call("WebElements.contains", text, subtext, caseSensitive)

def startsWith(text, subtext, caseSensitive=False):
    return call("WebElements.startsWith", text, subtext, caseSensitive)

def addPrefix(container, prefix):
    return call("WebElements.addPrefix", container, prefix)

def sortSelect(selectElement, sortByValue=False):
    return call("WebElements.sortSelect", selectElement, sortByValue)

def removeDuplicates(array):
    return call("WebElements.removeDuplicates", array)

def selectedOptions(selectBox):
    return call("WebElements.selectedOptions", selectBox)

def selectAllOptions(selectBox):
    return call("WebElements.selectAllOptions", selectBox)

def setOptions(selectBox, options):
    return call("WebElements.setOptions", selectBox, options)

def selectAllCheckboxes(container, check=True):
    return call("WebElements.selectAllCheckboxes", container, check)

def getValues(container, checkSelected=False, tagName="option"):
    return call("WebElements.getValues", container, checkSelected, tagName)

def getElementByValue(element, value):
    return call("WebElements.getElementByValue", element, value)

def getElementByInnerHTML(element, html):
    return call("WebElements.getElementByInnerHTML", element, value)

def selectedOption(selectBox):
    return call("WebElements.selectedOption", selectBox)

def selectOption(selectBox, option):
    return call("WebElements.selectOption", selectBox, option)

def replaceAll(string, toReplace, replacement):
    return call("WebElements.replaceAll", string, toReplace, replacement)

def classes(element):
    return call("WebElements.classes", element)

def hasClass(element, className):
    return call("WebElements.hasClass", element, className)

def setClasses(element, classList):
    return call("WebElements.setClasses", element, classList)

def removeClass(element, classToRemove):
    return call("WebElements.removeClass", element, classToRemove)

def addClass(element, classToAdd):
    return call("WebElements.addClass", element, classToAdd)

def removeFromArray(arrayOfItems, toRemove):
    return call("WebElements.removeFromArray", arrayOfItems, toRemove)

def chooseClass(element, classes, choice):
    return call("WebElements.chooseClass", element, classes, choice)

def redraw(element):
    return call("WebElements.redraw", element)

def strip(string):
    return call("WebElements.strip", element)

def stripLeadingZeros(string):
    return call("WebElements.stripLeadingZeros", string)

def inList(array, value):
    return call("WebElements.inList", array, value)

def appendOnce(array, item):
    return call("WebElements.appendOnce", array, item)

def combine(array1, array2):
    return call("WebElements.combine", array1, array2)

def suppress(element, attribute):
    return call("WebElements.suppress", element, attribute)

def unsuppress(element, attribute):
    return call("WebElements.unsuppress", element, attribute)

def toggleMenu(button):
    return call("WebElements.toggleMenu", button)

def closeMenu():
    return call("WebElements.closeMenu")

def selectText(element, start, end):
    return call("WebElements.selectText", element, start, end)

def openPopup(url, width=700, height=700, normal=False, windowTitle="_blank", options=None):
    return call("WebElements.openPopup", windowTitle, url, width, height, normal, options)

def scrolledToBottom(scroller):
    return call("WebElements.scrolledToBottom", scroller)

def toggleClass(element, className):
    return call("WebElements.toggleClass", element, className)

def toggleTableRowSelect(checkbox):
    return call("WebElements.toggleTableRowSelect", checkbox)

def getNotificationPermission():
    return call("WebElements.getNotificationPermission")

def showNotification(title, content, icon="images/info.png"):
    return call("WebElements.showNotification", title, content, icon)

def checkboxActsLikeRadioButton(element, pair):
    return call("WebElements.checkboxActsLikeRadioButton", element, pair)

def stopOperation(event):
    return call("WebElements.stopOperation", event)

def buildFileOpener(dropBox):
    return call("WebElements.buildFileOpener", dropBox)

def clickDropDown(menu, openOnly, button, parentElement):
    return call("WebElements.clickDropDown", menu, openOnly, button, parentElement)

def serialize(field):
    return call("WebElements.serialize", field)

def serializeElements(elements):
    return call("WebElements.serializeElements", elements)

def serializeAll(container=DOCUMENT):
    return call("WebElements.serializeAll", container)

def confirm(message, action):
    return call("WebElements.confirm", message, inlineFunction(action))

def callOpener(method):
    return call("WebElements.callOpener", method)

def updateParent():
    return call("WebElements.updateParent")

def focus(element, selectText=False):
    return call("WebElements.focus", element, selectText)

def setValue(element, value):
    return call("WebElements.setValue", element, value)

def redirect(to):
    return Script("window.location = %s" % var(to))

def showIfSelected(option, elementToShow, element=THIS):
    return call("WebElements.showIfSelected", element, option, elementToShow)

def showIfChecked(elementToShow, checkbox=THIS):
    return call("WebElements.showIfChecked", checkbox, elementToShow)

def expandTemplate(template, valueDictionary):
    return call("WebElements.expandTemplate", template, valueDictionary)

class doClientSide(object):
    """
        A magical class that will run a method client side without knowledge of the method signature
    """
    __slots__ = "method"

    def __init__(self, method=''):
        self.method = method

    def __getattr__(self, name):
        return self.__class__((self.method and self.method + "." or "") + name)

    def __call__(self, *args):
        return call(self.method, *args)

do = doClientSide()
