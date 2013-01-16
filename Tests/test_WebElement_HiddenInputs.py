'''
    test_HiddenInputs.py

    Tests the functionality of WebElements/HiddenInputs.py

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

from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestHiddenValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenValue", name="Test")

    def test_attributes(self):
        assert self.element.attributes['type'] == 'hidden'

    def test_text(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("I changed the value")
        assert self.element.value() == "I changed the value"
        assert self.element.text() == "I changed the value"
        self.element.setText("I changed the text")
        assert self.element.text() == "I changed the text"
        assert self.element.value() == "I changed the text"


class TestHiddenBooleanValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenBooleanValue", name="Test")

    def test_value(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("1")
        assert self.element.value() is True
        self.element.setText(True)
        assert self.element.value() is True
        self.element.setValue("")
        assert self.element.value() is False
        self.element.setValue(False)
        assert self.element.value() is False


class TestHiddenIntValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenIntValue", name="Test")

    def test_value(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("1")
        assert self.element.value() == 1
        assert self.element.text() == 1
        self.element.setText("")
        assert self.element.text() == 0
        assert self.element.value() == 0
        self.element.setText(None)
        assert self.element.text() == 0
        assert self.element.value() == 0
        self.element.setText(2)
        assert self.element.text() == 2
        assert self.element.value() == 2
        self.element.setText(0)
        assert self.element.text() == 0
        assert self.element.value() == 0

