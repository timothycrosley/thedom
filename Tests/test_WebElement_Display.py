'''
    test_Display.py

    Tests the functionality of WebElements/Display.py

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

class TestImage(ElementTester):

    def setup_method(self, element):
        self.element = Factory.build("Image", name="Test")

    def test_setProperties(self):
        self.element.setProperties({'src':'images/lightbulb.png'})
        assert self.element.attributes['src'] == 'images/lightbulb.png'

    def test_value(self):
        assert not self.element.attributes.get('src', None)
        self.element.setProperty('src', "images/lightbulb.png")
        assert self.element.attributes['src'] == "images/lightbulb.png"


class TestList(ElementTester):

    def setup_class(self):
        self.element = Factory.build('List', 'testList')


class TestLabel(object):

    def setup_method(self, method):
        self.element = Factory.build("Label", "Test")

    def test_text(self):
        assert not self.element.text()
        self.element.setText("I changed the text")
        assert self.element.text() == "I changed the text"
        assert "I changed the text" in self.element.toHTML()

    def test_setProperties(self):
        assert self.element.text() == ""
        self.element.setProperties({'text':'I set the text'})
        assert self.element.text() == "I set the text"
        assert "I set the text" in self.element.toHTML()


class TestParagraph(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build("Paragraph", "Test")


class TestSubscript(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build("Subscript", "Test")


class TestSuperscript(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build("Superscript", "Test")


class TestPreformattedText(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build("PreformattedText", "Test")


class TestFormError(ElementTester):

    def setup_class(self):
        self.element = Factory.build("formError", name="TestFormError")


class TestEmpty(ElementTester):

    def setup_class(self):
        self.element = Factory.build("box")
        self.element.addChildElement(Factory.build("empty", name="Test"))
