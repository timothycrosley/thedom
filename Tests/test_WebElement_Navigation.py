'''
    test_Navigation.py

    Tests the functionality of WebElements/Navigation.py

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
from WebElements.Buttons import Link

class TestItemPager(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build('ItemPager', 'Test')
        self.element.itemsPerPage = 5
        self.element.pagesShownAtOnce = 15
        self.element.connect('jsIndexChanged', None, self, 'fakeJavascript')

    def fakeJavascript(self):
        return "doSomething();"

    def test_setItems(self):
        self.element.setItems(range(0, 100))
        assert self.element.currentPageItems() == [0, 1, 2, 3, 4]
        self.test_validXML()

        self.element.insertVariables({'TestIndex':5})
        self.element.setItems(range(0, 100))
        assert self.element.currentPageItems() == [5, 6, 7, 8, 9]
        self.test_validXML()

        self.element.setItems(range(0, 4))
        assert self.element.currentPageItems() == [0, 1, 2, 3]
        self.test_validXML()
        assert self.element.nextButton.shown() == False
        assert self.element.lastButton.shown() == False

        self.element.setItems([])
        self.test_validXML()
        assert self.element.shown() == False

        #Show all toggled
        self.element.showAllButton.toggle()
        self.element.setItems(range(0, 100))
        assert self.element.currentPageItems() == range(0, 100)
        self.test_validXML()

    def test_jsSetNavigationIndex(self):
        assert self.fakeJavascript() in self.element.jsSetNavigationIndex(2)


class TestJumpToLetter(ElementTester):

    def setup_class(self):
        self.element = Factory.build('JumpToLetter', 'test')


class TestBreadCrumb(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build("BreadCrumb", "Test")
        self.homeLink = self.element.links[0]

    def test_attributes(self):
        assert self.element.trail == []
        assert len(self.element.links) == 1
        assert type(self.element.links[0]) == Link
        assert self.element.linkCount == 1
        assert self.element.currentText == 'Home'
        assert self.element.currentLocation == 'Home'

    def test_addLink(self):
        google = self.element.addLink("Google", "www.google.com")
        gmail = self.element.addLink("GMail", "www.gmail.com")
        simpleinnovation = self.element.addLink("Simple Innovation", "www.simpleinnovation.net")

        assert self.element.links == [self.homeLink, google, gmail,
                                         simpleinnovation]
        assert self.element.currentLocation == "www.simpleinnovation.net"
        assert self.element.currentText == "Simple Innovation"

    def test_insertVariables(self):
        #        [label]  [location]  [key]
        gmail = "Gmail[:]www.gmail.com[:]gm"
        simpleInnovation =  "Simple Innovation[:]www.simpleinnovation.net[:]si"
        google = "Google[:]www.google.com[:]goo"
        links = [gmail, simpleInnovation, google]
        valueDict = {'Test:HiddenData': "[/]".join(links)}
        self.element.insertVariables(valueDict)
        assert self.element.currentLocation == "www.google.com"
        assert self.element.currentText == "Google"
        assert self.element.linkCount == 4
        assert self.element.trail == [{'field': 'Home', 'term': 'gm'},
                                      {'field': 'www.gmail.com', 'term': 'si'},
                                      {'field': 'www.simpleinnovation.net', 'term': 'goo'}]

    def test_insertVariablesGoBackToLink(self):
        #        [label]  [location]  [key]
        gmail = "Gmail[:]www.gmail.com[:]gm"
        simpleInnovation =  "Simple Innovation[:]www.simpleinnovation.net[:]si"
        google = "Google[:]www.google.com[:]goo"
        arincdirect = "Arinc Direct[:]direct.arinc.net[:]ad"
        links = [gmail, simpleInnovation, google]

        valueDict = {'Test:LinkClicked':3,
                     'Test:HiddenData': "[/]".join(links)}
        self.element.insertVariables(valueDict)
        assert self.element.currentLocation == "www.simpleinnovation.net"
        assert self.element.currentText == "Simple Innovation"
        assert self.element.linkCount == 3
        assert self.element.trail == [{'field': 'Home', 'term': 'gm'},
                                         {'field': 'www.gmail.com', 'term': 'si'}]

        self.element.insertVariables({'Test:Location':'direct.arinc.net',
                                      'Test:Label':'Arinc Direct',
                                      'Test:Key':'ad'})
        assert self.element.currentLocation == "direct.arinc.net"
        assert self.element.currentText == "Arinc Direct"
