#!/usr/bin/python
"""
   Name:
       Layout

   Description:
       Contains Elements that make it easy to layout pages exactly like you want.

"""

import Base
import DOM
import Display
import Factory
from MethodUtils import CallBack

Factory = Factory.Factory("Layout")


class Stack(Base.WebElement):
    """
       A stack is a container for child elements where only of the contained elements can be
       displayed at a time.
    """
    __slots__ = ('index', 'stackElements')
    properties = Base.WebElement.properties.copy()
    properties['index'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Base.WebElement.__init__(self, id, name, parent, **kwargs)
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

    def toHtml(self, formatted=False, *args, **kwargs):
        """
            Changes toHtml behavior to only generate the html for the visible element
        """
        if self.stackElements:
            return self.visibleElement().toHtml(formatted=formatted, *args, **kwargs) or ""
        return ""

    def addChildElement(self, childElement, ensureUnique=True):
        self.stackElements.append(childElement)
        childElement.parent = self
        if len(self.stackElements) == 1:
            self.__setChildren__()
        return childElement

Factory.addProduct(Stack)


class Box(DOM.Div):
    """
        A container that allows child elements to be contained within
       the border of the container.
    """
    __slots__ = ()

Factory.addProduct(Box)


class Flow(Base.WebElement):
    """
        A container that does not impose a border around its childElements
       allowing them to flow freely.
    """
    __slots__ = ()

Factory.addProduct(Flow)


class Horizontal(Box):
    """
        A container element that adds child elements horizontally.
    """
    __slots__ = ()
    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)
        self.addClass("WClear")

    def __modifyChild__(self, childElement):
        if not childElement.displayable:
            self.childElements.append(childElement)
            return
        if not childElement._tagName:
            container = Box.addChildElement(self, Box())
            container.addChildElement(childElement)
        else:
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            container = childElement
            self.childElements.append(childElement)

        if not container.hasClass("WLeft") and not container.hasClass("WRight") and not \
               (container._style and container.style.get("float", None)):
            container.addClass("WLeft")

    def toHtml(self, formatted=False, *args, **kwargs):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        returnValue = Box.toHtml(self, formatted=formatted, *args, **kwargs)
        self._childElements = oldChildElements
        return returnValue

Factory.addProduct(Horizontal)


class Vertical(Box):
    """
        A container that encourage elements to be added vertically with minimum html
    """
    __slots__ = ()
    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)
        self.addClass("WClear")

    def __modifyChild__(self, childElement):
        if not childElement.displayable:
            self.childElements.append(childElement)
        elif childElement._tagName:
            childElement.addClass("WClear")
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            self.childElements.append(childElement)
        else:
            container = Box()
            container.addClass("WClear")
            container.addChildElement(childElement)
            return Box.addChildElement(self, container)

    def toHtml(self, formatted=False, *args, **kwargs):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        returnValue = Box.toHtml(self, formatted=formatted, *args, **kwargs)
        self._childElements = oldChildElements
        return returnValue

Factory.addProduct(Vertical)


class FieldSet(DOM.FieldSet):
    """
        Groups child elements together with a labeled border
    """
    __slots__ = ('legend')
    properties = DOM.FieldSet.properties.copy()
    properties['legend'] = {'action':'setLegendText'}

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        DOM.FieldSet.__init__(self, id, name, parent, **kwargs)
        self.legend = None

    def getLegend(self):
        """
            Gets the legend associated with the field set - creating one if it is not present
        """
        if self.legend:
            return self.legend
        self.legend = Box.addChildElement(self, DOM.Legend)
        self.legend.text = Base.TextNode()
        return self.legend

    def setLegendText(self, legend):
        """
            Sets the label associated to the elements by adding a labeled legend
        """
        self.getLegend().text.setText(legend)

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

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)
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

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)

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

    def content(self, formatted=False, *args, **kwargs):
        return self.layout.toHtml(formatted=formatted, *args, **kwargs)

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


class HorizontalRule(DOM.HR):
    """
        Defines a 'hr' webelement - to specify a major shift in content horizontally
    """
    __slots__ = ()

Factory.addProduct(HorizontalRule)


class VerticalRule(Box):
    """
        Defines a vertical rule break - to specify a major shift in content vertically
    """
    __slots__ = ()
    allowsChildren = False

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)
        self.addClass("WVerticalRule")

Factory.addProduct(VerticalRule)


class Center(Box):
    """
        Defines a centered area (using valid css3)
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Box.__init__(self, id, name, parent, **kwargs)
        self.addClass("WCenter")
        outer = self.addChildElement(Box())
        outer.addClass("WOuter")
        inner = outer.addChildElement(Box())
        inner.addClass("WInner")
        self.addChildElementsTo = inner

Factory.addProduct(Center)
