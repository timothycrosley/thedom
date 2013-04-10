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

from . import Base
from . import Buttons
from . import ClientSide
from . import Containers
from . import Display
from . import HiddenInputs
from . import Inputs
from . import Layout
from . import UITemplate
from .Factory import Factory
from .IteratorUtils import iterableLength
from .MethodUtils import CallBack
from .PositionController import PositionController
from .StringUtils import interpretAsString
from .MultiplePythonSupport import *

Factory = Factory("Navigation")


class ItemPager(Layout.Vertical):
    """
        Paged Results:
        Encapsulates the UI logic for paging multiple item from a database or other source.
    """
    __slots__ = ('resultsStartAt', 'numberOfResults', 'showAllButton', 'startButton', 'backButton', 'pageLinks',
                 'nextButton', 'lastButton', 'pagesShownAtOnce', 'itemsPerPage', '_index_', '_pages_',
                 'resultsEndAt')
    signals = Base.TemplateElement.signals + ['jsIndexChanged']
    properties = Base.TemplateElement.properties.copy()
    properties['itemsPerPage'] = {'action':'classAttribute', 'type':'int'}
    properties['pagesShownAtOnce'] = {'action':'classAttribute', 'type':'int'}

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
        self.startButton.setText("&lt;&lt;")
        self.startButton.setDestination("#Link")

        self.backButton = buttonLayout.addChildElement(Buttons.Link())
        self.backButton.setText("&lt; Back")
        self.backButton.setDestination("#Link")
        self.backButton.addClass("WSpaced")

        self.pageLinks = buttonLayout.addChildElement(Layout.Flow())

        self.nextButton = buttonLayout.addChildElement(Buttons.Link())
        self.nextButton.setText("Next &gt;")
        self.nextButton.setDestination("#Link")

        self.lastButton = buttonLayout.addChildElement(Buttons.Link())
        self.lastButton.setText("&gt;&gt;")
        self.lastButton.setDestination("#Link")
        self.lastButton.addClass("WSpaced")

        self.pagesShownAtOnce = 15
        self.itemsPerPage = 25
        self._index_ = self.addChildElement(HiddenInputs.HiddenIntValue(id + 'Index'))
        self._pages_ = None

        self.showAllButton.addJavascriptEvent('onclick', "WebElements.replace(this, WebElements.buildThrobber());")
        self.showAllButton.connect('jsToggled', None, self, 'jsSetNavigationIndex', 0)
        self.showAllButton.connect('toggled', True, self.showAllButton, 'setValue', 'Show in Pages')
        self.showAllButton.connect('toggled', False, self.showAllButton, 'setValue', 'Show All')

    def setItems(self, items=None):
        """
            Set a list of items for the item pager to page-through
        """
        itemsPerPage = int(self.itemsPerPage)
        if iterableLength(items) <= itemsPerPage:
            self.showAllButton.remove()
        elif self.showAllButton.toggled():
            itemsPerPage = iterableLength(items)

        self._pages_ = PositionController(items=items or [], startIndex=self._index_.value(),
                                          itemsPerPage=itemsPerPage,
                                          pagesShownAtOnce=int(self.pagesShownAtOnce))
        self._index_.setValue(self._pages_.startIndex)

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

    def jsSetNavigationIndex(self, index):
        """
            Creates the javascript to switch to a different position within the items:
            index - the first item you want to appear in your pages results
        """
        return ("WebElements.get('%(id)sIndex').value = '%(index)d';%(handlers)s;" %
                {'id':self.fullId(), 'index':index, 'handlers':"\n".join([ClientSide.var(result) for result in
                                                                          self.emit('jsIndexChanged')])})

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
            self.nextButton.addJavascriptEvent('onclick', self.jsSetNavigationIndex(self._pages_.nextPageIndex))
            self.lastButton.addJavascriptEvent('onclick', self.jsSetNavigationIndex(self._pages_.lastPageIndex))
        else:
            self.nextButton.hide()
            self.lastButton.hide()

        if self._pages_.arePrev:
            self.backButton.show()
            self.startButton.show()
            self.backButton.addJavascriptEvent('onclick', self.jsSetNavigationIndex(self._pages_.prevPageIndex))
            self.startButton.addJavascriptEvent('onclick', self.jsSetNavigationIndex(0))
        else:
            self.backButton.hide()
            self.startButton.hide()

        pageList = self._pages_.pageList()
        if len(pageList) > 1:
            for page in self._pages_.pageList():
                link = self.pageLinks.addChildElement(Buttons.Link())
                link.setText(unicode(page / self._pages_.itemsPerPage + 1))
                link.addClass('WSpaced')
                if page != self._index_.value():
                    link.setDestination('#Link')
                    link.addJavascriptEvent('onclick', self.jsSetNavigationIndex(page))

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


class BreadCrumb(Layout.Box):
    """
        Defines a dynamically built navigation breadcrumb
    """
    __slots__ = ('hiddenData', 'prevLinkClicked', 'location', 'label', 'currentLocation', 'currentText', 'formName',
                 'linkCount', 'links', 'trail', 'currentLink')
    properties = Layout.Box.properties.copy()
    properties['formName'] = {'action':'classAttribute'}

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id, name, parent, **kwargs)
        self.addClass("WBreadCrumb")

        hiddenData = Inputs.TextBox(id + ':HiddenData')
        hiddenData.attributes['type'] = 'hidden'
        self.hiddenData = self.addChildElement(hiddenData)

        prevLinkClicked = Inputs.TextBox(id + ':LinkClicked')
        prevLinkClicked.attributes['type'] = 'hidden'
        self.prevLinkClicked = self.addChildElement(prevLinkClicked)

        location = Inputs.TextBox(id + ':Location')
        location.attributes['type'] = 'hidden'
        self.location = self.addChildElement(location)

        label = Inputs.TextBox(id + ':Label')
        label.attributes['type'] = 'hidden'
        self.label = self.addChildElement(label)

        key = Inputs.TextBox(id + ':Key')
        key.attributes['type'] = 'hidden'
        self.key = self.addChildElement(key)

        self.currentLocation = ''
        self.currentText = ''
        self.formName = "setMe"

        self.linkCount = 0
        self.links = []
        self.addLink('Home', 'Home')

        self.addScript(CallBack(self, 'jsSubmitLink'))

        self.trail = []

    def _render(self):
        Layout.Box._render(self)
        self.highlightCurrentLink()

    def addLink(self, text, location, key=None):
        """
            Adds a link to the breadcumb that can be clicked to return to a previous location
        """
        key = key or text

        if self.currentLocation:
            self.trail.append({'field':self.currentLocation, 'term':key})

            spacer = Display.Label('spacer')
            spacer.setText(' >> ')
            self.addChildElement(spacer)

            value = self.hiddenData.value()
            if value:
                value += '[/]'
            value += text + '[:]' + location + '[:]' + key
            self.hiddenData.setValue(value)

        link = Buttons.Link('breadcrumb')
        link.addClass("WCrumb")
        link.setText(text)
        link.name = unicode(self.linkCount)
        link.addJavascriptEvent('onclick', "submitLink('" + text + "', '" +
                                                       location + "', '" +
                                                       key + "', '" +
                                                       unicode(self.linkCount) + "');")

        self.currentLocation = location
        self.currentText = text
        self.addChildElement(link)
        self.currentLink = link
        self.linkCount += 1
        self.links.append(link)
        return link

    def filterDict(self):
        """
            Returns a dictionary of field - term, to represent your current location based on the breadcrumbs
        """
        data = {}
        for location in self.trail:
            data[location['field']] = location['term']

        return data

    def jsSubmitLink(self):
        """
            Returns the javascript that will change your location in the breadcrumb trail clientside
        """
        return """
                function submitLink(label, view, key, index){
                    if(index != null){
                        link = WebElements.get('""" + self.prevLinkClicked.id + """');
                        link.value = index;
                    }
                    if(key == null){
                        key = label;
                    }

                    WebElements.get('""" + self.label.id  + """').value = label;
                    WebElements.get('""" + self.location.id + """').value = view;
                    WebElements.get('""" + self.key.id + """').value = key;
                    WebElements.get('""" + self.formName + """').submit();
                }
               """

    def highlightCurrentLink(self):
        """
            Updates the display of the current link to reflected its highlighted status
        """
        self.currentLink.removeClass('WCrumb')

    def insertVariables(self, valueDict=None):
        """
            Overrides insert variables to update the displayed status of the breadcrumb and compute the
            current location and trail.
        """
        Layout.Box.insertVariables(self, valueDict)

        clicked = 'none'
        if self.prevLinkClicked.value():
            clicked = int(self.prevLinkClicked.value())

        links = self.hiddenData.value()
        self.hiddenData.setValue('')
        self.prevLinkClicked.setValue('')
        if clicked != 0:
            if links:
                current = 1
                for link in links.split('[/]'):
                    if current == clicked:
                        break

                    label, location, key = link.split('[:]')
                    self.addLink(label, location, key)

                    current += 1

            if self.location.value():
                self.addLink(self.label.value(),
                             self.location.value(),
                             self.key.value())
                self.location.setValue('')
                self.label.setValue('')
                self.key.setValue('')

Factory.addProduct(BreadCrumb)


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
                       "    valueElement.onchange();"
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

        key = interpretAsString(key)
        value = interpretAsString(value)
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


class TimeFrame(Layout.Horizontal):
    """
        Allows a user to select the time frame from which items will appear
    """
    __slots__ = ('anyTime', 'hours24', 'days7', 'days14', 'helpDropDown', 'help', 'days')
    signals = Base.TemplateElement.signals + ['jsTimeFrameChanged']
    properties = Layout.Horizontal.properties.copy()
    properties['help'] = {'action':'help.setText'}
    properties['disableAnyTime'] = {'action':'call', 'type':'bool'}

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Horizontal._create(self, id, name, parent, **kwargs)
        self.style['margin-top'] = '2px'
        self.addClass("WTimeFrame")

        label = self.addChildElement(Display.Label())
        label.setText('Show Timeframe:')
        label.addClass("WLabel")

        self.anyTime = self.addChildElement(Buttons.Link())
        self.anyTime.addClass('WSpaced')
        self.anyTime.setText('All,')

        self.hours24 = self.addChildElement(Buttons.Link())
        self.hours24.addClass('WSpaced')
        self.hours24.setText('24 Hours,')

        self.days7 = self.addChildElement(Buttons.Link())
        self.days7.addClass('WSpaced')
        self.days7.setText('7 Days,')

        self.days14 = self.addChildElement(Buttons.Link())
        self.days14.addClass('WSpaced')
        self.days14.setText('14 Days')

        self.helpDropDown = self.addChildElement(Containers.DropDownMenu('help'))
        helpLink = self.helpDropDown.addChildElement(Buttons.Link())
        helpLink.setText("(Describe Time Frame)")
        helpLink.setDestination("#Link")
        self.help = self.helpDropDown.addChildElement(Display.Label())
        self.help.setText("Help text goes here")

        self.days = self.addChildElement(HiddenInputs.HiddenIntValue(id + ":days"))
        self.days.addClass('Value')

    def disableAnyTime(self):
        """
            Will display the anyTime option in addition to the 14 days, 7 days and 1 day options
        """
        self.anyTime.remove()
        if self.days.value() == 0:
            self.days.setValue(1)

    def _render(self):
        Layout.Horizontal._render(self)
        setTimeFrame = ("WebElements.stealClassFromPeer(this, 'selected');WebElements.peer(this, 'Value').value = '%d';" +
                        "".join(self.emit("jsTimeFrameChanged")))
        valueMap = {0:self.anyTime, 1:self.hours24, 7:self.days7, 14:self.days14}
        for value, element in iteritems(valueMap):
            element.addJavascriptEvent('onclick', setTimeFrame % value)
        valueMap[self.days.value()].addClass('selected')

Factory.addProduct(TimeFrame)
