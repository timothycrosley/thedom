'''
    HiddenInputs.py

    Contains a collection of inputs that are not displayed to the user, but are passed to the server

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

from . import Base, Factory
from .Inputs import InputElement
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("HiddenInputs")


class HiddenValue(InputElement):
    """
        Defines a hidden '<input>' webelement (An input that can be modified but not viewed clientside)
    """
    __slots__ = ('width', )
    signals = InputElement.signals + ['textChanged']
    displayable = False

    def _create(self, id=None, name=None, parent=None, key=None):
        InputElement._create(self, id, name, parent, key=key)
        self.attributes['type'] = "hidden"

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
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, key=None):
        HiddenValue._create(self, id, name, parent, key=key)
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
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, key=None):
        HiddenValue._create(self, id, name, parent, key=key)
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
