'''
    test_Inputs.py

    Tests the functionality of thedom/Inputs.py

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
from thedom.Inputs import ValueElement


class TestValueElement(object):

    def setup_method(self, method):
        self.element = ValueElement("ValueId", "ValueName")

    def test_insertVariableByKey(self):
        variableDict = {'SomeValue':'AHHH!',
                        'ValueId':'Second',
                        'ValueName':'Third',
                        'SomeOtherValue':[1, 2, 3, 4]}

        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Second'
        assert self.element.exportVariables() == {'ValueName':'Second'}

    def test_insertVariableById(self):
        variableDict = {'SomeValue':'AHHH!',
                        'ValueId':'Second',
                        'ValueName':'Third',
                        'SomeOtherValue':[1, 2, 3, 4]}

        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Second'
        assert self.element.exportVariables() == {'ValueName':'Second'}

    def test_insertVariableByName(self):
        variableDict = {'SomeValue':'AHHH!',
                        'ValueName':'Third',
                        'SomeOtherValue':[1, 2, 3, 4]}

        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Third'


    def test_insertVariableListByName(self):
        variableDict = {'TestValues':'asfjsfadlkfsdj',
                        'ValueName':["Red", "Green", "Blue"],
                        'SomeOtherValue':[5, 6, 7, 8]}
        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Red'
        assert self.element.exportVariables() == {'ValueName':'Red'}

        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Green'
        assert self.element.exportVariables() == {'ValueName':'Green'}

        self.element.insertVariables(variableDict)
        assert self.element.value() == 'Blue'
        assert self.element.exportVariables() == {'ValueName':'Blue'}

    def test_value(self):
        assert not self.element.value()
        self.element.setValue("I set the value :)")
        assert self.element.value() == 'I set the value :)'

class TestIntegerTextBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("IntegerTextBox", 'int')

    def test_value(self):
        assert self.element.value() == 0
        self.element.setValue("Hello")
        assert self.element.value() == 0
        self.element.setValue("1000000000")
        assert self.element.value() == 1000000000
        self.element.setValue(-100000000)
        assert self.element.value() == -100000000

        self.element.minimum = 0
        self.element.maximum = 100
        self.element.setValue(-99999999)
        assert self.element.value() == 0
        self.element.setValue(9999999999999)
        assert self.element.value() == 100
        self.element.setValue("42")
        assert self.element.value() == 42

class TestCheckBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("CheckBox", name="Test")

    def test_value(self):
        assert self.element.value() == False
        self.element.setValue("I changed the value")
        assert self.element.value() == True
        self.element.setValue("")
        assert self.element.value() == False
        self.element.setValue(True)
        assert self.element.value() == True
        self.element.setValue(False)
        assert self.element.value() == False
        self.element.setValue("True")
        assert self.element.value() == True
        self.element.setValue("False")
        assert self.element.value() == False

    def test_valueChanged(self):
        element2 = Factory.build("CheckBox", name="Test2")
        self.element.connect('valueChanged', None, element2, 'setValue')

        self.element.setValue(True)
        assert element2.value() == True
        assert self.element.value() == True
        self.element.setValue(False)
        assert element2.value() == False
        assert self.element.value() == False
        self.element.setValue(True)
        assert element2.value() == True
        assert self.element.value() == True
        element2.setValue(False)
        assert element2.value() == False
        assert self.element.value() == True


class TestRadio(TestCheckBox):

    def setup_class(self):
        self.element = Factory.build("Radio", name="Test")


class TestTextBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("TextBox", name="Test")

    def test_attributes(self):
        assert self.element.attributes['type'] == 'text'
        assert self.element.attributes.get('size', '0') == '0'

    def test_setProperties(self):
        self.element.setProperties({'size':'10'})
        assert self.element.attributes.get('size', '0') == '10'


class TestTextArea(ElementTester):

    def setup_class(self):
        self.element = Factory.build("TextArea", "Test")

    def test_content(self):
        assert self.element.content({}) == ""
        assert self.element.value() == ""

        self.element.setValue("I set a value")
        assert self.element.content({}) == "I set a value"
        assert self.element.value() == "I set a value"


class TestOption(ElementTester):

    def setup_method(self, obj):
        self.element = Factory.build("Option", "Test")

    def test_select(self):
        assert not self.element.selected()
        assert not self.element.attributes.get('selected', None)

        self.element.select()
        assert self.element.selected()
        assert self.element.attributes.get('selected', None)

        self.element.unselect()
        assert not self.element.selected()
        assert not self.element.attributes.get('selected', None)

    def test_text(self):
        assert self.element.text() == ""

        self.element.setText("My Option Text")
        assert self.element.text() == "My Option Text"
        assert "My Option Text" in self.element.toHTML()

    def test_setProperties(self):
        data = {'selected':True, 'text':"My Text"}
        self.element.setProperties(data)
        assert self.element.text() == "My Text"
        assert "My Text" in self.element.toHTML()
        assert self.element.selected() == True

        newData = {'selected':False, 'text':"My New Text"}
        self.element.setProperties(newData)
        assert self.element.text() == "My New Text"
        assert "My New Text" in self.element.toHTML()
        assert self.element.selected() == False


class TestSelect(ElementTester):

    def setup_method(self, element):
        self.element = Factory.build("Select", "Test")
        self.option1 = Factory.build("Option", "Option1")
        self.option1.setValue("Value1")
        self.option1.setText("Text1")
        self.option2 = Factory.build("Option", "Option2")
        self.option2.setValue("Value2")
        self.option2.setText("Text2")
        self.option3 = Factory.build("Option", "Option3")
        self.option3.setValue("Value3")
        self.option3.setText("Text3")
        self.element.add(self.option1)
        self.element.add(self.option2)
        self.element.add(self.option3)
        self.options = {"Value1":"Text1",
                        "Value2":"Text2",
                        "Value3":"Text3"}

    def test_addOptions(self):

        assert self.element.options() == self.options

        newOption = Factory.build("Option", "Option4")
        newOption.setValue("Value4")
        newOption.setText("Text4")
        self.element.add(newOption)
        self.options['Value4'] = "Text4"
        assert self.element.options() == self.options

        self.element.addOptions({"Value5":"Text5",
                                "Value6":"Text6"})
        self.options["Value5"] = "Text5"
        self.options["Value6"] = "Text6"
        assert self.element.options() == self.options

        self.element.addOption("NewOption")
        assert self.element.options()['NewOption'] == 'NewOption'

        self.element.addOptions(("Value7", "Value8", "Value9"))
        assert self.element.options()['Value7'] == "Value7"
        assert self.element.options()['Value8'] == "Value8"
        assert self.element.options()['Value9'] == "Value9"

        self.element.addOptions((('Value10', 'Key10'), ('Value11', 'Key11'), ('Value12', 'Key12')))
        assert self.element.options()['Key10'] == "Value10"
        assert self.element.options()['Key11'] == "Value11"
        assert self.element.options()['Key12'] == "Value12"

    def test_addOptionList(self):
        self.element.reset()
        self.element.addOptionList([{'name':'option1', 'value':'option1value'},
                                    {'name':'option2', 'value':'option2value'}])
        assert self.element.options() == {'option1value':'option1',
                                          'option2value':'option2'}

    def test_value(self):
        assert self.element.value() == "Value1"

        self.element.setValue("Value2")
        assert self.element.value() == "Value2"

        #ensure setting to invalid value doesnt work
        self.element.setValue("Value24222349")
        assert self.element.value() == "Value1"
        assert self.element.selected() == None

        self.option3.select()
        assert self.element.value() == "Value3"
        assert self.element.selected() == self.option3

        #ensure setting the value to nothing deselects everything
        self.element.setValue("")
        assert self.element.value() == "Value1"
        assert self.element.selected() == None


class TestMulitSelect(ElementTester):

    def setup_method(self, element):
        self.element = Factory.build("MultiSelect", "Test")
        self.option1 = Factory.build("Option", "Option1")
        self.option1.setValue("Value1")
        self.option1.setText("Text1")
        self.option2 = Factory.build("Option", "Option2")
        self.option2.setValue("Value2")
        self.option2.setText("Text2")
        self.option3 = Factory.build("Option", "Option3")
        self.option3.setValue("Value3")
        self.option3.setText("Text3")
        self.element.add(self.option1)
        self.element.add(self.option2)
        self.element.add(self.option3)
        self.options = {"Value1":"Text1",
                        "Value2":"Text2",
                        "Value3":"Text3"}

    def test_addOptions(self):

        assert self.element.options() == self.options

        newOption = Factory.build("Option", "Option4")
        newOption.setValue("Value4")
        newOption.setText("Text4")
        self.element.add(newOption)
        self.options['Value4'] = "Text4"
        assert self.element.options() == self.options

        self.element.addOptions({"Value5":"Text5",
                                "Value6":"Text6"})
        self.options["Value5"] = "Text5"
        self.options["Value6"] = "Text6"
        assert self.element.options() == self.options

        self.element.addOption("NewOption")
        assert self.element.options()['NewOption'] == 'NewOption'

    def test_addOptionList(self):
        self.element.reset()
        self.element.addOptionList([{'name':'option1', 'value':'option1value'},
                                    {'name':'option2', 'value':'option2value'}])
        assert self.element.options() == {'option1value':'option1',
                                          'option2value':'option2'}

    def test_value(self):
        assert self.element.value() == []

        self.element.setValue("Value2")
        assert self.element.value() == ["Value2"]

        #ensure setting to invalid value doesnt work
        self.element.setValue("Value24222349")
        assert self.element.value() == []

        self.element.setValue(["Value1", "Value2"])
        assert self.element.value() == ["Value1", "Value2"]
