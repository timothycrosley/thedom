"""
    Buttons.py

    Contains elements that perform an action when clicked

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
"""

from . import Base, ClientSide, Display, DOM, Factory, Layout
from .HiddenInputs import HiddenValue
from .Inputs import InputElement
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("Buttons")


class Link(DOM.A):
    """
        Defines an <a href> webelement (An html link meant to open a new page)
    """
    __slots__ = ('_textNode')
    signals = Base.WebElement.signals + ['emit', 'textChanged']
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['value'] = {'action':'setDestination'}
    properties['target'] = {'action':'attribute'}
    properties['onclick'] = {'action':'javascriptEvent'}
    properties['href'] = {'action':'setDestination'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        DOM.A._create(self, id, name, parent, **kwargs)
        self._textNode = self.addChildElement(Base.TextNode())

    def setDestination(self, destination):
        """
            Sets the URL the link points to.
        """
        self.attributes['href'] = destination

    def destination(self):
        """
            Returns the URL the link points to.
        """
        return self.attributes.get('href', "")

    def setText(self, text):
        """
            Sets the text associated with the link.
        """
        self._textNode.setText(text)
        self.emit('textChanged', text)

    def text(self):
        """
            Returns the text associated with the link.
        """
        return self._textNode.text()

Factory.addProduct(Link)


class PopupLink(Link):
    """
        A link that will open the new page in a popup window
    """
    __slots__ = ('height', 'width', 'windowTitle', 'normal', 'popupOptions')
    properties = Link.properties.copy()
    properties['width'] = {'action':'classAttribute'}
    properties['height'] = {'action':'classAttribute'}
    properties['normal'] = {'action':'classAttribute'}
    properties['windowTitle'] = {'action':'classAttribute'}
    properties['popupOptions'] = {'action':'classAttribute'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Link._create(self, id, name, parent, **kwargs)
        self.height = 700
        self.width = 700
        self.windowTitle = "_blank"
        self.normal = False
        self.popupOptions = None
        self.addJavascriptEvent('onClick', CallBack(self, 'javascriptPopUp'))

    def javascriptPopUp(self):
        """
            Returns the javascript responsible for opening up the link in a new window
        """
        return "return " + str(ClientSide.openPopup(url=ClientSide.Script("this.href"), height=self.height,
                                                    width=self.width, normal=self.normal,
                                                    windowTitle=self.windowTitle, options=self.popupOptions))

Factory.addProduct(PopupLink)


class Button(InputElement):
    """
        Defines an input button '<input type="button">' webelement
    """
    __slots__ = ()
    properties = InputElement.properties.copy()
    properties['disabled'] = {'action':'setDisabled', 'type':'bool'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        InputElement._create(self, id, name, parent, **kwargs)
        self.attributes['type'] = 'button'

    def _render(self):
        InputElement._render(self)

        # Update visible state
        if self.shown():
            if not self.editable():
                self.style['display'] = 'none'
            else:
                if self.style.get('display') == 'none':
                    self.style.pop('display', None)

    def setDisabled(self, disabled):
        """
            Toggles disabled status of button, if disabled user can not click the button to perform desired action
        """
        if disabled:
            self.attributes['disabled'] = '1'
            self.attributes['readonly'] = '1'
        else:
            self.attributes.pop('disabled', None)
            self.attributes.pop('readonly', None)

    def disabled(self):
        """
            Returns true if the button is disabled.
        """
        return self.attributes.get('disabled', None) == '1'

    def setText(self, text):
        """
            Sets the buttons visible text
        """
        self.setValue(text)

    def text(self):
        """
            Returns the buttons text
        """
        return self.value()

Factory.addProduct(Button)


class PopupButton(PopupLink):
    __slots__ = ('button')
    properties = PopupLink.properties.copy()
    properties['buttonClass'] = {'action': 'button.addClassesFromString', 'name': 'class'}
    properties['buttonStyle'] = {'action': 'button.setStyleFromString', 'name': 'style'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        PopupLink._create(self, id, name, parent, **kwargs)
        self.button = self.addChildElement(Button())
        self.addClass("PopupButton")

    def setText(self, text):
        """
            Sets the text associated with the pop-up button.
        """
        return self.button.setText(text)

    def text(self):
        """
            Returns the text associated with the pop-up button.
        """
        return self.button.text()

Factory.addProduct(PopupButton)

class ClosePopupButton(Button):
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Button._create(self, id, name, parent, **kwargs)
        self.addJavascriptEvent('onclick', 'window.close();')
        self.setText('Close')

Factory.addProduct(ClosePopupButton)


class UpButton(Display.HoverImage):
    """
        A concrete button implementation, used to increase something by a factor of 1
    """
    __slots__ = ()
    imageOnHover = 'images/count_up_highlight.png'
    imageOnClick = 'images/count_up_pressed.png'

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Display.HoverImage._create(self, id, name, parent, **kwargs)

        self.style['height'] = "11px"
        self.style['width'] = "16px"
        self.setProperty('src', "images/count_up.png")

Factory.addProduct(UpButton)


class DownButton(Display.HoverImage):
    """
        A concrete button implementation, used to decrease something by a factor of 1
    """
    __slots__ = ()
    imageOnHover = 'images/count_down_highlight.png'
    imageOnClick = 'images/count_down_pressed.png'

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Display.HoverImage._create(self, id, name, parent, **kwargs)

        self.style['height'] = "11px"
        self.style['width'] = "16px"
        self.setProperty("src", "images/count_down.png")

Factory.addProduct(DownButton)


class PrintButton(Button):
    """
        Defines a button thats sole purpose in life is to print the current page
    """
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Button._create(self, id, name, parent, **kwargs)
        self.setValue("Print")
        self.addJavascriptEvent('onclick', 'window.print()')

Factory.addProduct(PrintButton)


class SubmitButton(Button):
    """
        Defines a button that when clicked will submit the current page back to the server (if contained in a form)
    """
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Button._create(self, id, name, parent, **kwargs)
        self.attributes['type'] = 'submit'

Factory.addProduct(SubmitButton)


class ToggleButton(Layout.Box):
    """
        Defines a button that can be used as a toggle, with an on and off state
    """
    __slots__ = ('button', 'toggledState')
    properties = Button.properties.copy()
    properties['checked'] = {'action':'call', 'name':'toggleOn', 'type':'bool'}
    signals = Layout.Box.signals + ['toggled', 'jsToggled']

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id + "Container", name, parent, **kwargs)

        button = self.__createToggle__(id)
        button.addJavascriptEvent('onClick', CallBack(self, 'jsToggle'))
        button.addClass("WToggleButton")
        self.button = self.addChildElement(button)

        toggledState = HiddenValue(id + ":Toggled")
        toggledState.setValue('off')
        self.toggledState = self.addChildElement(toggledState)

    def __createToggle__(self, id):
        return Button(id)

    def toggle(self):
        """
            Reverses the current toggle state
        """
        if self.toggledState.value() == 'off':
            self.toggleOn()
        else:
            self.toggleOff()

    def toggleOff(self):
        """
            Turns the toggle off
        """
        if self.button.hasClass('Pushed'):
            self.button.removeClass('Pushed')
            self.toggledState.setValue('off')
            self.emit('toggled', False)

    def toggleOn(self):
        """
            Turns the toggle on
        """
        self.button.addClass('Pushed')
        self.toggledState.setValue('on')
        self.emit('toggled', True)

    def jsToggle(self):
        """
            Returns the javascript that will reverse the buttons toggle state client side
        """
        return """if(WebElements.next(this).value == 'off'){
                    """ + self.jsToggleOn() + '\n'.join(self.emit('jsToggled', True)) + """
                  }
                  else{
                    """ + self.jsToggleOff() + '\n'.join(self.emit('jsToggled', False)) + """
                  }"""

    def jsToggleOff(self):
        """
            Returns the javascript that will turn the button off client side
        """
        return """
                var element = WebElements.get('""" + self.button.fullId() + """');
                WebElements.removeClass(element, 'Pushed');
                WebElements.next(element).value = 'off';
               """

    def jsToggleOn(self):
        """
            Returns the javascript that will turn the button on client side
        """
        return """
                var element = WebElements.get('""" + self.button.fullId() + """');
                WebElements.addClass(element, 'Pushed');
                WebElements.next(element).value = 'on';
               """

    def toggled(self):
        """
            Will return True if the button is toggled on
        """
        if self.toggledState.value() == 'on':
            return True

        return False

    def setText(self, text):
        """
            Sets the visible text of the button
        """
        self.button.setText(text)

    def setValue(self, value):
        """
            Sets the invisible value associated with the button
        """
        self.button.setValue(value)

    def value(self):
        """
            Returns the value associated with the button
        """
        return self.button.value()

    def setProperties(self, valueDict=None):
        """
            Fowards the properties to the button, in case it is not a child element.
        """
        Layout.Box.setProperties(self, valueDict)
        self.button.setProperties(valueDict)

    def insertVariables(self, valueDict=None):
        """
            Updates the display status based on the passed in variables
        """
        if valueDict is None:
            valueDict = {}

        Layout.Box.insertVariables(self, valueDict)
        if self.toggled():
            self.toggleOn()
        else:
            self.toggleOff()

Factory.addProduct(ToggleButton)


class ToggleLink(ToggleButton):
    """
        Defines a link that can be toggled on and off like a toggle button
    """
    __slots__ = ()

    def __createToggle__(self, id):
        link = Link(id)
        link.setDestination("#Link")
        link.addClass("WToggleLink")
        return link

Factory.addProduct(ToggleLink)
