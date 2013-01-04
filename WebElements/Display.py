#!/usr/bin/python
"""
   Name:
       Display

   Description:
       Contains elements that are used solely to display information on the screen

"""

import Base
import ClientSide
import DictUtils
import DOM
import Factory
from Inputs import ValueElement
from MethodUtils import CallBack

Factory = Factory.Factory("Display")


class Image(DOM.Img):
    """
        Adds an image to the page
    """
    __slots__ = ()

    allowsChildren = False
    tagSelfCloses = True

Factory.addProduct(Image)


class HoverImage(Image):
    """
        Defines an image that changes on mouseover
    """
    __slots__ = ()

    properties = Image.properties.copy()
    properties['imageOnHover'] = {'action':'classAttribute'}
    properties['imageOnClick'] = {'action':'classAttribute'}
    imageOnHover = None
    imageOnClick = None

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Image._create(self, id, name, parent, **kwargs)

        self.connect("rendering", None, self, "__addEvents__")

    def __addEvents__(self):
        if self.imageOnHover:
            self.addJavascriptEvent('onmouseover', "this.src = '%s';" % self.imageOnHover)
            self.addJavascriptEvent('onmouseout', "this.src = '%s';" % self.attributes['src'])
        if self.imageOnClick:
            self.addJavascriptEvent('onmousedown', "this.src = '%s';" % self.imageOnClick)
            self.addJavascriptEvent('onmouseup', "this.src = '%s';" % self.attributes['src'])

Factory.addProduct(HoverImage)


class List(DOM.UL):
    """
        Defines a list webelement (that will automatically list out its child elements in the format chosen)
    """
    __slots__ = ('ordered')

    properties = DOM.UL.properties.copy()
    properties['ordered'] = {'action':'classAttribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}

    class Item(DOM.LI):
        """
            Defines an individual Item within a list
        """
        __slots__ = ('_textNode')

        def _create(self, id=None, name=None, parent=None, **kwargs):
            DOM.LI._create(self, id=id, name=name, parent=parent)

            self._textNode = self.addChildElement(Base.TextNode())

        def setText(self, text):
            """
                Sets the displayed item text
            """
            self._textNode.setText(text)

        def text(self):
            """
                Returns the displayed item text
            """
            return self._textNode.text()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        DOM.UL._create(self, id=id, name=name, parent=parent)
        self.ordered = False
        self.connect("rendering", None, self, "__updateTag__")

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
            self._tagName = "ol"

Item = List.Item
Factory.addProduct(List)


class Label(DOM.Label):
    """
        Defines a label webelement, which will display a single string of text to the user
    """
    __slots__ = ('_textNode')

    signals = DOM.Label.signals + ['textChanged']
    properties = DOM.Label.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['useNBSP'] = {'action':'call', 'type':'bool'}
    properties['strong'] = {'action':'call', 'name':'makeStrong', 'type':'bool'}
    properties['emphasis'] = {'action':'call', 'name':'addEmphasis', 'type':'bool'}

    class ClientSide(DOM.Label.ClientSide):

        def setText(self, text):
            element = self.get()
            element.innerHTML = text
            return element

    def _create(self, id=None, name=None, parent=None, **kwargs):
        DOM.Label._create(self, id=id, name=name, parent=parent)

        self._textNode = self.addChildElement(Base.TextNode())

    def setText(self, text):
        """
            Sets the displayed text
        """
        if text != self._textNode.text():
            self._textNode.setText(text)
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
        return self._textNode.text()

    def appendText(self, text):
        """
            Adds a new line character followed by additional text
        """
        prevText = self.text()
        if not prevText:
            return self.setText(text)

        self.setText(prevText + "<br />" + text)

    def makeStrong(self):
        """
            wraps into a strong tag - requires parent element to be defined
        """
        self.addChildElementsTo = self.addChildElement(DOM.Strong())
        self.addChildElementsTo.addChildElement(self._textNode)

    def addEmphasis(self):
        """
            wraps into an emphasis tag - requires parent element to be defined
        """
        self.addChildElementsTo = self.addChildElement(DOM.Em())
        self.addChildElementsTo.addChildElement(self._textNode)

Factory.addProduct(Label)


class Paragraph(DOM.P):
    """
        Defines a paragraph element
    """
    __slots__ = ()

Factory.addProduct(Paragraph)


class Subscript(DOM.Sub):
    """
        Defines a subscripted text element
    """
    __slots__ = ()

Factory.addProduct(Subscript)


class Superscript(DOM.Sup):
    """
        Defines a superscripted text element
    """
    __slots__ = ()

Factory.addProduct(Superscript)


class PreformattedText(DOM.Pre):
    """
        Defines a preformatted text label, where no forced format should be applied (such as single space)
    """
    __slots__ = ()

Factory.addProduct(PreformattedText)


class HeaderLabel(Label):
    """
        Defined a heading (h1-h6) label
    """
    __slots__ = ('level')
    properties = Label.properties.copy()
    properties['level'] = {'action':'classAttribute', 'type':'int'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Label._create(self, id, name, parent=parent)
        self.level = 2

    def toHtml(self, formatted=False, *args, **kwargs):
        self.level = int(self.level)
        if self.level > 6 or self.level < 1:
            raise ValueError("Valid levels for headers are 1-6 (h1-6)")

        self._tagName = "h%d" % self.level
        return Label.toHtml(self, formatted, *args, **kwargs)

Factory.addProduct(HeaderLabel)


class FreeText(Label):
    """
        A Free text element is a label without a border
    """
    __slots__ = ()
    tagName = ''

Factory.addProduct(FreeText)


class LabeledData(Label):
    """
        Defines a label data pair, where the value type is defined by the label
    """
    __slots__ = ('__data__', )

    properties = Base.WebElement.properties.copy()
    properties['label'] = {'action':'setText'}
    properties['data'] = {'action':'setData'}

    def _create(self, id=None, name=None, parent=None, label=""):
        Label._create(self, id, name, parent=parent)
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


class FormError(Label):
    """
        Defines where a form error should be placed - adds it to the page
        even when an error doesn't occur so that errors can be added
        by javascript as well as server side validators
    """
    __slots__ = ('forElement')
    tagName = "div"

    def _create(self, id="", name=None, parent=None, **kwargs):
        Label._create(self, id  and id + "Error", name, parent, **kwargs)

        self.hide()
        self.forElement = None

Factory.addProduct(FormError)


class Message(Label):
    __slots__ = ('forElement')
    properties = Label.properties.copy()
    properties['messageType'] = {'action':'setMessageType'}
    class ClientSide(Label.ClientSide):
        def setMessageType(self, messageType):
            return self.chooseClass(ClientSide.MessageTypes.CLASS_LIST, ClientSide.MessageTypes.CLASSES[messageType])

        def showMessage(self, messageType, messageText):
            return self.setMessageType(messageType)(self.setText(messageText))

        def showError(self, errorText):
            return self.showMessage(ClientSide.MessageTypes.ERROR, errorText)

        def showInfo(self, infoText):
            return self.showMessage(ClientSide.MessageTypes.INFO, errorText)

        def showWarning(self, warningText):
            return self.showMessage(ClientSide.MessageTypes.WARNING, errorText)

        def showSuccess(self, successText):
            return self.showMessage(ClientSide.MessageTypes.SUCCESS, successText)

    def _create(self, id="", name=None, parent=None, **kwargs):
        Label._create(self, id and id + "Message", name, parent, **kwargs)

        self.forElement = None

    def render(self):
        """
            Override the render to hide the element if no text is set on the message
        """
        Label.render(self)
        if not self.text():
            self.hide()

        if self.forElement:
            self.attributes['for'] = self.forElement.fullId()

    def setMessageType(self, messageType):
        """
            Sets the type of message to be displayed
        """
        self.chooseClass(ClientSide.MessageTypes.CLASS_MAP.values(), ClientSide.MessageTypes.CLASS_MAP[messageType])

    def showMessage(self, messageType, messageText):
        """
            Renders a message given the type of message, and associated text
        """
        self.setMessageType(messageType)
        self.setText(messageText)

    def showError(self, error):
        """
            Shows an error message
        """
        self.showMessage(ClientSide.MessageTypes.ERROR, error)

    def showInfo(self, info):
        """
            Shows an info message
        """
        self.showMessage(ClientSide.MessageTypes.INFO, info)

    def showWarning(self, warning):
        """
            Shows a warning message
        """
        self.showMessage(ClientSide.MessageTypes.WARNING, warning)

    def showSuccess(self, success):
        """
            Shows a success message
        """
        self.showMessage(ClientSide.MessageTypes.SUCCESS, success)

    def clearMessage(self):
        """
            Removes any messages from the label
        """
        self.setText("")
        for messageClass in ClientSide.MessageTypes.CLASS_MAP.keys():
            self.removeClass(messageClass)

Factory.addProduct(Message)


class BlankRendered(Base.WebElement):
    """
        Outupts nothing but still renders child elements
    """
    __slots__ = ()
    displayable = False

    def toHtml(self, formatted=False, *args, **kwargs):
        Base.WebElement.toHtml(self, False, *args, **kwargs)
        return ""

    def shown(self):
        return False

Factory.addProduct(BlankRendered)


class Empty(Base.WebElement):
    """
        Outputs nothing to the page -- a useful placeholder
    """
    __slots__ = ()
    displayable = False

    def _create(self, name=None, id=None, parent=None):
        Base.WebElement._create(self, None, None, parent)

    def toHtml(self, formatted=False, *args, **kwargs):
        return ""

    def shown(self):
        return False

Factory.addProduct(Empty)


class StraightHTML(Base.WebElement):
    """
        Simply displays the html as it is given
    """
    __slots__ = ('html')
    properties = Base.WebElement.properties.copy()
    properties['html'] = {'action':'classAttribute'}

    def _create(self, name=None, id=None, parent=None, html=""):
        Base.WebElement._create(self, None, None, parent)

        self.html = html

    def toHtml(self, formatted=False, *args, **kwargs):
        return self.html

Factory.addProduct(StraightHTML)


class StatusIndicator(DOM.Div):
    """
        Shows a visual indication of status from incomplete to complete
    """
    __slots__ = ('status')
    statuses = ['StatusIncomplete', 'StatusPartial', 'StatusComplete']
    Incomplete = 0
    Partial = 1
    Complete = 2

    properties = DOM.Div.properties.copy()
    properties['setStatus'] = {'action':'setStatus', 'type':'int'}

    def _create(self, name=None, id=None, parent=None):
        DOM.Div._create(self, name=name, id=id, parent=parent)
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


class CacheElement(Base.WebElement):
    """
        Renders an element once caches the result and returns the cache every time after
    """
    __slots__ = ('__cachedHTML__')

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.WebElement._create(self, id, name, parent, **kwargs)
        self.__cachedHTML__ = None

    def toHtml(self, formatted=False, *args, **kwargs):
        if self.__cachedHTML__ == None:
            self.__cachedHTML__ = Base.WebElement.toHtml(self, formatted, *args, **kwargs)
        return self.__cachedHTML__

Factory.addProduct(CacheElement)
