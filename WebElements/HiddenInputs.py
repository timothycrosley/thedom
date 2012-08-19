#!/usr/bin/python
"""
   Name:
       Hidden Inputs

   Description:
       Contains elements that are hidden from the user

"""

import Base
import Factory
from Inputs import InputElement
from MethodUtils import CallBack

Factory = Factory.Factory(Base.Invalid, name="HiddenInputs")


class HiddenValue(InputElement):
    """
        Defines a hidden '<input>' webelement (An input that can be modified but not viewed clientside)
    """
    signals = InputElement.signals + ['textChanged']
    displayable = False

    def __init__(self, id=None, name=None, parent=None, key=None):
        InputElement.__init__(self, id, name, parent, key=key)
        self.attributes['type'] = "hidden"
        self.addClass((id or name or '') + "Value")
        self.addClass("Value")
        self.addClass("WHiddenInput")
        self.addClass(id or name or '')

        self.width = "hidden"

    def setText(self, text):
        """
            Sets the hidden inputs value
        """
        if text != self.value():
            self.setValue(text)
            self.emit('textChanged', text)

    def shown(self):
        """
            A hiddenInput is never visible
        """
        return False

    def text(self):
        """
            Returns the hidden inputs value
        """
        return self.value()

Factory.addProduct(HiddenValue)


class HiddenBooleanValue(HiddenValue):
    """
        Defines a hidden value which accepts true or false values
    """

    def __init__(self, id=None, name=None, parent=None, key=None):
        HiddenValue.__init__(self, id, name, parent, key=key)
        self.attributes['value'] = ''

    def setValue(self, value):
        """
            Sets the hidden inputs value to 1 or '' to represent true or false
        """
        if value:
            HiddenValue.setValue(self, True)
            self.attributes['value'] = '1'
        else:
            HiddenValue.setValue(self, False)
            self.attributes['value'] = ''

    def value(self):
        """
            Returns the true or false value of the input
        """
        return bool(HiddenValue.value(self))

Factory.addProduct(HiddenBooleanValue)


class HiddenIntValue(HiddenValue):
    """
        Defines a hidden value which accepts integer values only
    """
    def __init__(self, id=None, name=None, parent=None, key=None):
        HiddenValue.__init__(self, id, name, parent, key=key)
        self.attributes['value'] = 0

    def setValue(self, value):
        """
            Sets the value of the input as an integer
        """
        if (value is None) or (value == ''):
            value = 0

        HiddenValue.setValue(self, int(value))
        self.attributes['value'] = unicode(value)

    def value(self):
        """
            Returns the integer value of the input
        """
        return int(HiddenValue.value(self) or 0)

Factory.addProduct(HiddenIntValue)
