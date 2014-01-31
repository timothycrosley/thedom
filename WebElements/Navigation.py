'''
    Navigation.py

    Contains elements that aid in page navigation

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

from . import Base, Buttons, ClientSide, Containers, Display, HiddenInputs, Inputs, Layout, UITemplate
from .Factory import Factory
from .IteratorUtils import iterableLength
from .MethodUtils import CallBack
from .MultiplePythonSupport import *
from .PositionController import PositionController
from .Types import Safe

Factory = Factory("Navigation")


class ItemPager(Layout.Vertical):
    """
        Paged Results:
        Encapsulates the UI logic for paging multiple item from a database or other source.
    """
    __slots__ = ('resultsStartAt', 'numberOfResults', 'showAllButton', 'startButton', 'backButton', 'pageLinks',
                 'nextButton', 'lastButton', 'pagesShownAtOnce', 'itemsPerPage', '_index_', '_pages_',
                 'resultsEndAt', 'updateJS')
    signals = Base.TemplateElement.signals + ['jsIndexChanged']
    properties = Base.TemplateElement.properties.copy()
    properties['itemsPerPage'] = {'action':'classAttribute', 'type':'int'}
    properties['pagesShownAtOnce'] = {'action':'classAttribute', 'type':'int'}

    class ClientSide(Layout.Vertical.ClientSide):

        def control(self, pageControl, silent=True, timeout=None):
            return self.onChange(pageControl.clientSide.get(silent=silent, timeout=timeout, params=self.params))

        def onChange(self, event):
            return ClientSide.onPagerChange(self, event)

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical._create(self, id, name, parent, **kwargs)

        positionLayout = self.addChildElement(Layout.Horizontal())
        positionLayout.addClass("WActions")
        label = positionLayout.addChildElement(Display.Label())
        label.setText('Showing Results')
        label.addClass('WSpaced')

        self.resultsStartAt = positionLayout.addChildElement(Display.Label())
        self.resultsStartAt.makeStrong()
        self.resultsStartAt.setText('1')
        self.resultsStartAt.addClass('WSpaced')

        label = positionLayout.addChildElement(Display.Label())
        label.setText('-')
        label.addClass('WSpaced')

        self.resultsEndAt = positionLayout.addChildElement(Display.Label())
        self.resultsEndAt.makeStrong()
        self.resultsEndAt.setText('25')
        self.resultsEndAt.addClass('WSpaced')

        label = positionLayout.addChildElement(Display.Label())
        label.setText('out of')
        label.addClass('WSpaced')

        self.numberOfResults = positionLayout.addChildElement(Display.Label())
        self.numberOfResults.makeStrong()
        self.numberOfResults.setText('100')
        self.numberOfResults.addClass('WSpaced')

        self.showAllButton = positionLayout.addChildElement(Buttons.ToggleButton('showAllButton'))
        self.showAllButton.setText("Show All")

        buttonLayout = self.addChildElement(Layout.Horizontal())

        self.startButton = buttonLayout.addChildElement(Buttons.Link())
        self.startButton.setText("<<")
        self.startButton.setDestination("#Link")

        self.backButton = buttonLayout.addChildElement(Buttons.Link())
        self.backButton.setText("< Back")
        self.backButton.setDestination("#Link")
        self.backButton.addClass("WSpaced")

        self.pageLinks = buttonLayout.addChildElement(Layout.Flow())

        self.nextButton = buttonLayout.addChildElement(Buttons.Link())
        self.nextButton.setText("Next >")
        self.nextButton.setDestination("#Link")

        self.lastButton = buttonLayout.addChildElement(Buttons.Link())
        self.lastButton.setText(">>")
        self.lastButton.setDestination("#Link")
        self.lastButton.addClass("WSpaced")

        self.pagesShownAtOnce = 15
        self.itemsPerPage = 25
        self._index_ = self.addChildElement(HiddenInputs.HiddenIntValue(id + 'Index'))
        self._pages_ = None

        self.showAllButton.connect('toggled', True, self.showAllButton, 'setValue', 'Show in Pages')
        self.showAllButton.connect('toggled', False, self.showAllButton, 'setValue', 'Show All')

    def setItems(self, items=None):
        """
            Set a list of items for the item pager to page-through
        """
        pageLimit = int(self.itemsPerPage)
        if self.showAllButton.toggled():
            itemsPerPage = iterableLength(items)
        else:
            itemsPerPage = pageLimit
        self._pages_ = PositionController(items=items or [], startIndex=self._index_.value(),
                                          itemsPerPage=itemsPerPage,
                                          pagesShownAtOnce=int(self.pagesShownAtOnce))
        self._index_.setValue(self._pages_.startIndex)

        if self._pages_.length <= pageLimit:
            self.showAllButton.remove()

    def currentPageItems(self, allItems=None, requestFields=None):
        """
            The items contained in the currently highlighted page

            optionally pass all available items and the current requests fields-dict
            to set and retrieve with a single call.
        """
        if requestFields is not None:
            self.insertVariables(requestFields)
        if allItems is not None:
            self.setItems(allItems)
        return self._pages_ and self._pages_.currentPageItems or ()

    def _render(self):
        """
            Updates the ui to reflect the currently selected page and provide links to other pages
        """
        Layout.Vertical._render(self)
        if not self._pages_:
            return
        elif not self.currentPageItems():
            self.hide()
            return

        self.resultsStartAt.setText(self._pages_.startPosition)
        self.resultsEndAt.setText(self._pages_.nextPageIndex)
        self.numberOfResults.setText(self._pages_.length)

        if self._pages_.areMore:
            self.nextButton.show()
            self.lastButton.show()
            self.nextButton.attributes['index'] = self._pages_.nextPageIndex
            self.lastButton.attributes['index'] = self._pages_.lastPageIndex
        else:
            self.nextButton.hide()
            self.lastButton.hide()

        if self._pages_.arePrev:
            self.backButton.show()
            self.startButton.show()
            self.backButton.attributes['index'] = self._pages_.prevPageIndex
            self.startButton.attributes['index'] = 0
        else:
            self.backButton.hide()
            self.startButton.hide()

        pageList = self._pages_.pageList()
        if len(pageList) > 1:
            for page in self._pages_.pageList():
                if page == self._index_.value():
                    pageElement = self.pageLinks.addChildElement(Display.Label())
                else:
                    pageElement = self.pageLinks.addChildElement(Buttons.Link())
                    pageElement.setDestination('#Link')
                    pageElement.attributes['index'] = page

                pageElement.setText(unicode(page / self._pages_.itemsPerPage + 1))
                pageElement.addClass('WSpaced')

Factory.addProduct(ItemPager)


class JumpToLetter(Layout.Vertical):
    """
        Provides a simple set of links that allow a user to jump to a particular letter
    """
    __slots__ = ('__letterMap__', 'selectedLetter')
    letters = map(chr, xrange(ord('A'), ord('Z') + 1))

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical._create(self, id, name, parent, **kwargs)
        self.addClass("WJumpToLetter")
        self.style['float'] = "left"

        self.__letterMap__ = {}
        self.selectedLetter = self.addChildElement(HiddenInputs.HiddenValue(self.id + "SelectedLetter"))
        for letter in self.letters:
            link = self.addChildElement(Buttons.Link())
            link.addClass("WLetter")
            link.setText(letter)

            self.__letterMap__[letter] = link

        self.selectedLetter.connect('valueChanged', None, self, "selectLetter")

        self.addScript("function letterJumpHover(letterJump){"
                       "    var letterJump = WebElements.get(letterJump);"
                       "    letterJump.paddingBottom = '4px';"
                       "    letterJump.paggingTop = '3px';"
                       "}")
        self.addScript("function letterJumpLeave(letterJump){"
                       "    var letterJump = WebElements.get(letterJump);"
                       "    letterJump.paddingBottom = '10px';"
                       "    letterJump.paggingTop = '10px';"
                       "}")
        self.addScript("function l(letterJump, letter){"
                       "    WebElements.get(letterJump).value = letter;"
                       "}")

    def _render(self):
        Layout.Vertical._render(self)
        fullId = self.fullId()
        for letter, link in iteritems(self.__letterMap__):
            if letter == self.selectedLetter.value():
                link.addClass("WLetterSelected")
            else:
                link.setDestination("#" + letter)
                if not link.javascriptEvent('onmouseover'):
                    link.addJavascriptEvent("onmouseover", "letterJumpHover('%s');" % fullId)
                    link.addJavascriptEvent("onmouseout", "letterJumpLeave('%s')" % fullId)
                    link.addJavascriptEvent("onclick", "letterSelect('%s', '%s');" % (fullId, letter))

    def clearSelection(self):
        """
            Deselects the currently selected letter (if there is one)
        """
        self.selectedLetter.setValue('')

    def selectLetter(self, letter):
        """
            Selects the passed in letter
        """
        self.selectedLetter.setValue(letter)

    def unselectLetter(self, letter):
        """
            Unselects the letter if it matches letter, otherwise does nothing
        """
        if letter == self.selectedLetter:
            self.selectedLetter.setValue('')

Factory.addProduct(JumpToLetter)


class UnrolledSelect(Display.List):
    """
         A select input implementation where all options are visible at once but only one is selectable
    """
    __slots__ = ('userInput', 'optionList', '_lastAdded')

    def _create(self, id, name=None, parent=None, **kwargs):
        Display.List._create(self, None, None, parent)
        self.addChildElement(Display.Label()).addClass('first')
        self.addClass('WUnrolledSelect')
        self.userInput = HiddenInputs.HiddenValue(id, parent=self)
        self.childElements.append(self.userInput)
        self.userInput.addClass("Value")
        self.optionList = []

        self.addScript("function selectUnrolledOption(option)"
                       "{"
                       "    var valueElement = WebElements.fellowChild(option, 'WUnrolledSelect', 'Value');"
                       "    valueElement.value = option.name;"
                       "    WebElements.stealClassFromFellowChild(option, 'WUnrolledSelect', 'selected');"
                       "}")

        self._lastAdded = False

    def _render(self):
        if not self._lastAdded:
            self.addChildElement(Display.Label()).addClass('last')
            self._lastAdded = True

    def addOptions(self, options, displayKeys=False):
        """
            Adds a group of options to a select box:

            options - Takes a dictonary of option keys to option values
                      or a straight list of option names

            displayKeys(False) - if dictionaries keys will be used for display and the values
                                 will be used for keys
        """
        if isinstance(options, dict):
            for key, value in iteritems(options):
                self.addOption(key, value, displayKeys)
        else:
            for option in options:
                if type(option) in (list, tuple):
                    self.addOption(option[0], option[1])
                else:
                    self.addOption(option)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds a options based on a list of tuple(name-value) pairs
        """
        for option in options:
            name = option['name']
            value = option['value']
            self.addOption(name, value, displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds a new option that can be selected
        """
        newOption = Buttons.Link()
        newOption.setDestination("#Link")
        if not self.optionList:
            newOption.addClass('selected')
        if not value:
            value = key

        if displayKeys:
            newOption.name = value
            newOption.setText(key)
        else:
            newOption.name = key
            newOption.setText(value)

        newOption.addJavascriptEvent('onclick', 'selectUnrolledOption(this);')

        self.optionList.append(newOption)
        return self.addChildElement(newOption)

    def options(self):
        """
            Returns a list of all available options
        """
        options = {}
        for option in self.optionList:
            options[option.name] = option.text()

        return options

    def selected(self):
        """
            Returns the selected item
        """
        for option in self.childElements:
            if option.selected():
                return option

    def setValue(self, value):
        """
            Selects a child select option
        """
        for option in self.optionList:
            if option.name == "value":
                option.addClass('selected')
            else:
                option.removeClass('selected')

    def value(self):
        """
            Returns the value of the currently selected item
        """
        for option in self.optionList:
            if option.hasClass('selected'):
                return option.name

Factory.addProduct(UnrolledSelect)
