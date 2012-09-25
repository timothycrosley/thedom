#!/usr/bin/python
"""
   Name:
       Layout

   Description:
       Contains Elements that make it easy to layout pages exactly like you want.

"""

import Base
import Display
import Factory
from MethodUtils import CallBack

Factory = Factory.Factory("Layout")

class Center(Base.WebElement):
    """
        Makes childElements appear in the center of there parent element
    """
    __slots__ = ()
    tagName = "center"
Factory.addProduct(Center)


class Stack(Base.WebElement):
    """
       A stack is a container for child elements where only of the contained elements can be
       displayed at a time.
    """
    __slots__ = ('index', 'stackElements')
    properties = Base.WebElement.properties.copy()
    properties['index'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name, parent)
        self.index = 0
        self.stackElements = []

    def __setChildren__(self):
        visibleElement = self.visibleElement()
        if visibleElement:
            self._childElements = [self.visibleElement()]
        else:
            self._childElements = None

    def setVisibleElement(self, element):
        """
            Updates the index to show the givin element:
                element - the element to show
        """
        if element in self.stackElements:
            self.index = self.stackElements.index(element)
            self.__setChildren__()
            return True
        return False

    def visibleElement(self):
        """
            Returns the currently visible web element
        """
        if self.index >= 0 and self.index < len(self.stackElements):
            return self.stackElements[int(self.index)]
        elif self.stackElements:
            return self.stackElements[0]
        return None

    def toHtml(self, formatted=False):
        """
            Changes toHtml behavior to only generate the html for the visible element
        """
        if self.stackElements:
            return self.visibleElement().toHtml(formatted=formatted) or ""
        return ""

    def addChildElement(self, childElement, ensureUnique=True):
        self.stackElements.append(childElement)
        childElement.parent = self
        if len(self.stackElements) == 1:
            self.__setChildren__()
        return childElement

Factory.addProduct(Stack)


class Box(Base.WebElement):
    """
        A container that allows child elements to be contained within
       the border of the container.
    """
    __slots__ = ()
    properties = Base.WebElement.properties.copy()
    properties['containerType'] = {'action':'setContainerType'}
    tagName = "div"

    def setContainerType(self, container_type):
        """
            Change the container type to div (block) or span (inline)
        """
        if container_type in ["div", "span"]:
            self._tagName = container_type
            return True
        else:
            return False

    def containerType(self):
        """
            Returns the container type (div or span)
        """
        return self._tagName

Factory.addProduct(Box)


class Flow(Base.WebElement):
    """
        A container that does not impose a border around its childElements
       allowing them to flow freely.
    """
    __slots__ = ()
    tagName = None

Factory.addProduct(Flow)


class Horizontal(Box):
    """
        A container element that adds child elements horizontally.
    """
    __slots__ = ()
    def __init__(self, id=None, name=None, parent=None):
        Box.__init__(self, id, name, parent)
        self.addClass("ClearFix")

    def addChildElement(self, childElement, align=None, width=None, style=None, ensureUnique=True):
        if width is not None:
            childElement.widthPreference = width
        if style is not None:
            childElement.stylePreference = style
        if align is not None:
            childElement.align = align

        return Box.addChildElement(self, childElement, ensureUnique=ensureUnique)

    def __modifyChild__(self, childElement):
        width = getattr(childElement, 'widthPreference', '')
        align = getattr(childElement, 'alignPreference', 'left')
        style = getattr(childElement, 'stylePreference', {})

        if width == "0" or width == "hide":
            self.childElements.append(childElement)
        if not childElement.displayable:
            self.childElements.append(childElement)
            return
        if not childElement.tagName:
            container = Box.addChildElement(self, Box())
            container.addChildElement(childElement)
        else:
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            container = childElement
            self.childElements.append(childElement)

        container.style['float'] = align
        if width:
            container.style['vertical-align'] = 'middle'
            container.style['width'] = width

        if style:
            container.style.update(style)

    def toHtml(self, formatted=False):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        returnValue = Box.toHtml(self, formatted=formatted)
        self._childElements = oldChildElements
        return returnValue

Factory.addProduct(Horizontal)


class Vertical(Box):
    """
        A container that encourage elements to be added vertically with minimum html
    """
    __slots__ = ()
    def __init__(self, id=None, name=None, parent=None):
        Box.__init__(self, id, name, parent)
        self.addClass("ClearFix")

    def addChildElement(self, childElement, style=None, ensureUnique=True):
        if style:
            childElement.style.update(style)
        return Box.addChildElement(self, childElement, ensureUnique=ensureUnique)

    def __modifyChild__(self, childElement):
        if not childElement.displayable:
            self.childElements.append(childElement)
        elif childElement.tagName:
            childElement.style['clear'] = "both"
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            self.childElements.append(childElement)
        else:
            container = Box()
            container.style['clear'] = "both"
            container.addChildElement(childElement)
            return Box.addChildElement(self, container)

    def toHtml(self, formatted=False):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        returnValue = Box.toHtml(self, formatted=formatted)
        self._childElements = oldChildElements
        return returnValue

Factory.addProduct(Vertical)


class FieldSet(Box):
    """
        Groups child elements together with a labeled border
    """
    __slots__ = ('legend')
    tagName = 'fieldset'
    Box.properties['legend'] = {'action':'setLegend'}

    def __init__(self, id=None, name=None, parent=None):
        Box.__init__(self, id, name, parent)
        self.legend = None

    def addLegend(self):
        """
            Adds and returns the legend to the field set
        """
        if self.legend:
            return
        l = Base.WebElement()
        self.legend = Box.addChildElement(self, l)

    def setLegend(self, legend):
        """
            Sets the label associated to the elements by adding a labeled legend
        """
        self.addLegend()
        self.legend.tagName = 'legend'
        self.legend.addChildElement(Base.TextNode(legend))

Factory.addProduct(FieldSet)


class Fields(Box):
    """
        Automatically lays out fields in a grid
    """
    __slots__ = ('fields', 'labels', 'inputs', 'fieldHeight', '__showErrorsOnRight__')
    properties = Box.properties.copy()
    properties['labelsStyle'] = {'action':'labels.setStyleFromString'}
    properties['inputsStyle'] = {'action':'inputs.setStyleFromString'}
    properties['showErrorsOnRight'] = {'action':'call', 'name':'showErrorsOnRight', 'type':'bool'}
    properties['fieldHeight'] = {'action':'classAttribute'}

    def __init__(self, id=None, name=None, parent=None):
        Box.__init__(self, id, name, parent)
        self.fields = self.addChildElement(Display.BlankRendered())

        layout = self.addChildElement(Horizontal())
        self.labels = layout.addChildElement(Vertical())
        self.inputs = layout.addChildElement(Vertical())

        self.fieldHeight = "3.5em"
        self.__showErrorsOnRight__ = False

    def showErrorsOnRight(self):
        """
            Moves errors over to the right (instead of directly below) the inputs
        """
        self.fieldHeight = "2em"
        self.__showErrorsOnRight__ = True

    def addChildElement(self, element):
        if hasattr(element, 'label') and hasattr(element, 'userInput'):
            fieldHeight = element.style.get('height', self.fieldHeight)
            label = self.labels.addChildElement(element.label)
            if not label.style.get('height'):
                label.style['height'] = fieldHeight
            if self.__showErrorsOnRight__:
                inputWithErrorLayout = self.inputs.addChildElement(Horizontal())
            else:
                inputWithErrorLayout = self.inputs.addChildElement(Vertical())
            inputLayout = inputWithErrorLayout.addChildElement(Horizontal())
            inputLayout.addChildElement(element.userInput)
            inputLayout.addChildElement(element.fieldActions)
            inputWithErrorLayout.addChildElement(element.formError)
            inputWithErrorLayout.style['height'] = fieldHeight
            element.connect('hidden', None, label, 'hide')
            element.connect('hidden', None, inputWithErrorLayout, 'hide')
            element.connect('shown', None, label, 'show')
            element.connect('shown', None, inputWithErrorLayout, 'show')
            element.connect('editableChanged', None, label, 'setEditable')
            element.connect('editableChanged', None, inputWithErrorLayout, 'setEditable')
            if not element.shown():
                element.emit("hidden")
            return self.fields.addChildElement(element)

        return Box.addChildElement(self, element)

Factory.addProduct(Fields)


class Grid(Box):
    """
        Automatically lays out elements in a grid without using tables
    """
    __slots__ = ('rowHeight', 'numberOfColumns', 'uniformStyle', 'layout')
    properties = Box.properties.copy()
    properties['rowHeight'] = {'action':'classAttribute'}
    properties['uniformStyle'] = {'action':'classAttribute'}
    properties['numberOfColumns'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id=None, name=None, parent=None):
        Box.__init__(self, id, name, parent)

        self.rowHeight = None
        self.numberOfColumns = 2
        self.uniformStyle = ""

        self.connect("beforeToHtml", None, self, "__applyLayout__")

    def __applyLayout__(self):
        self.numberOfColumns = int(self.numberOfColumns)

        columns = []
        for columnIndex in xrange(self.numberOfColumns):
            columns.append(Vertical())

        columnIndex = 0
        for element in self:
            style = self.rowHeight and {'height':self.rowHeight} or {}
            columns[columnIndex].addChildElement(element, ensureUnique=False, style=style)
            if self.uniformStyle:
                element.setStyleFromString(self.uniformStyle)

            columnIndex += 1
            if columnIndex >= self.numberOfColumns:
                columnIndex = 0

        self.layout = Horizontal(parent=self)
        for column in columns:
            self.layout += column

    def content(self, formatted=False):
        return self.layout.toHtml(formatted=formatted)

Factory.addProduct(Grid)


class LineBreak(Box):
    """
        Forces a newline below all divs
        Like a more forceful <br/>
    """
    __slots__ = ()

    def __init__(self, name=None, id=None, parent=None):
        Box.__init__(self, '', None, parent)
        self.addChildElement(Base.TextNode("&nbsp;"))
        self.style['clear'] = 'both'
        self.style['height'] = '0px'

Factory.addProduct(LineBreak)


class HorizontalRule(Base.WebElement):
    """
        Defines a 'hr' webelement - a line drawn between 2 elements horizontally
    """
    __slots__ = ()
    tagName = 'hr'
    allowsChildren = False
    tagSelfCloses = True

Factory.addProduct(HorizontalRule)


class VerticalRule(Base.WebElement):
    """
        Defines a vertical rule break - a line drawn between 2 elements vertically
    """
    __slots__ = ('stylePreference')
    tagName = 'span'
    allowsChildren = False

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name, parent)
        self.stylePreference = {'height':'100%'}
        self.addClass("WVerticalRule")

Factory.addProduct(VerticalRule)
