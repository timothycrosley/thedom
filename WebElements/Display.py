#!/usr/bin/python
"""
   Name:
       Display

   Description:
       Contains elements that are used solely to display information on the screen

"""

import Base
import DictUtils
import Factory
from Inputs import ValueElement
from MethodUtils import CallBack

Factory = Factory.Factory(Base.Invalid, name="Display")


class Image(ValueElement):
    """
        Adds an image to the page
    """
    tagName = "img"
    allowsChildren = False
    tagSelfCloses = True
    properties = ValueElement.properties.copy()
    properties['src'] = {'action':'setValue'}

    def __init__(self, id=None, name=None, parent=None):
        ValueElement.__init__(self, id, name, parent)

    def setValue(self, value):
        """
            Sets the location from which to load the image
        """
        ValueElement.setValue(self, value)
        self.attributes['src'] = value

Factory.addProduct(Image)


class HoverImage(Image):
    """
        Defines an image that changes on mouseover
    """
    properties = ValueElement.properties.copy()
    properties['imageOnHover'] = {'action':'classAttribute'}
    properties['imageOnClick'] = {'action':'classAttribute'}
    imageOnHover = None
    imageOnClick = None

    def __init__(self, id=None, name=None, parent=None):
        Image.__init__(self, id, name, parent)

        self.connect("beforeToHtml", None, self, "__addEvents__")

    def __addEvents__(self):
        if self.imageOnHover:
            self.addJavascriptEvent('onmouseover', "this.src = '%s';" % self.imageOnHover)
            self.addJavascriptEvent('onmouseout', "this.src = '%s';" % self.value())
        if self.imageOnClick:
            self.addJavascriptEvent('onmousedown', "this.src = '%s';" % self.imageOnClick)
            self.addJavascriptEvent('onmouseup', "this.src = '%s';" % self.value())

Factory.addProduct(HoverImage)


class List(Base.WebElement):
    """
        Defines a list webelement (that will automatically list out its child elements in the format chosen)
    """
    tagName = "ul"
    properties = Base.WebElement.properties.copy()
    properties['ordered'] = {'action':'classAttribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}

    class Item(Base.WebElement):
        """
            Defines an individual Item within a list
        """
        tagName = "li"

        def setText(self, text):
            """
                Sets the displayed item text
            """
            self.textBeforeChildren = text

        def text(self):
            """
                Returns the displayed item text
            """
            return self.textBeforeChildren

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id=id, name=name, parent=parent)
        self.ordered = False
        self.connect("beforeToHtml", None, self, "__updateTag__")

    def addChildElement(self, childElement):
        item = self.Item()
        item.addChildElement(childElement)
        Base.WebElement.addChildElement(self, item)

        return childElement

    def addItem(self, name):
        """
            Adds an item to the list with text set as name
        """
        item = self.Item()
        item.setText(name)
        return Base.WebElement.addChildElement(self, item)

    def __updateTag__(self):
        if self.ordered:
            self.tagName = "ol"

Item = List.Item
Factory.addProduct(List)


class Label(Base.WebElement):
    """
        Defines a label webelement, which will display a single string of text to the user
    """
    tagName = 'span'
    signals = Base.WebElement.signals + ['textChanged']
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['useNBSP'] = {'action':'call', 'type':'bool'}

    def setText(self, text):
        """
            Sets the displayed text
        """
        if text != self.textBeforeChildren:
            self.textBeforeChildren = text
            self.emit('textChanged', text)

    def useNBSP(self):
        """
            Replaces the text with a single space character
        """
        self.setText('&nbsp;')

    def text(self):
        """
            Returns the displayed text
        """
        return self.textBeforeChildren

    def appendText(self, text):
        """
            Adds a new line character followed by additional text
        """
        prevText = self.text()
        if not prevText:
            return self.setText(text)

        self.setText(prevText + "<br />" + text)

Factory.addProduct(Label)


class PreformattedText(Label):
    """
        Defines a preformatted text label, where no forced format should be applied (such as single space)
    """
    tagName = "pre"
    allowsChildren = False

Factory.addProduct(PreformattedText)


class HeaderLabel(Label):
    """
        Defined a heading (h1-h6) label
    """
    properties = Base.WebElement.properties.copy()
    properties['level'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id=None, name=None, parent=None):
        Label.__init__(self, id, name, parent=parent)
        self.level = 2

    def toHtml(self, variableDict=None, formatted=False):
        if self.level > 6 or self.level < 1:
            raise ValueError("Valid levels for headers are 1-6 (h1-6)")

        self.tagName = "h%d" % self.level
        return Base.WebElement.toHtml(self, variableDict, formatted)

Factory.addProduct(HeaderLabel)


class FreeText(Label):
    """
        A Free text element is a label without a border
    """
    tagName = ''

Factory.addProduct(FreeText)


class LabeledData(Label):
    """
        Defines a label data pair, where the value type is defined by the label
    """
    properties = Base.WebElement.properties.copy()
    properties['label'] = {'action':'setText'}
    properties['data'] = {'action':'setData'}

    def __init__(self, id=None, name=None, parent=None, label=""):
        Label.__init__(self, id, name, parent=parent)
        self.style['vertical-align'] = "middle"
        self.__data__ = self.addChildElement(Label)
        self.__data__.addClass('WDataLabeled')
        self.setText(label)
        self.addClass("WLabeledData")

    def setData(self, data):
        """
            Sets the displayed data
        """
        return self.__data__.setText(data)

    def data(self):
        """
            Returns the displayed data
        """
        return self.__data__.text()

Factory.addProduct(LabeledData)


class Error(Label):
    """
        Defines an error webElement
    """
    tagName = "div"
    def __init__(self, id=None, name=None, parent=None):
        Label.__init__(self, id, name, parent)

Factory.addProduct(Error)


class FormError(Label):
    """
        Defines a '<form:error>' web element, which is used by formencode, or dynamics forms error processor to
        know where to place an error when present
    """
    displayable = False
    tagName = 'form:error'
    tagSelfCloses = True

    def __init__(self, id=None, name=None, parent=None):
        if id and not name:
            name = id or "ErrorGettingName"
            id = None

        Label.__init__(self, id, name, parent)

    def setError(self, errorText):
        """
            Sets the error text
        """
        self.tagName = "span"
        self.addClass("error-message")
        self.tagSelfCloses = False
        self.textBeforeChildren = errorText

    def shown(self):
        """
            Form Errors are never visible but only replaced
        """
        return False

Factory.addProduct(FormError)


class BlankRendered(Base.WebElement):
    """
        Outupts nothing but still renders child elements
    """
    displayable = False

    def toHtml(self, variableDict=None, formatted=False):
        Base.WebElement.toHtml(self, variableDict, False)
        return ""

    def shown(self):
        return False

Factory.addProduct(BlankRendered)


class Empty(Base.WebElement):
    """
        Outputs nothing to the page -- a useful placeholder
    """
    displayable = False

    def __init__(self, name=None, id=None, parent=None):
        Base.WebElement.__init__(self, None, None, parent)

    def toHtml(self, variableDict=None, formatted=False):
        return ""

    def shown(self):
        return False

Factory.addProduct(Empty)


class HTML(Base.WebElement):
    """
        Simply displays the html as it is given
    """
    properties = Base.WebElement.properties.copy()
    properties['html'] = {'action':'classAttribute'}

    def __init__(self, name=None, id=None, parent=None, html=""):
        Base.WebElement.__init__(self, None, None, parent)

        self.html = html

    def toHtml(self, variableDict=None, formatted=False):
        return self.html

Factory.addProduct(HTML)


class StatusIndicator(Base.WebElement):
    """
        Shows a visual indication of status from incomplete to complete
    """
    statuses = ['StatusIncomplete', 'StatusPartial', 'StatusComplete']
    Incomplete = 0
    Partial = 1
    Complete = 2

    tagName = "div"
    properties = Base.WebElement.properties.copy()
    properties['setStatus'] = {'action':'setStatus', 'type':'int'}

    def __init__(self, name=None, id=None, parent=None):
        Base.WebElement.__init__(self, name=name, id=id, parent=parent)
        self.setStatus(StatusIndicator.Incomplete)
        self.style['height'] = "100%"
        self.addClass('hidePrint')
        self.addClass('WStatusIndicator')

    def setStatus(self, status):
        """
            Sets the current displayed status
        """
        self.status = int(status)
        statusClass = self.statuses[self.status]
        self.chooseClass(self.statuses, statusClass)

Factory.addProduct(StatusIndicator)
