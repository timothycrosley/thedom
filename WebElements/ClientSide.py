"""
    Convience python functions that return javascript code -
    including complete bindings for WebElements.js
"""

import json

class Script(object):
    __slots__ = ('content', 'container')

    def __init__(self, content, container=None):
        self.content = content
        self.container = container

    def __str__(self):
        return self.content

    def claim(self):
        if self.container:
            self.container.removeScript(self)
        return self.content

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

def eventHandler(script):
    """
        returns a javascript inline function that takes an evt as its only argument
    """
    return inlineFunction(script, accepts=('evt',))

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

def stealClassFromPeer(element, className):
    return call("WebElements.steelClassFromPeer", element, className)

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
