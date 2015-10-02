'''
    ClientSide.py

    Convenience python functions that return JavaScript code -
    including complete python bindings for thedom.js

    NOTE: documentation for the binding functions is defined in thedom.js and not as doc strings on the binding
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
        self.content = "%s.%s = %s" % (self.content, name, var(value))
        return self

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
        return "{" + ",".join(["%s:%s" % (var(key), var(value)) for key, value in iteritems(variable)]) + "}"
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
EVENT = Script("event")
DOCUMENT = Script("document")
WINDOW = Script("window")
STOP_EVENT = Script("thedom.stopOperation")

### thedom.js bindings follow - doc strings are contained within javascript code

def addEvent(element, eventType, handler):
    return call("thedom.Events.addEvent", element, eventType, handler)

def removeEvent(element, eventType, handler):
    return call("thedom.Events.removeEvent", element, eventType, handler)

def get(element):
    return call("thedom.get", element)

def forEach(arrayOfItems, callBack):
    return call("thedom.forEach", arrayOfItems, callBack)

def onEach(arrayOfItems, callBack):
    return call("thedom.map", arrayOfItems, callBack)

def sortElements(elements):
    return call("thedom.sortElements", elements)

def sortUnique(elements):
    return call("thedom.sortUnique", elements)

def getElementsByTagNames(tagNames, parentElement=DOCUMENT, unsorted=True):
    return call("thedom.getElementsByTagNames", tagNames, parentElement, unsorted)

def getByCondition(conditional, parentNode=DOCUMENT, stopOnFirstMatch=False):
    return call("thedom.getByCondition", conditional, parentNode, stopOnFirstMatch)

def getValue(element):
    return call("thedom.getValue", element)

def hideClass(className, parentNode=DOCUMENT):
    return call("thedom.hideClass", className, parentNode)

def showClass(className, parentNode=DOCUMENT):
    return call("thedom.showClass", className, parentNode)

def buildThrobber():
    return call("thedom.buildThrobber")

def becomeThrobber(element=THIS):
    return call("thedom.becomeThrobber", element)

def getElementsByClassName(className, parentNode=DOCUMENT, stopOnFirstMatch=False):
    return call("thedom.getElementsByClassName", className, parentNode, stopOnFirstMatch)

def getElementByClassName(className, parentNode=DOCUMENT):
    return call("thedom.getElementByClassName", className, parentNode)

def directChildren(parent):
    return call("thedom.directChildren", parent)

def directChildrenWithClass(parent, className):
    return call("thedom.directChildrenWithClass", parent, className)

def directChild(parent, className):
    return call("thedom.directChild", parent, className)

def getChildrenByAttribute(parentNode, attributeName, attributeValue):
    return call("thedom.getElementsByAttribute", parentNode, attributeName, attributeValue)

def getChildByAttribute(parentNode, attributeName, attributeValue):
    return call("thedom.getChildByAttribute", parentNode, attributeName, attributeValue)

def getChildrenByName(parentNode, name):
    return call("thedom.getChildrenByName", parentNode, name)

def getChildByName(parentNode, name):
    return call("thedom.getChildByName", parentNode, name)

def populate(fieldDict):
    return call("thedom.populate", fieldDict)

def countDown(label, seconds, action):
    return call("thedom.countDown", label, seconds, action)

def abortCountDown(label):
    return call("thedom.abortCountDown", label)

def pixelsToLeft(element):
    return call("thedom.pixelsToLeft", element)

def pixelsAbove(element):
    return call("thedom.pixelsAbove", element)

def setAbsoluteRelativeToParent(element, pixelsDown=0, pixelsToRight=0, parentElement=None):
    return call("thedom.setAbsoluteRelativeToParent", element, pixelsDown, pixelsToRight, parentElement)

def displayDropDown(dropDown, parentElement=None):
    return call("thedom.displayDropDown", dropDown, parentElement)

def toggleDropDown(dropDown, parentElement=None):
    return call("thedom.toggleDropDown", dropDown, parentElement)

def openAccordion(accordionName):
    return call("thedom.openAccordion", accordionName)

def fellowChild(element, parentClass, childClass):
    return call("thedom.fellowChild", element, parentClass, childClass)

def firstChild(element):
    return call("thedom.firstChild", element)

def lastChild(element):
    return call("thedom.lastChild", element)

def nextSibling(element):
    return call("thedom.next", element)

def prevSibling(element):
    return call("thedom.prev", element)

def increment(element, max=None):
    return call("thedom.increment", element, max)

def defincrement(element, min=None):
    return call("thedom.deincrement", element, min)

def setPrefix(container, prefix):
    return call("thedom.setPrefix", container, prefix)

def parent(element, className, giveUpAtClass=False):
    return call("thedom.parent", element, className, giveUpAtClass)

def clearChildren(element, replacement=None):
    return call("thedom.clearChildren", element, replacement)

def childElements(parentElement):
    return call("thedom.childElements", parentElement)

def peer(element, className):
    return call("thedom.peer", element, className)

def peers(element, className):
    return call("thedom.peers", element, className)

def stealClassFromPeer(element, className):
    return call("thedom.stealClassFromPeer", element, className)

def stealClassFromFellowChild(element, parentClassName, className):
    return call("thedom.stealClassFromFellowChild", element, parentClassName, className)

def stealClassFromContainer(element, container, className):
    return call("thedom.stealClassFromContainer", element, container, className)

def hide(element):
    return call("thedom.hide", element)

def show(element):
    return call("thedom.show", element)

def toggleVisibility(element):
    return call("thedom.toggleVisibility", element)

def elementShown(element):
    return call("thedom.elementShown", element)

def replace(element, newElement):
    return call("thedom.replace", element, newElement)

def remove(element):
    return call("thedom.remove", element)

def clear(element):
    return call("thedom.clear", element)

def addOption(selectElement, optionName, optionValue=None):
    return call("thedom.addOption", element, optionName, optionValue)

def addOptions(selectElement, options):
    return call("thedom.addOptions", options)

def addHtml(element, html):
    return call("thedom.addHtml", element, html)

def move(element, to, makeTop=False):
    return call("thedom.move", element, to, makeTop)

def copy(element, to, incrementId=False):
    return call("thedom.copy", element, to, incrementId)

def contains(text, subtext, caseSensitive=False):
    return call("thedom.contains", text, subtext, caseSensitive)

def endsWith(text, subtext):
    return call("thedom.endsWith", text, subtext)

def startsWith(text, subtext, caseSensitive=False):
    return call("thedom.startsWith", text, subtext, caseSensitive)

def addPrefix(container, prefix):
    return call("thedom.addPrefix", container, prefix)

def sortSelect(selectElement, sortByValue=False):
    return call("thedom.sortSelect", selectElement, sortByValue)

def removeDuplicates(array):
    return call("thedom.removeDuplicates", array)

def selectedOptions(selectBox):
    return call("thedom.selectedOptions", selectBox)

def selectAllOptions(selectBox):
    return call("thedom.selectAllOptions", selectBox)

def setOptions(selectBox, options):
    return call("thedom.setOptions", selectBox, options)

def selectAllCheckboxes(container, check=True):
    return call("thedom.selectAllCheckboxes", container, check)

def getValues(container, checkSelected=False, tagName="option"):
    return call("thedom.getValues", container, checkSelected, tagName)

def getElementByValue(element, value):
    return call("thedom.getElementByValue", element, value)

def getElementByInnerHTML(element, html):
    return call("thedom.getElementByInnerHTML", element, value)

def selectedOption(selectBox):
    return call("thedom.selectedOption", selectBox)

def selectOption(selectBox, option):
    return call("thedom.selectOption", selectBox, option)

def replaceAll(string, toReplace, replacement):
    return call("thedom.replaceAll", string, toReplace, replacement)

def classes(element):
    return call("thedom.classes", element)

def hasClass(element, className):
    return call("thedom.hasClass", element, className)

def setClasses(element, classList):
    return call("thedom.setClasses", element, classList)

def removeClass(element, classToRemove):
    return call("thedom.removeClass", element, classToRemove)

def addClass(element, classToAdd):
    return call("thedom.addClass", element, classToAdd)

def addClasses(element, classesToAdd):
    return call("thedom.addClasses", element, classesToAdd)

def removeFromArray(arrayOfItems, toRemove):
    return call("thedom.removeFromArray", arrayOfItems, toRemove)

def chooseClass(element, classes, choice):
    return call("thedom.chooseClass", element, classes, choice)

def redraw(element):
    return call("thedom.redraw", element)

def strip(string):
    return call("thedom.strip", element)

def stripLeadingZeros(string):
    return call("thedom.stripLeadingZeros", string)

def inList(array, value):
    return call("thedom.inList", array, value)

def appendOnce(array, item):
    return call("thedom.appendOnce", array, item)

def combine(array1, array2):
    return call("thedom.combine", array1, array2)

def suppress(element, attribute):
    return call("thedom.suppress", element, attribute)

def unsuppress(element, attribute):
    return call("thedom.unsuppress", element, attribute)

def toggleMenu(button):
    return call("thedom.toggleMenu", button)

def closeMenu():
    return call("thedom.closeMenu")

def disableChildren(parentElement):
    return call("thedom.disableChildren", parentElement)

def selectText(element, start, end):
    return call("thedom.selectText", element, start, end)

def openPopup(url, width=700, height=700, normal=False, windowTitle="_blank", options=None):
    return call("thedom.openPopup", windowTitle, url, width, height, normal, options)

def scrolledToBottom(scroller):
    return call("thedom.scrolledToBottom", scroller)

def toggleClass(element, className):
    return call("thedom.toggleClass", element, className)

def toggleTableRowSelect(checkbox):
    return call("thedom.toggleTableRowSelect", checkbox)

def getNotificationPermission():
    return call("thedom.getNotificationPermission")

def showNotification(title, content, icon="images/info.png"):
    return call("thedom.showNotification", title, content, icon)

def checkboxActsLikeRadioButton(element, pair):
    return call("thedom.checkboxActsLikeRadioButton", element, pair)

def stopOperation(event):
    return call("thedom.stopOperation", event)

def stopInline(event=EVENT):
    return call("thedom.stopInline", event)

def buildFileOpener(dropBox):
    return call("thedom.buildFileOpener", dropBox)

def clickDropDown(menu, openOnly, button, parentElement):
    return call("thedom.clickDropDown", menu, openOnly, button, parentElement)

def serialize(field):
    return call("thedom.serialize", field)

def serializeElements(elements):
    return call("thedom.serializeElements", elements)

def serializeAll(container=DOCUMENT):
    return call("thedom.serializeAll", container)

def confirm(message, action, attach=THIS):
    return call("thedom.confirm", message, inlineFunction(action, accepts=('element', )), attach)

def callOpener(method):
    return call("thedom.callOpener", method)

def updateParent():
    return call("thedom.updateParent")

def focus(element, selectText=False):
    return call("thedom.focus", element, selectText)

def setValue(element, value):
    return call("thedom.setValue", element, value)

def redirect(to):
    return Script("window.location = %s" % var(to))

def showIfSelected(option, elementToShow, element=THIS):
    return call("thedom.showIfSelected", element, option, elementToShow)

def showIfChecked(elementToShow, checkbox=THIS):
    return call("thedom.showIfChecked", checkbox, elementToShow)

def expandTemplate(template, valueDictionary):
    return call("thedom.expandTemplate", template, valueDictionary)

def createCalendar(element):
    return call("thedom.createCalendar",{'field':get(element)})

def onPagerChange(pager, callBack):
    return call("thedom.onPagerChange", pager, inlineFunction(callBack, accepts=('params', )))

def timezone():
    return call("thedom.timezone")

def setCookie(name, value):
    return call("thedom.setCookie", name, value)

def getCookie(name):
    return call("thedom.getCookie", name)

def openAccordion(content, image, value):
    return openAccordion("thedom.openAccordion", content, image, value)

def closeAccordion(content, image, value):
    return openAccordion("thedom.closeAccordion", content, image, value)

def toggleAccordion(content, image, value):
    return call("thedom.toggleAccordion", content, image, value)

def setAttribute(instance, name, value):
    return Script("%s.%s = %s" % (instance, name, var(value)))

def selectTab(tab):
    return call("thedom.selectTab", tab)

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
