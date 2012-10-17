"""
   Name:
       Boxs

   Description:
       Elements that allow you to contain elements on the page
"""

import DOM
import Base
import Buttons
import Display
import Factory
import Fields
import HiddenInputs
import Inputs
import Layout
import UITemplate
from Factory import Composite
from MethodUtils import CallBack

Factory = Factory.Factory("Containers")


class DropDownMenu(Layout.Box):
    """
        Defines a dropdown menu webelement -- where clicking a button exposes or hides a menu.
    """
    __slots__ = ('toggle', 'menu', 'openOnly', 'parentElement')
    properties = Layout.Box.properties.copy()
    properties['openOnly'] = {'action':'classAttribute', 'type':'bool'}
    properties['parentElement'] = {'action':'classAttribute'}


    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id  and (id + "Container") or "", name, parent)
        self.toggle = None
        self.menu = None
        self.openOnly = False
        self.parentElement = None

    def setToggleButton(self, toggleButton, relation="WebElements.peer"):
        """
            Sets the button that controls the toggling of the menu

            toggleButton - the control button
            relation - the relational javascript method to call to get the menu aka "WebElements.peer" or
                      "WebElements.childElement"
        """
        self.toggle = toggleButton
        if self.id:
            self.toggle.id = self.id + ":Toggle"
        self.toggle.addJavascriptEvent('onclick',
                                       "WebElements.clickDropDown(%s(this, 'WMenu'), %s, this, %s);" %
                                        (relation, ((self.openOnly and "true") or "false"),
                                    (self.parentElement and "$('#%s')" % self.parentElement) or "null"))
        self.toggle.addClass("WToggle")
        return toggleButton

    def addChildElement(self, childElement):
        if not self.toggle:
            return self.setToggleButton(Layout.Box.addChildElement(self, childElement))
        elif not self.menu:
            self.menu = Layout.Box.addChildElement(self, childElement)
            if self.id:
                self.menu.id = self.id + ":Content"
            self.menu.addClass("WMenu")
            self.menu.addJavascriptEvent('onclick', 'WebElements.State.isPopupOpen = true;')
            self.menu.hide()
            return self.menu
        else:
            return Layout.Box.addChildElement(self, childElement)

Factory.addProduct(DropDownMenu)


class CollapsedText(DropDownMenu):
    """
        Shows a limited amount of text revealing the rest when the user hovers over
    """
    __slots__ = ('lengthLimit', '__text', 'label')
    properties = DropDownMenu.properties.copy()
    properties['lengthLimit'] = {'action':'classAttribute', 'type':'int'}
    properties['text'] = {'action':'setText'}

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        DropDownMenu.__init__(self, id, name, parent, **kwargs)

        self.lengthLimit = 40
        self.label = self.addChildElement(Display.Label)
        self.__text = None

        self.connect('beforeToHtml', None, self, '__updateUI__')

    def setText(self, text):
        """
            Sets the collapse able text
        """
        self.__text = text

    def __updateUI__(self):
        text = self.text()
        if len(text or '') > int(self.lengthLimit or 0):
            self.label.parent.addJavascriptEvent('onmouseover',
                                               "WebElements.displayDropDown(WebElements.peer(this, 'WMenu'));")
            self.label.parent.addJavascriptEvent('onmouseout', "WebElements.hide(WebElements.peer(this, 'WMenu'));")
            self.label.setText(text[:int(self.lengthLimit) - 3] + "...")
            self.completeText = self.addChildElement(Display.Label())
            self.completeText.setText(text)
            self.completeText.style['width'] = 240
        else:
            self.label.setText(text)

    def text(self):
        """
            Returns the set text
        """
        return self.__text

Factory.addProduct(CollapsedText)

class Autocomplete(Layout.Box):
    """
        A text box that opens a drop down menu upon editing
    """
    __slots__ = ('blockTab', 'menu', 'userInput')
    properties = Layout.Box.properties.copy()
    properties['blockTab'] = {'action':'classAttribute', 'type':'bool'}

    def __init__(self, id, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id + "Container", name, parent)

        self.blockTab = True
        self.menu = None
        self.userInput = None

        self.addChildElement(Inputs.TextBox(id))
        self.userInput.attributes['autocomplete'] = "off"
        self.userInput.addJavascriptEvent('onkeydown', CallBack(self, "jsShowIfActive"))
        self.userInput.addJavascriptEvent('onkeyup', CallBack(self, "jsShowIfActive"))
        self.userInput.addClass("WToggle")

        self.addScript("""if(!document.hasMenuClose){
                            document.hasMenuClose = true;
                            var AutoCompletePopup = null;
                            var MenuClicked = false;
                            var prevFunction = document.onclick;
                            document.onclick =
                            function CloseLastAutocompletePopup()
                            {
                                if(AutoCompletePopup && !MenuClicked){
                                    WebElements.hide(AutoCompletePopup)
                                }
                                if(prevFunction)prevFunction();
                                MenuClicked = false;
                            }
                          };""")

    def addChildElement(self, childElement):
        if not self.userInput:
            self.userInput = Layout.Box.addChildElement(self, childElement)
            return self.userInput
        if not self.menu:
            self.menu = Layout.Box.addChildElement(self, childElement)
            self.menu.id = self.id + ":Content"
            self.menu.addClass("WMenu")
            self.menu.hide()
            return self.menu
        else:
            return Layout.Box.addChildElement(self, childElement)

    def jsShowIfActive(self):
        return """if(event.keyCode != ENTER){
                    var menu = WebElements.peer(this, 'WMenu');
                    if(this.value""" + (self.blockTab and " && event.keyCode != TAB)" or ")") + """
                    {
                        WebElements.show(menu);
                        AutoCompletePopup = menu;
                    }
                    else
                    {
                        WebElements.hide(menu);
                        AutoCompletePopup = null;
                    }
                  }
                  """

Factory.addProduct(Autocomplete)


class Tab(Layout.Box):
    """
        A single tab - holds a single element(The tabs content) and the tabs label
    """
    __slots__ = ('text', '_textNode', 'tabLabel', 'imageName', 'isSelected')
    signals = Layout.Box.signals + ['selected', 'unselected']
    properties = Layout.Box.properties.copy()
    properties['select'] = {'action':'call', 'type':'bool'}
    properties['text'] = {'action':'classAttribute'}
    properties['imageName'] = {'action':'classAttribute'}
    Base.addChildProperties(properties, Display.Label, 'tabLabel')

    class TabLabel(Display.Label):
        """
            The label used to represent the tab in the tab-bar
        """
        __slots__ = ()
        def __init__(self, id, name=None, parent=None, **kwargs):
            Display.Label.__init__(self, id=id, name=name, parent=parent)
            self.addClass("WTabLabel")

        def select(self):
            """
                changes the class to reflect a selected tab label
            """
            self.removeClass('WUnselected')
            self.addClass('WSelected')

        def unselect(self):
            """
                changes the class to reflect an unselected tab label
            """
            self.removeClass('WSelected')
            self.addClass('WUnselected')

        @staticmethod
        def jsSelect(tab):
            return ("WebElements.removeClass(%(tab)s, 'WUnselected');"
                    "WebElements.addClass(%(tab)s, 'WSelected');") % {'tab':tab}

        @staticmethod
        def jsUnselect(tab):
            return ("WebElements.removeClass(%(tab)s, 'WSelected');"
                    "WebElements.addClass(%(tab)s, 'WUnselected');") % {'tab':tab}

    def __init__(self, id, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id=id, name=name, parent=parent)

        self.text = None
        self._textNode = Base.TextNode()
        self.tabLabel = self.TabLabel(id=self.id + "Label", parent=self)
        self.imageName = None
        self.unselect()

        self.tabLabel.connect('beforeToHtml', None, self, '__updateUI__')

    def __updateUI__(self):
        if self.imageName:
            image = self.tabLabel.addChildElement(Layout.Box())
            image.addClass(self.imageName)
            image.style['margin'] = "auto"
            image.style['clear'] = "both"

        self.tabLabel.addChildElement(self._textNode).setText(self.text or self.name)

    def select(self):
        """
            Displays the tab, and highlights the tab label
        """
        self.isSelected = True
        self.tabLabel.select()
        self.show()
        self.emit('selected')

    def unselect(self):
        """
            Unhighlights the tab label, and hides the tab
        """
        self.isSelected = False
        self.tabLabel.unselect()
        self.hide()
        self.emit('unselected')

Factory.addProduct(Tab)
TabLabel = Tab.TabLabel


class TabContainer(Base.WebElement):
    """
        TabContaier makes it easy to show association between several elements on a page via tabs
    """
    __slots__ = ('tabs', 'selectedTab', 'layout', '__tabLabelContainer__', '__tabContentContainer__')
    __layoutElement__ = Layout.Vertical
    __tabLayoutElement__ = Layout.Horizontal

    def __init__(self, id, name=None, parent=None, **kwargs):
        Base.WebElement.__init__(self, id, name, parent, **kwargs)

        self.tabs = {}
        self.selectedTab = None

        self.layout = self.addChildElement(self.__layoutElement__(id, name, parent))
        self.layout.addClass("W" + self.__class__.__name__)

        self.__tabLabelContainer__ = self.layout.addChildElement(self.__tabLayoutElement__())
        self.__tabLabelContainer__.addClass('WTabLabels')
        self.__tabContentContainer__ = self.layout.addChildElement(Layout.Box())
        self.__tabContentContainer__.addClass('WTabContents')

        self.addScript(CallBack(self, 'jsInit'))

    def jsInit(self):
        if self.selectedTab:
            return "var %s_selectedTab = '%s';" % (self.jsId(), self.selectedTab.jsId())
        return ""

    def jsSelectTab(self, tab):
        """
            Returns the javascript code to select an individual tab client side
        """
        return (("WebElements.hide(%(tabContainer)s_selectedTab);" +
                 tab.TabLabel.jsUnselect("%s_selectedTab + 'Label'" % self.jsId()) +
                 "%(tabContainer)s_selectedTab = '%(tab)s';"
                 "WebElements.show(%(tabContainer)s_selectedTab);" +
                 tab.TabLabel.jsSelect("'" + tab.jsId() + "Label'")) %
                    {'tab':tab.jsId(),
                     'tabContainer':self.jsId()})

    def selectTab(self, tabName):
        """
            Selects an individual tab based upon its name
        """
        tab = self.tabs[tabName]
        if tab == self.selectedTab:
            return
        elif self.selectedTab:
            self.selectedTab.unselect()

        self.selectedTab = tab
        tab.select()

    def addChildElement(self, element):
        if isinstance(element, Tab):
            element.tabLabel.addJavascriptEvent('onclick', self.jsSelectTab(element))
            self.tabs[element.name] = element
            element.id = self.id + element.name.capitalize()
            element.tabLabel.id = element.id + "Label"
            element.connect('selected', None, self, 'selectTab', element.name)
            if not self.selectedTab or element.isSelected:
                element.select()

            self.__tabLabelContainer__.addChildElement(element.tabLabel)
            return self.__tabContentContainer__.addChildElement(element)
        else:
            return Base.WebElement.addChildElement(self, element)

Factory.addProduct(TabContainer)


class VerticalTabContainer(TabContainer):
    __layoutElement__ = Layout.Horizontal
    __tabLayoutElement__ = Layout.Vertical

Factory.addProduct(VerticalTabContainer)


class Accordion(Layout.Vertical):
    """
        Defines an accordion, a labeled section of the page, that upon clicking the label has its visibility
        toggled
    """
    __slots__ = ('toggle', 'toggleImage', 'toggleLabel', 'isOpen', 'contentElement')
    jsFunctions = ['toggleAccordion']
    properties = Layout.Box.properties.copy()
    properties['open'] = {'action':'call', 'type':'bool'}
    properties['label'] = {'action':'setLabel'}

    def __init__(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical.__init__(self, id, name, parent, **kwargs)
        self.addClass("WAccordion")

        self.toggle = self.addChildElement(Layout.Horizontal())
        self.toggle.addClass('AccordionToggle')
        self.toggle.addJavascriptEvent('onclick', CallBack(self, 'jsToggle'))
        self.toggleImage = self.toggle.addChildElement(Display.Image(id + "Image"))
        self.toggleImage.addClass('AccordionImage')
        self.toggleLabel = self.toggle.addChildElement(Display.Label())
        self.toggleLabel.addClass('AccordionLabel')
        self.isOpen = self.toggle.addChildElement(HiddenInputs.HiddenBooleanValue(id + "Value"))
        self.contentElement = self.addChildElement(Layout.Box(id + "Content"))
        self.contentElement.addClass('AccordionContent')
        self.addChildElementsTo = self.contentElement

        self.isOpen.connect('valueChanged', True, self, 'open')
        self.isOpen.connect('valueChanged', False, self, 'close')
        self.close()

        self.addJSFunctions(Accordion)

    def setLabel(self, text):
        """
            Sets the toggle label text
        """
        self.toggleLabel.setText(text)

    def jsToggleOn(self):
        """
            Returns the javascript that will toggle the label on client side
        """
        return """if (!WebElements.shown('%s')){
                     WebElements.show('%s');
                     WebElements.get('%s').value = 'True';
                     WebElements.get('%s').src = 'images/hide.gif'
                """ % (self.contentElement.jsId(), self.contentElement.jsId(),
                       self.isOpen.jsId(), self.toggleImage.jsId())

    def jsToggleOff(self):
        """
            Returns the javascript that will toggle the label off client side
        """
        return """if (WebElements.shown('%s')){
                     WebElements.hide('%s');
                     WebElements.get('%s').value = 'False';
                     WebElements.get('%s').src = 'images/show.gif'
                """ % (self.contentElement.jsId(), self.contentElement.jsId(),
                       self.isOpen.jsId(), self.toggleImage.jsId())

    def jsToggle(self):
        """
            Returns the javascript that will set the toggled state to the reverse of its current state client side
        """
        return "toggleAccordion('%s', '%s', '%s');" % (self.contentElement.jsId(), self.toggleImage.jsId(),
                                                   self.isOpen.jsId())
    @staticmethod
    def toggleAccordion(elementContent, elementImage, elementValue):
        return """if(!WebElements.shown(elementContent)){
                     WebElements.show(elementContent);
                     elementValue.value = 'True';
                     elementImage.src = 'images/hide.gif'
                  }
                  else
                  {
                     WebElements.hide(elementContent);
                     elementValue.value = 'False';
                     elementImage.src = 'images/show.gif'
                  }"""

    def open(self):
        """
            Makes the accordions content visible
        """
        self.toggleImage.setProperty('src', 'images/hide.gif')
        self.contentElement.show()
        self.isOpen.setValue(True)

    def close(self):
        """
            Hides the accordions content
        """
        self.toggleImage.setProperty('src', 'images/show.gif')
        self.contentElement.hide()
        self.isOpen.setValue(False)


Factory.addProduct(Accordion)


class FormContainer(DOM.Form):
    """
        Defines a form container web element - a portion of the page that contains fields to be submitted back to
        the server.
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        DOM.Form.__init__(self, id, name, parent, **kwargs)
        self.setProperty('method', 'POST')

    def validators(self, useFullId=True):
        """
            Returns a list of all validators associated with this element and all child elements:   -
                useFullId - if set to True the validators are set against the prefix + id   -
        """
        validatorDict = {}
        validator = getattr(self, 'validator', None)
        if self.editable() and validator:
            validatorDict['chained_validators'] = validator

        for child in self.childElements:
            validatorDict.update(child.validators(useFullId))

        return validatorDict

Factory.addProduct(FormContainer)


class ActionBox(Layout.Vertical):
    """
        Defines a list of actions grouped together under a header
    """
    __slots__ = ('header', 'actions')
    properties = Layout.Vertical.properties.copy()
    properties['header'] = {'action':'header.setText'}

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Layout.Vertical.__init__(self, id, name, parent, **kwargs)
        self.addClass("WActionBox")

        self.header = self.addChildElement(Display.Label())
        self.header.addClass("WActionBoxHeader")

        self.actions = self.addChildElement(Display.List())

    def addChildElement(self, childElement, ensureUnique=False):
        if type(childElement) == Buttons.Link:
            return self.actions.addChildElement(childElement)
        else:
            return Layout.Vertical.addChildElement(self, childElement, ensureUnique=ensureUnique)

Factory.addProduct(ActionBox)
