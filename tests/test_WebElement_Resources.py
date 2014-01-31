'''
    test_Resources.py

    Tests the functionality of WebElements/Resources.py

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
from WebElements.Resources import ScriptContainer


class TestResourceFile(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ResourceFile", "Test")
        self.element.setFile("javascript.js")

    def test_setFile(self):
        self.element.setFile("")
        assert self.element.resourceType == None
        assert self.element.fileName == ""

        self.element.setFile("Style.css")
        assert self.element.resourceType == "css"
        assert self.element.fileName == "Style.css"

        self.element.setFile("Javascript.js")
        assert self.element.resourceType == "javascript"
        assert self.element.fileName == "Javascript.js"


class TestScriptContainer(ElementTester):

    def setup_method(self, method):
        self.element = ScriptContainer()

    def test_addScript(self):
        assert self.element._scripts == []

        self.element.addScript("alert('I am a script :D');")
        self.element.addScript("var value = 'I am another script';")
        assert self.element._scripts == ["alert('I am a script :D');",
                                                 "var value = 'I am another script';"]
        assert "alert('I am a script :D');" in self.element.toHTML()
        assert "var value = 'I am another script';" in self.element.toHTML()

    def test_removeScript(self):
        assert self.element._scripts == []

        self.element.addScript("alert('I am a script :D');")
        assert self.element._scripts == ["alert('I am a script :D');"]

        self.element.removeScript("alert('I am a script :D');")
        assert self.element._scripts == []
