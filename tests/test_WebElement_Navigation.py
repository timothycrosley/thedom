'''
    test_Navigation.py

    Tests the functionality of thedom/Navigation.py

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
from thedom.Buttons import Link


class TestItemPager(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build('ItemPager', 'Test')
        self.element.itemsPerPage = 5
        self.element.pagesShownAtOnce = 15

    def test_noIetms(self):
        self.element.currentPageItems() == ()

    def test_setItems(self):
        self.element.setItems(range(0, 100))
        assert list(self.element.currentPageItems()) == list(range(0, 5))
        self.test_validXML()

        self.element.insertVariables({'TestIndex':5})
        self.element.setItems(range(0, 100))
        assert list(self.element.currentPageItems()) == list(range(5, 10))
        self.test_validXML()

        self.element.setItems(range(0, 4))
        assert list(self.element.currentPageItems()) == list(range(0, 4))
        self.test_validXML()
        assert self.element.nextButton.shown() == False
        assert self.element.lastButton.shown() == False

        self.element.setItems([])
        self.test_validXML()
        assert self.element.shown() == False

        #Show all toggled
        self.element.showAllButton.toggle()
        self.element.setItems(range(0, 100))
        assert list(self.element.currentPageItems()) == list(range(0, 100))
        self.test_validXML()


class TestJumpToLetter(ElementTester):

    def setup_class(self):
        self.element = Factory.build('JumpToLetter', 'test')
