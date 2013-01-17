'''
    test_Fields.py

    Tests the functionality of WebElements/Fields.py

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
from WebElements.Base import Invalid
from WebElements.Display import Label
from WebElements.Inputs import CheckBox, TextBox

class TestTextField(ElementTester):

    def setup_class(self):
        self.element = Factory.build('TextField', 'test')


class TestTextAreaField(ElementTester):

    def setup_class(self):
        self.element = Factory.build('TextAreaField', 'test')


class TestAutoField(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Fields-AutoField", "Test")

    def test_label(self):
        assert type(self.element.label) == Label
        assert self.element.text() == ""

        self.element.setText("I changed the labels text!")
        assert self.element.text() == "I changed the labels text!"
        assert "I changed the labels text!" in self.element.toHTML()

    def test_userInput(self):
        assert type(self.element.userInput) == Invalid

        newInputField = Factory.build("TextBox", "MyTextBox")
        self.element.addChildElement(newInputField)
        assert self.element.userInput == newInputField


class TestSelectField(ElementTester):

    def setup_class(self):
        self.element = Factory.build('SelectField', 'test')


class TestCheckBoxField(ElementTester):

    def setup_class(self):
        self.element = Factory.build("CheckboxField", "Test")

    def test_attributes(self):
        assert type(self.element.userInput) == CheckBox
        assert type(self.element.label) == Label

    def setProperties(self):
        data = {"text":"My Label Text",
                "value":"on"}

        self.element.setProperties(data)
        assert self.element.userInput.value() == True
        assert self.element.text() == "My Label Text"

class TestIntField(ElementTester):

    def setup_class(self):
        self.element = Factory.build('IntegerField', 'intField')

class TestDateField(ElementTester):

    def setup_class(self):
        self.element = Factory.build('DateField', 'test')


class TestNestedSelect(ElementTester):

    def setup_class(self):
        self.element = Factory.build("nestedselect", "Test", "Test")
        self.element.setGroupData((('fruits', ('apple', 'orange', 'grape')),))


class TestFilter(ElementTester):

    def setup_method(self, obj):
        self.element = Factory.build("Filter", "Test")
        self.element.addSearchField("All")
        self.element.addSearchField("Name")
        self.element.addSearchField("Type")

    def test_attributes(self):
        assert self.element.searchFieldList == ['All', 'Name', 'Type']

    def test_addSearchField(self):
        self.element.addSearchField("New Search Field")
        assert self.element.searchFieldList == ['All', 'Name', 'Type',
                                                     'New Search Field']

    def test_insertVariables(self):
        assert self.element.filterList() == []
        data = {'Test:Or:Toggled': 'on', 'Test:And:Toggled':'off',
                'Test1:Or:Toggled':'off', 'Test1:And:Toggled':'on',
                'Test2:OrToggled':'on', 'Test2:And:Toggled':'off',
                'FilterTerm':['Something', 'Timothy', 'Person'],
                'FilterType':['BaseFilter', 'And', 'Or'],
                'FilterField':['All', 'Name', 'Type']}


        self.element.insertVariables(data)
        assert self.element.filterList() == [{'field': 'All',
                                                   'term': 'Something',
                                                   'type': 'BaseFilter'},
                                                  {'field': 'Name',
                                                   'term': 'Timothy',
                                                   'type': 'And'},
                                                  {'field': 'Type',
                                                   'term': 'Person',

                                                   'type': 'Or'}]
