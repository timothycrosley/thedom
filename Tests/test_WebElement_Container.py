'''
    test_Container.py

    Tests the functionality of WebElements/Container.py

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

class TestDropDownMenu(ElementTester):

    def setup_class(self):
        self.element = Factory.build("dropdownmenu", "Test")


class TestAutocomplete(ElementTester):

    def setup_class(self):
        self.element = Factory.build("autocomplete", "Test")


class TestTab(ElementTester):

    def setup_class(self):
        self.element = Factory.build("tab", "Test")

    def test_text(self):
        tab = Factory.build("tab", "Test")
        assert tab.tabLabel.text() == ""
        assert tab.text() == ""
        assert tab.text() == tab.tabLabel.text()

        tab.setProperty('text', 'heyy')
        assert tab.tabLabel.text() == "heyy"
        assert tab.text() == "heyy"
        assert tab.text() == tab.tabLabel.text()

class TestTabContainer(ElementTester):

    def setup_class(self):
        self.element = Factory.build('TabContainer', 'Test')

    def test_tabs(self):
        tab1 = self.element.addChildElement(Factory.build('Tab', 'Tab1'))
        tab2 = self.element.addChildElement(Factory.build('Tab', 'Tab2'))
        tab3 = self.element.addChildElement(Factory.build('Tab', 'Tab3'))
        assert tab1.isSelected
        assert not tab2.isSelected
        assert not tab3.isSelected

        tab2.select()
        assert not tab1.isSelected
        assert tab2.isSelected
        assert not tab3.isSelected

        tab3.select()
        assert not tab1.isSelected
        assert not tab2.isSelected
        assert tab3.isSelected


class TestAccordion(ElementTester):

    def setup_class(self):
        self.element = Factory.build("accordion", "Test")


class TestFormContainer(ElementTester):

    def setup_class(self):
        self.element = Factory.build("FormContainer", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Flow", name="Container"))

