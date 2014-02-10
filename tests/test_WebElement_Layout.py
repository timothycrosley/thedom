'''
    test_Layout.py

    Tests the functionality of thedom/Layout.py

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
from thedom.All import Factory


class TestStack(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Stack", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("box", name="box"))


class TestBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Box", name="Test")


class TestFlow(ElementTester):

    def setup_class(self):
        self.element = Factory.build("box", name="Test")
        self.flowContainer = self.element.addChildElement(Factory.build("flow", name="flow"))
        self.flowContainer.addChildElement(Factory.build("Button", name="Button"))
        self.flowContainer.addChildElement(Factory.build("box", name="box"))

class TestHorizontal(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Horizontal", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Flow", name="Container"))


class TestVertical(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Vertical", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Flow", name="Container"))


class TestFields(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Fields", name="Test")


class TestLineBreak(ElementTester):

    def setup_class(self):
        self.element = Factory.build("lineBreak", name="Test")


class TestHorizontalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('HorizontalRule', 'test')


class TestVerticalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('VerticalRule', 'test')

class TestCenter(ElementTester):

    def setup_class(self):
        self.element = Factory.build('center', 'test')
