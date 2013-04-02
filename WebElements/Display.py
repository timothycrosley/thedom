'''
    Display.py

    Contains elements such as Labels, whose primary purpose are to display information to the user

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

import datetime

from . import Base, ClientSide, DictUtils, DOM, Factory
from .Inputs import ValueElement
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

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

    def _render(self):
        Image._render(self)
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

    def addChildElement(self, childElement):
        """
            Overrides the add childelement behavior to nest child elements in Item elements.
        """
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

    def _render(self):
        DOM.UL._render(self)
        if self.ordered:
            self._tagName = "ol"

Item = List.Item
Factory.addProduct(List)


def label(cls):
    """
        Adds text access methods and properties to an existing class by sub-classing it.
    """
    class Labelable(cls):
        __slots__ = ('_textNode')

        signals = cls.signals + ['textChanged']
        properties = cls.properties.copy()
        properties['text'] = {'action':'setText'}
        properties['useNBSP'] = {'action':'call', 'type':'bool'}
        properties['strong'] = {'action':'call', 'name':'makeStrong', 'type':'bool'}
        properties['emphasis'] = {'action':'call', 'name':'addEmphasis', 'type':'bool'}

        class ClientSide(cls.ClientSide):

            def setText(self, text):
                element = self.get()
                element.innerHTML = text
                return element

        def _create(self, id=None, name=None, parent=None, **kwargs):
            cls._create(self, id=id, name=name, parent=parent)

            self._textNode = self.addChildElement(Base.TextNode())

        def setText(self, text, safe=False):
            """
                Sets the displayed text
            """
            if not safe:
                text = self.sanitize(text)
            if text != self._textNode.text():
                self._textNode.setText(text)
                self.emit('textChanged', text)

        def useNBSP(self):
            """
                Replaces the text with a single space character
            """
            self.setText('&nbsp;', safe=True)

        def text(self):
            """
                Returns the displayed text
            """
            return self._textNode.text()

        def appendText(self, text, safe=False):
            """
                Adds a new line character followed by additional text
            """
            prevText = self.text()
            if not prevText:
                return self.setText(text)

            if not safe:
                text = self.sanitize(text)

            self.setText(prevText + "<br />" + text, safe=True)

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

    Labelable.__name__ = cls.__name__
    return Labelable


@label
class Label(DOM.Label):
    """
        Defines a label webelement, which will display a single string of text to the user
    """
    __slots__ = ()

Factory.addProduct(Label)


@label
class Paragraph(DOM.P):
    """
        Defines a paragraph element
    """
    __slots__ = ()

Factory.addProduct(Paragraph)


@label
class Subscript(DOM.Sub):
    """
        Defines a subscripted text element
    """
    __slots__ = ()

Factory.addProduct(Subscript)


@label
class Superscript(DOM.Sup):
    """
        Defines a superscripted text element
    """
    __slots__ = ()

Factory.addProduct(Superscript)


@label
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

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Override toHTML to complain if an invalid header level is given.
        """
        self.level = int(self.level)
        if self.level > 6 or self.level < 1:
            raise ValueError("Valid levels for headers are 1-6 (h1-6)")

        self._tagName = "h%d" % self.level
        return Label.toHTML(self, formatted, *args, **kwargs)

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
    """
        Defines a label that contains a status, and is styled based on that status.
    """
    __slots__ = ('forElement')
    properties = Label.properties.copy()
    properties['messageType'] = {'action':'setMessageType'}

    class ClientSide(Label.ClientSide):
        def setMessageType(self, messageType):
            """
                Sets the type of message to be displayed
            """
            return self.chooseClass(ClientSide.MessageTypes.CLASS_LIST, ClientSide.MessageTypes.CLASSES[messageType])

        def showMessage(self, messageType, messageText):
            """
                Renders a message given the type of message, and associated text
            """
            return self.setMessageType(messageType)(self.setText(messageText))

        def showError(self, errorText):
            """
                Shows an error message
            """
            return self.showMessage(ClientSide.MessageTypes.ERROR, errorText)

        def showInfo(self, infoText):
            """
                Shows an info message
            """
            return self.showMessage(ClientSide.MessageTypes.INFO, errorText)

        def showWarning(self, warningText):
            """
                Shows a warning message
            """
            return self.showMessage(ClientSide.MessageTypes.WARNING, errorText)

        def showSuccess(self, successText):
            """
                Shows a success message
            """
            return self.showMessage(ClientSide.MessageTypes.SUCCESS, successText)

    def _create(self, id="", name=None, parent=None, **kwargs):
        Label._create(self, id and id + "Message", name, parent, **kwargs)

        self.forElement = None

    def _render(self):
        """
            Override the render to hide the element if no text is set on the message
        """
        Label._render(self)
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

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Overrides toHTML to render the element server-side but not return any html.
        """
        Base.WebElement.toHTML(self, False, *args, **kwargs)
        return ""

    def shown(self):
        """
            Overrides shown to always return False.
        """
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

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Overrides toHTML to always return an empty string.
        """
        return ""

    def shown(self):
        """
            Overrides shown to always return False.
        """
        return False

Factory.addProduct(Empty)


class Copyright(Label):
    __slots__ = ('owner', )
    properties = Base.WebElement.properties.copy()
    properties['owner'] =  {'action':'classAttribute'}

    def _create(self, name=None, id=None, parent=None, **kwargs):
        Label._create(self, name, id, parent, **kwargs)
        self.owner = ''

    def _render(self):
        self.setText("&copy;%s %s - All rights reserved." % (datetime.datetime.now().year, self.owner), safe=True)

Factory.addProduct(Copyright)


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

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Overrides toHTML to return the given html.
        """
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

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Overrides toHTML to only render itself once, and return a cached copy on subsequent calls.
        """
        if self.__cachedHTML__ is None:
            self.__cachedHTML__ = Base.WebElement.toHTML(self, formatted, *args, **kwargs)
        return self.__cachedHTML__

Factory.addProduct(CacheElement)
