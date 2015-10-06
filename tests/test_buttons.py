'''
    test_Buttons.py

    Tests the functionality of thedom/Buttons.py

    Copyright (C) 2015  Timothy Edmund Crosley

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

from test_Base import ElementTester
from thedom.All import Factory


class TestLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Link", "TestLink")

    def test_destination(self):
        assert not self.element.destination()

        self.element.setDestination("www.google.com")
        assert self.element.destination() == "www.google.com"
        assert self.element.toHTML().find("www.google.com") > 0
        
    def test_rel(self):
        self.element.setProperty('rel', 'test')
        assert self.element.attributes['rel'] == 'test'

    def test_text(self):
        assert not self.element.text()
        self.element.setText("TEXT!")
        assert self.element.text() == "TEXT!"


class TestPopupLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build('PopupLink', 'myPopupLink')


class TestButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Button", name="Test")
        self.submitElement = Factory.build("SubmitButton")

    def test_attributes(self):
        assert self.element.attributes['type'] == 'button'
        assert self.submitElement.attributes['type'] == 'submit'


class TestPrintButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build('PrintButton', 'test')


class TestSubmitButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build('SubmitButton', 'test')


class TestToggleButton(ElementTester):

    def setup_method(self, obj):
        self.element = Factory.build("ToggleButton", "Test")

    def test_attributes(self):
        assert self.element.button.id == "Test"

    def test_toggle(self):
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "Pushed" in self.element.button.classes

        self.element.toggle()
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "Pushed" in self.element.button.classes

        self.element.toggle()
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "Pushed" in self.element.button.classes

        self.element.toggleOff()
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "Pushed" in self.element.button.classes

        self.element.toggleOn()
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "Pushed" in self.element.button.classes

    def test_value(self):
        assert self.element.value() == ""
        assert self.element.button.value() == ""
        self.element.setValue("I changed the value")
        assert self.element.value() == "I changed the value"
        assert self.element.button.value() == "I changed the value"

    def test_insertVariablesToggledOn(self):
        self.element.insertVariables({'Test:Toggled':"on"})
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "Pushed" in self.element.button.classes

    def test_insertVariablesToggledFalse(self):
        self.element.insertVariables({'Test:Toggled':"off"})
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "Pushed" in self.element.button.classes


class TestToggleLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build('ToggleLink', 'test')
