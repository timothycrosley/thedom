#!/usr/bin/python
"""
   Name:
       Buttons

   Description:
       Contains click-to-perform elements

"""

import Base
import ClientSide
import Display
import Factory
import Layout
from Inputs import InputElement
from HiddenInputs import HiddenValue
from MethodUtils import CallBack

Factory = Factory.Factory("Buttons")


class Link(Base.WebElement):
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
    tagName = 'a'

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name, parent)
        self._textNode = self.addChildElement(Base.TextNode())

    def setDestination(self, destination):
        self.attributes['href'] = destination

    def destination(self):
        return self.attributes.get('href', "")

    def setText(self, text):
        self._textNode.setText(text)
        self.emit('textChanged', text)

    def text(self):
        return self._textNode.text()

Factory.addProduct(Link)


class PopupLink(Link):
    """
        A link that will open the new page in a popup window
    """
    __slots__ = ('height', 'width', 'windowTitle', 'normal', 'separateWindow')

    properties = Link.properties.copy()
    properties['width'] = {'action':'classAttribute'}
    properties['height'] = {'action':'classAttribute'}
    # the 'normal' flag allows you to retain the menu/toolbar
    properties['normal'] = {'action':'classAttribute'}
    properties['windowTitle'] = {'action':'classAttribute'}
    properties['separateWindow'] = {'action':'classAttribute', 'type':'bool'}

    def __init__(self, id=None, name=None, parent=None):
        Link.__init__(self, id, name, parent)
        self.height = 700
        self.width = 700
        self.windowTitle = "_blank"
        self.normal = False
        self.separateWindow = False
        self.addJavascriptEvent('onClick', CallBack(self, 'javascriptPopUp'))

    def javascriptPopUp(self):
        """
            Returns the javascript responsible for opening up the link in a new window
        """
        return "return " + ClientSide.openPopup(height=self.height, width=self.width, normal=self.normal,
                                                separateWindow=self.separateWindow, windowTitle=self.windowTitle)

Factory.addProduct(PopupLink)


class Button(InputElement):
    """
        Defines an input button '<input type="button">' webelement
    """
    __slots__ = ()

    properties = InputElement.properties.copy()
    properties['disabled'] = {'action':'setDisabled', 'type':'bool'}

    def __init__(self, id=None, name=None, parent=None):
        InputElement.__init__(self, id, name, parent)
        self.attributes['type'] = 'button'

        self.connect('beforeToHtml', None, self, 'updateVisableState')

    def updateVisableState(self):
        """
            Called right before toHtml to make sure the button is not shown if it is not editable
        """
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

    def __init__(self, id=None, name=None, parent=None):
        PopupLink.__init__(self, id, name, parent)
        self.button = self.addChildElement(Button())
        self.addClass("PopupButton")

    def setText(self, text):
        return self.button.setText(text)

    def text(self):
        return self.button.text()

Factory.addProduct(PopupButton)

class ClosePopupButton(Button):
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None):
        Button.__init__(self, id, name, parent)
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

    def __init__(self, id=None, name=None, parent=None):
        Display.HoverImage.__init__(self, id, name, parent)

        self.style['height'] = "11px"
        self.style['width'] = "16px"
        self.setValue("images/count_up.png")

Factory.addProduct(UpButton)


class DownButton(Display.HoverImage):
    """
        A concrete button implementation, used to decrease something by a factor of 1
    """
    __slots__ = ()

    imageOnHover = 'images/count_down_highlight.png'
    imageOnClick = 'images/count_down_pressed.png'

    def __init__(self, id=None, name=None, parent=None):
        Display.HoverImage.__init__(self, id, name, parent)

        self.style['height'] = "11px"
        self.style['width'] = "16px"
        self.setValue("images/count_down.png")

Factory.addProduct(DownButton)


class PrintButton(Button):
    """
        Defines a button thats sole purpose in life is to print the current page
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None):
        Button.__init__(self, id, name, parent)
        self.setValue("Print")
        self.addJavascriptEvent('onclick', 'window.print()')

Factory.addProduct(PrintButton)


class SubmitButton(Button):
    """
        Defines a button that when clicked will submit the current page back to the server (if contained in a form)
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None):
        Button.__init__(self, id, name, parent)
        self.attributes['type'] = 'submit'

Factory.addProduct(SubmitButton)


class ToggleButton(Layout.Box):
    """
        Defines a button that can be used as a toggle, with an on and off state
    """
    __slots__ = ('button', 'toggledState')

    properties = Button.properties
    signals = Layout.Box.signals + ['toggled', 'jsToggled']

    def __init__(self, id, name=None, parent=None):
        Layout.Box.__init__(self, id + "Container", name, parent)

        self.setContainerType('span')

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
        return """if(WENextElement(this).value == 'off'){
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
                var element = WEGetElement('""" + self.button.jsId() + """');
                WERemoveClass(element, 'Pushed');
                WENextElement(element).value = 'off';
               """

    def jsToggleOn(self):
        """
            Returns the javascript that will turn the button on client side
        """
        return """
                var element = WEGetElement('""" + self.button.jsId() + """');
                WEAddClass(element, 'Pushed');
                WENextElement(element).value = 'on';
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
        Layout.Box.setProperties(self, valueDict)
        self.button.setProperties(valueDict)

    def insertVariables(self, valueDict=None):
        if valueDict == None:
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
