'''
   Fields.py

   Defines complex fields that are created using multiple WebElements

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

import json
import types

import operator
from . import Base, Buttons, Display, DOM, Factory, HiddenInputs, Inputs, Layout, ToClientSide, UITemplate
from .Factory import Composite
from .MethodUtils import CallBack
from .MultiplePythonSupport import *
from .StringUtils import interpretAsString, listReplace

Factory = Factory.Factory("Fields")

class BaseField(Layout.Box):
    """
        Base field implementation where a field is defined as:
            a label, input, and validator paired together
    """
    __slots__ = ('submitIfDisabled', 'layout', 'inputContainer', 'label', 'inputAndActions', 'userInput',
                 'fieldActions', 'formError')
    inputElement = None
    properties = Base.WebElement.properties.copy()
    Base.addChildProperties(properties, Display.Label, 'label')
    properties['labelContainerStyle'] = {'action':'labelContainer.setStyleFromString'}
    properties['text'] = {'action':'setText'}
    properties['setApart'] = {'action':'call', 'type':'bool'}
    properties['value'] = {'action':'setValue'}
    properties['labelStyle'] = {'action':'label.setStyleFromString'}
    properties['inputStyle'] = {'action':'userInput.setStyleFromString'}
    properties['required'] = {'action' : 'call' , 'name' : 'setRequired', 'type':'bool'}
    properties['key'] = {'action':'userInput.classAttribute'}
    properties['submitIfDisabled'] = {'action':'setSubmitIfDisabled', 'type':'bool'}
    properties['flip'] = {'action':'call', 'type':'bool'}

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id + "Field", name, parent)
        self.submitIfDisabled = False

        self.layout = self.addChildElement(Layout.Vertical(id + "Container"))
        self.inputContainer = self.layout.addChildElement(Layout.Horizontal())

        self.label = self.inputContainer.addChildElement(Display.Label())

        self.inputAndActions = self.inputContainer.addChildElement(Layout.Horizontal())
        self.userInput = self.inputAndActions.addChildElement(self.inputElement(id, name=name))
        self.fieldActions = self.inputAndActions.addChildElement(Layout.Box())
        self.addChildElementsTo = self.fieldActions

        errorContainer = self.layout.addChildElement(Layout.Horizontal())
        self.formError = errorContainer.addChildElement(Display.FormError(id, parent=self))
        self.layout.addChildElement(errorContainer)

    def flip(self):
        self.inputAndActions.replaceWith(self.label)
        self.label.replaceWith(self.inputAndActions)

    def _render(self):
        """
            Remove form error placeholder if field is not validatable - update read only status - update label
        """
        Layout.Box._render(self)

        if not self.formError.name:
            self.formError.remove()

        self.__updateReadOnly__()

        self.label.attributes.setdefault('for', self.userInput.fullId())

    def __updateReadOnly__(self):
        if not self.editable() and self.submitIfDisabled:
            # Creates a hidden input for a disabled field so that the field value
            # is still submitted even if the field is set as read-only
            value = self.value()
            if type(value) != list:
                value = [value,]
            for val in value:
                hiddenValue = HiddenInputs.HiddenValue(name=self.name)
                hiddenValue.setValue(val)
                self.addChildElement(hiddenValue)

    def setSubmitIfDisabled(self, submit):
        """
            If set to true the value will still be passed through on a submit even if the field is disabled
        """
        self.submitIfDisabled = submit

    def changeId(self, newId):
        """
            Updates the id for not only the field but the associated userInput and formError
        """
        self.userInput.id = newId
        self.userInput.name = newId
        self.formError.name = newId
        self.id = newId + "Field"

    def validators(self, useFullId=True):
        """
            Returns the validators associated with the field
        """
        validators = Layout.Box.validators(self, useFullId=useFullId)
        if useFullId:
            validators.pop(self.fullId(), None)
        else:
            validators.pop(self.id, None)

        validator = getattr(self, 'validator', None)
        if self.editable() and self.shown() and validator:
            if useFullId:
                id = self.userInput.fullId()
            else:
                id = self.userInput.id
            validators[id] = validator

        return validators

    def setRequired(self):
        """
            Sets the field to required and changes the display to communicate that to the user
        """
        label = Display.Label()
        label.addClass("Required")
        label.setText('*')
        self.userInput.addClass("RequiredField")
        self.label.addChildElement(label)

    def setValue(self, value):
        """
            Sets the value for the fields input element
        """
        self.userInput.setValue(value)

    def value(self):
        """
            Returns the value set on the input element of the field
        """
        return self.userInput.value()

    def setText(self, text):
        """
            Sets the displayed text associated with the field
        """
        self.label.setText(text)

    def text(self):
        """
            Returns the displayed text associated with the field
        """
        return self.label.text()

    def setApart(self):
        """
            Moves the label and field away from each other (seperated as far left-right as possible)
        """
        self.inputAndActions.parent.style['float'] = 'right'
        self.formError.parent.style['float'] = 'right'


class InputField(BaseField):
    """
        A field using an input element
    """
    __slots__ = ()
    inputElement = Inputs.InputElement
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.InputElement, 'userInput')
    properties['type'] = {'action':'userInput.attribute', 'name':'type'}

Factory.addProduct(InputField)


class TextField(BaseField):
    """
        A field with a textbox as the input
    """
    __slots__ = ()
    inputElement = Inputs.TextBox
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.TextBox, 'userInput')

Factory.addProduct(TextField)


class RadioField(BaseField):
    """
        A field with a radio button as the input
    """
    __slots__ = ()
    inputElement = Inputs.Radio
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.Radio, 'userInput')

    def __updateReadOnly__(self):
        # Only create the hidden input if the original radio button is selected to simulate
        # how an actual radio control would work
        if not self.editable() and self.submitIfDisabled and self.value():
            hiddenValue = HiddenInputs.HiddenValue(name=self.name)
            hiddenValue.setValue(self.userInput.id)
            self.addChildElement(hiddenValue)

    def setId(self, value):
        """
            Sets the id of the userInput
        """
        self.userInput.setId(value)

    def setName(self, value):
        """
            Sets the name of the userInput
        """
        self.userInput.setName(value)

    def selectJs(self):
        '''
        Returns the javascript to select this option clientside.
        The element's id must be set.
        '''
        return "document.getElementById('%s').checked=true;" % self.userInput.id

Factory.addProduct(RadioField)


class TextAreaField(BaseField):
    """
        A field with a textarea as the input
    """
    __slots__ = ()
    inputElement = Inputs.TextArea
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.TextArea, 'userInput')

Factory.addProduct(TextAreaField)


class AutoField(Layout.Vertical):
    """
        Allows you to use any input element as a field (text label, inputElement, validator pair)
        simply by adding it as a childElement
    """
    __slots__ = ('inputContainer', 'fieldActions', 'userInput', 'formError', 'label')
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['setApart'] = {'action':'call', 'type':'bool'}
    properties['value'] = {'action':'setValue'}

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Vertical._create(self, id, name, parent=parent)

        self.inputContainer = self.addChildElement(Layout.Horizontal())

        self.label = self.inputContainer.addChildElement(Display.Label())
        self.fieldActions = self.inputContainer.addChildElement(Layout.Box())
        self.addChildElementsTo = self.fieldActions
        self.userInput = self.inputContainer.addChildElement(Base.Invalid())

        errorContainer = self.addChildElement(Layout.Horizontal())
        self.formError = errorContainer.addChildElement(Display.FormError(id, parent=self))

    def exportVariables(self, exportedVariables=None, flat=False):
        if not self.userInput.key and self.key:
            self.userInput.key = self.key
            self.key = None

        Layout.Vertical.exportVariables(self, exportedVariables, flat)

    def setValue(self, value):
        """
            Sets the input elements value
        """
        self.userInput.setValue(value)

    def value(self):
        """
            Returns the input elements value
        """
        return self.userInput.value()

    def setText(self, text):
        """
            Sets the text displayed on the fields label
        """
        self.label.setText(text)

    def text(self):
        """
            Returns the text that will be displayed on the fields label
        """
        return self.label.text()

    def setApart(self):
        """
            Moves the input as far right (away from the label) as possible
        """
        self.inputContainer.style['float'] = 'right'

    def setInputElement(self, element):
        """
            Sets the input element for the field
        """
        self.userInput = self.userInput.replaceWith(element)
        self.formError.name = self.userInput.name or self.userInput.id
        return self.userInput

    def addChildElement(self, childElement, style=None):
        if (isinstance(childElement, Inputs.ValueElement) or hasattr(childElement, 'userInput')) and type(self.userInput) == Base.Invalid:
            return self.setInputElement(childElement)
        else:
            return Layout.Vertical.addChildElement(self, childElement, style)


Factory.addProduct(AutoField)


class SelectField(BaseField):
    """
        A field with a select box as the input
    """
    __slots__ = ()
    inputElement = Inputs.Select
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.Select, 'userInput')

    def _create(self, id, name=None, parent=None, **kwargs):
        self.fieldActions = None
        BaseField._create(self, id, name, parent, **kwargs)
        self.addChildElementsTo = self

    def addChildElement(self, childElement):
        if isinstance(childElement, Inputs.Option):
            return self.userInput.addChildElement(childElement)
        elif self.fieldActions:
            return self.fieldActions.addChildElement(childElement)
        return BaseField.addChildElement(self, childElement)

    def addOptions(self, dictionary, displayKeys=False):
        """
            Adds options to the fields select box where the options are passed in as a dictionary of id-value pairs.
        """
        return self.userInput.addOptions(dictionary, displayKeys)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds options to the fields select box where the options are passed in as a list of tuples of id-value pairs.
        """
        return self.userInput.addOptionList(options, displayKeys=displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds a single option the fields select box, based on key/value
        """
        return self.userInput.addOption(key, value=value, displayKeys=displayKeys)

    def options(self):
        """
            Returns a list of available options associated with the fields select box
        """
        return self.userInput.options()

    def selected(self):
        """
            Returns all selected options
        """
        return self.userInput.selected()

Factory.addProduct(SelectField)

@ToClientSide.Convert
class MultiFieldClientSide(object):

    def removeSelectedOption(self, button, sortBy):
        selectionBox = WebElements.fellowChild(button, 'multiField', 'selectionBox')
        hiddenMultiSelect = WebElements.fellowChild(button, 'multiField', 'hiddenMultiSelectionField')
        shownOption = WebElements.getByClassName('valueSelected', button.parent())
        hiddenOption = WebElements.getByInnerHTML(hiddenMultiSelect, shownOption.innerHTML)
        WebElements.addOption(selectionBox, hiddenOption.innerHTML, hiddenOption.value)
        WebElements.removeElement(button.parentNode)
        WebElements.removeElement(hiddenOption)
        if sortBy == "innerHTML":
            WebElements.sortSelect(selectionBox)
        elif sortBy == "value":
            WebElements.sortSelect(selectionBox, True)

    def addSelectedOption(self, selectBox):
        shownSelection = WebElements.fellowChild(selectBox, 'multiField', 'selectContainer')
        hiddenMultiSelect = WebElements.fellowChild(selectBox, 'multiField', 'hiddenMultiSelectionField')
        selected = WebElements.selectedOption(selectBox)
        shownSelection.innerHTML += WebElements.unserialize('%s')
        WebElements.addOption(hiddenMultiSelect, selected.innerHTML, selected.value)
        WebElements.selectOption(selectBox, ' ')
        WebElements.removeElement(selected)
        WebElements.selectAllOptions(hiddenMultiSelect)

class MultiField(SelectField):
    """
        The multifield is a multi select field, where each individual option is selected in the same mannor
        as a normal select field to make it more intuitive for users
    """
    __slots__ = ('sortBy', 'selectContainer', 'hiddenMultiSelect')
    properties = SelectField.properties.copy()
    properties['validator'] = {'action': 'hiddenMultiSelect.classAttribute', 'name': 'validator'}
    properties['sortBy'] = {'action': 'classAttribute'}

    def __createNewSelection__(self, name):
        new = Layout.Horizontal()
        new.addClass('WSelectedMultiOption')
        label = new.addChildElement(Display.Label())
        label.setText(name)
        label.style['overflow'] = 'hidden'
        label.attributes['title'] = name
        label.addClass('valueSelected')
        remove = new.addChildElement(Buttons.Button())
        remove.setText("Remove")
        remove.name = "MultiFieldRemove" + name
        remove.addJavascriptEvent('onclick', 'multiField.removeSelectedOption(this, "%s");' % self.sortBy)

        return new

    def _create(self, id, name=None, parent=None, **kwargs):
        SelectField._create(self, id, name, parent, **kwargs)
        self.sortBy = "innerHTML"
        self.userInput.id = id + "MultiField"
        self.userInput.name = (name or id) + "MultiField"

        self.selectContainer = self.addChildElement(Layout.Vertical())
        self.hiddenMultiSelect = self.addChildElement(Inputs.MultiSelect(id))
        self.hiddenMultiSelect.hide()
        self.hiddenMultiSelect.addClass('hiddenMultiSelectionField')
        self.selectContainer.addClass('selectContainer')
        self.userInput.addClass('selectionBox')
        self.userInput.addOption(' Click to add', ' ')
        self.addClass('multiField')

        self.userInput.addClientSideEvent('onChange', 'multiField.addSelectedOption(this)')

    def _render(self):
        SelectField._render(self)
        self.sort()

    def sort(self):
        """
            Sorts the options list based on the key value
        """
        self.userInput.childElements.sort(key=Inputs.Option.value)

    def setProperties(self, valueDict):
        SelectField.setProperties(self, valueDict)

        new = self.__createNewSelection__("' + selected.innerHTML + '")
        self.addScript(str(MultiFieldClientSide) % listReplace(new.toHTML(), ('"', '<', '>'), ('\\"', '&lt;', '&gt;')))
        self.runClientSide("multiField = MultiFieldClientSide()")

    def insertVariables(self, valueDict=None):
        """
            Overrides the insertVariable call to create the new selection objects and populate the hidden multiselect
        """
        if valueDict is None: valueDict = {}
        selectedOptions = valueDict.pop(self.hiddenMultiSelect.id, [])
        if type(selectedOptions) != list:
            selectedOptions = [selectedOptions]

        for option in selectedOptions:
            optionObject = self.userInput.query().filter(_value=option)[0]
            optionObject.select()
            self.hiddenMultiSelect.addChildElement(optionObject)
            self.selectContainer.addChildElement(self.__createNewSelection__(optionObject.text()))

        return SelectField.insertVariables(self, valueDict)

Factory.addProduct(MultiField)

class MultiSelectField(BaseField):
    """
        A field with a multiselect as the input
    """
    __slots__ = ()
    inputElement = Inputs.MultiSelect
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.MultiSelect, 'userInput')

    def _create(self, id, name=None, parent=None, **kwargs):
        self.fieldActions = None
        BaseField._create(self, id, name, parent, **kwargs)
        self.addChildElementsTo = self
        self.userInput.attributes['multiple'] = True

    def addChildElement(self, childElement):
        if isinstance(childElement, Inputs.Option):
            return self.userInput.addChildElement(childElement)
        elif self.fieldActions:
            return self.fieldActions.addChildElement(childElement)
        return BaseField.addChildElement(self, childElement)

    def addOptions(self, dictionary, displayKeys=False):
        """
            Adds options to the fields select box where the options are passed in as a dictionary of id-value pairs.
        """
        return self.userInput.addOptions(dictionary, displayKeys)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds options to the fields select box where the options are passed in as a list of tuples of id-value pairs.
        """
        return self.userInput.addOptionList(options, displayKeys=displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds a single option the fields select box, based on key/value
        """
        return self.userInput.addOption(key, value=value, displayKeys=displayKeys)

    def options(self):
        """
            Returns a list of available options associated with the fields select box
        """
        return self.userInput.options()

    def selected(self):
        """
            Returns all selected options
        """
        return self.userInput.selected()

Factory.addProduct(MultiSelectField)

class CheckboxField(BaseField):
    """
        A field with a checkbox as the input
    """
    __slots__ = ('labelContainer', 'childContainer')
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.CheckBox, 'userInput')
    properties['checked'] = {'action':'setValue', 'type':'bool'}
    inputElement = Inputs.CheckBox

    def _create(self, id, name=None, parent=None, **kwargs):
        BaseField._create(self, id, name, parent, **kwargs)

        inputContainer = Layout.Box(id + "_inputContainer", '', self)
        inputContainer.style['float'] = 'left'
        inputContainer.style['clear'] = 'none'
        userInput = Inputs.CheckBox(id, None, self)
        self.userInput.addJavascriptEvent('onload', 'CCClickCheckbox(this)')
        self.userInput.addJavascriptEvent('onclick', CallBack(self, 'toggleChildren'))
        self.userInput = self.userInput.replaceWith(userInput)
        self.inputContainer = self.addChildElement(inputContainer)

        labelContainer = Layout.Box(id + "_labelContainer", '', self)
        labelContainer.style['float'] = 'left'
        labelContainer.style['clear'] = 'none'
        labelContainer.style['margin-top'] = "3px"
        label = Display.Label(id + "_label", '' , self)
        self.label = labelContainer.addChildElement(label)
        self.labelContainer = self.addChildElement(labelContainer)

        self.addChildElement(Layout.LineBreak())

        childContainer = Layout.Box(id + "_childContainer", name, self)
        childContainer.style['display'] = CallBack(self, 'displayValue')
        self.childContainer = self.addChildElement(childContainer)
        self.addChildElementsTo = childContainer

    def __updateReadOnly__(self):
        # Only create the hidden input if the original checkbox is checked to simulate
        # how an actual checkbox control would work
        if not self.editable() and self.submitIfDisabled and self.value():
            hiddenValue = HiddenInputs.HiddenValue(name=self.name)
            hiddenValue.setValue('on')
            self.addChildElement(hiddenValue)

    def setProperties(self, valueDict):
        BaseField.setProperties(self, valueDict)
        if self.key:
            self.userInput.key = self.key
            self.key = None

    def setValue(self, value):
        """
            Sets the value on the checkbox
        """
        self.userInput.setValue(value)

    def displayValue(self):
        """
            Returns the css display value for the checkbox field children
        """
        if not self.userInput.value():
            return 'none'

        return 'block'

    def toggleChildren(self):
        """
            Returns javascript that will toggle the visibility of the checkbox field child elements clientside
        """
        javascript = "WebElements.toggleVisibility('" + self.childContainer.fullId() + "');"
        return javascript

    def validators(self, useFullId=True):
        # Only use the validators contained in the
        # childElements when the checkbox is clicked
        if not self.userInput.value():
            return {}

        return BaseField.validators(self, useFullId)

    def exportVariables(self, exportedVariables=None, flat=False):
        if exportedVariables is None: exportedVariables = {}

        # Only export child values when thet checkbox is clicked
        if not self.userInput.value():
            self.userInput.exportVariables(exportedVariables, flat)
        else:
            BaseField.exportVariables(self, exportedVariables, flat)

        return exportedVariables

Factory.addProduct(CheckboxField)

class IntegerField(BaseField):
    """
        A field with a incremntable and deincrementable textfield (with up and down arrows) as the input
    """
    __slots__ = ('toggleLayout', 'up', 'down')
    inputElement = Inputs.IntegerTextBox
    properties = TextField.properties.copy()
    Base.addChildProperties(properties, Inputs.IntegerTextBox, 'userInput')

    def _create(self, id, name, parent, **kwargs):
        BaseField._create(self, id, name=None, parent=None, **kwargs)

        self.toggleLayout = self.addChildElement(Layout.Vertical())
        self.toggleLayout.style["font-size"] = "75%"
        self.toggleLayout.addClass("Clickable")

        self.label.style['display'] = "block"
        self.label.style['margin-top'] = "5px;"
        self.up = self.toggleLayout.addChildElement(Buttons.UpButton())
        self.up.addClass("hidePrint")
        self.down = self.toggleLayout.addChildElement(Buttons.DownButton(src='images/count_down.png'))
        self.down.addClass("hidePrint")
        self.userInput.setValue(0)

    def _render(self):
        BaseField._render(self)
        self.__addEvents__()
        self.__updateReadOnly__()

    def __addEvents__(self):
        minimum = self.userInput.minimum
        if minimum is None:
            minimum = "undefined"
        maximum = self.userInput.maximum
        if maximum is None:
            maximum = "undefined"
        self.up.addJavascriptEvent('onclick', "WebElements.increment('%s', %s);" %
                                 (self.userInput.fullId(), str(maximum)))
        self.down.addJavascriptEvent('onclick', "WebElements.deincrement('%s', %s);" %
                                 (self.userInput.fullId(), str(minimum)))

    def __updateReadOnly__(self):
        if not self.editable():
            self.toggleLayout.remove()

Factory.addProduct(IntegerField)


class DateField(TextField):
    """
        A field with a date widget as the input (which provides a browseable way to select the date)
    """
    __slots__ = ('userInput', 'dateFormat', 'calendarLink', 'calendarTypeLabel', 'formatDisplay', 'isZulu')
    properties = TextField.properties.copy()
    Base.addChildProperties(properties, Display.Label, 'calendarTypeLabel')
    properties['isZulu'] = {'action':'setIsZulu', 'type':'bool'}
    properties['hideTypeLabel'] = {'action':'formatDisplay.call', 'name':'hide', 'type':'bool'}
    properties['dateFormat'] = {'action':'classAttribute'}

    def _create(self, id, name=None, parent=None, **kwargs):
        TextField._create(self, id, name, parent, **kwargs)
        self.userInput.style['width'] = '7.5em'
        self.dateFormat = "dd-mmm-yyyy"

        layout = self.addChildElement(Layout.Horizontal())
        layout.addClass("FieldDescription")
        self.calendarLink = layout.addChildElement(Display.Image(id + "CalendarLink",
                                                                 src='images/calendar_icon.gif'))
        self.calendarLink.addClass('Clickable')
        self.calendarLink.addClass('hidePrint')
        self.calendarLink.addJavascriptEvent('onclick', CallBack(self, "jsOpenCalendar"))

        self.calendarTypeLabel = layout.addChildElement(Display.Label())
        self.calendarTypeLabel.style['margin-left'] = "4px;"
        self.calendarTypeLabel.style['margin-right'] = "4px;"
        self.calendarTypeLabel.style['display'] = "block;"

        self.setIsZulu(False)
        self.formatDisplay = layout.addChildElement(Display.Label())

    def setIsZulu(self, isZulu):
        """
            If set to true the calender will use the zulu date
        """
        self.isZulu = isZulu
        if isZulu:
            self.calendarTypeLabel.setText("Z")
        else:
            self.calendarTypeLabel.setText("LCL")

    def _render(self):
        TextField._render(self)
        if not self.editable():
            self.calendarLink.hide()
        self.formatDisplay.setText(self.dateFormat)

    def jsOpenCalendar(self):
        """
            Returns the javascript that will open the calender clientside
        """
        if self.isZulu:
            calendarType = "zulu"
        else:
            calendarType = "lcl"

        return ("%sCalendar.popUpCalendar(this, WebElements.get('%s'), '%s')" %
                (calendarType, self.userInput.fullId(), self.dateFormat))

Factory.addProduct(DateField)


class NestedSelect(SelectField):
    """
        Defines two select boxes where the selection of an item from the first will trigger
        the population of the second.
    """
    __slots__ = ('itemSelect', 'items')
    properties = SelectField.properties.copy()
    properties['groupData'] = {'action':'setGroupData'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        SelectField._create(self, id, name, parent, **kwargs)

        self.userInput.addJavascriptEvent('onclick', CallBack(self, "jsPopulateItemSelect"))
        self.userInput.connect('selectionChanged', None, self, 'updateItems')

        self.itemSelect = self.addChildElement(Inputs.Select(id + "Items"))
        self.items = None

    def updateItems(self):
        """
            Updates the items select Layout.Box to load the items contained in the currently
            selected group.
        """
        selected = self.userInput.selected()
        if selected:
            for item in self.items[selected.value()]:
                self.itemSelect.addOption(item)

    def setGroupData(self, data):
        """
            Sets the groups and the items each group should contain
                data - a collection of name to value tuples - for example:
                    (('fruits',('apple', 'orange', 'grape')), )
        """
        self.userInput.reset()
        self.itemSelect.reset()
        self.items = dict(data)
        for newGroup, items in data:
            self.userInput.addOption(newGroup, newGroup)

        self.addScript(CallBack(self, "jsGroups"))
        self.addScript(CallBack(self, "jsPopulateItemSelect"))

    def jsGroups(self):
        """
            Creates the group structure client side
        """
        if self.items:
            return """document.%(groupId)s = %(groups)s;
                    document.%(itemId)s = %(items)s;
                """ % {'items':json.dumps(self.items), 'groups':json.dumps(list(self.items.keys())),
                       'id':self.fullId(), 'itemId':self.itemSelect.fullId(), 'groupId':self.userInput.fullId()}

    def jsPopulateItemSelect(self):
        """
            Populates the item select Layout.Box with the items contained in the selected group
        """
        return """WebElements.setOptions('%(itemSelectId)s',
                     document.%(itemSelectId)s[WebElements.getValue('%(groupSelectId)s')]);
               """ % {'itemSelectId':self.itemSelect.fullId(),
                      'groupSelectId':self.userInput.fullId()}

Factory.addProduct(NestedSelect)


class Filter(Layout.Box):
    """
        Defines a dynamic and expandable list of filters
    """
    __slots__ = ('searchFieldList', 'filters', 'isSubFilter', 'filterContainer', 'searchTerm', 'searchFields',
                 'filterType', 'removeButton', 'addAndFilter', 'addOrFilter', 'addFilter', 'subFilter')

    jsFunctions = ["javascriptAddFilter", "javascriptRemoveFilter"]

    def _create(self, id, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id, name, parent, **kwargs)

        self.searchFieldList = []
        self.filters = [self, ]
        self.isSubFilter = False

        filterContainer = Layout.Box(id + ":Container")
        filterContainer.addClass('WFilter')
        self.filterContainer = self.addChildElement(filterContainer)

        filterInput = Layout.Box()
        filterInput.style['float'] = 'left'
        filterContainer.addChildElement(filterInput)

        label = Display.Label('filterTermLabel')
        label.setText('Search for:')
        filterInput.addChildElement(label)

        searchTerm = Inputs.TextBox(id + ":SearchTerm", "FilterTerm")
        searchTerm.addClass("WFilterTerm")
        self.searchTerm = filterInput.addChildElement(searchTerm)

        label = Display.Label('filterFieldLabel')
        label.setText('in:')
        filterInput.addChildElement(label)

        searchFields = Inputs.Select(id + ":SearchFields", "FilterField")
        searchFields.addClass("WFilterField")
        self.searchFields = filterInput.addChildElement(searchFields)

        filterType = Inputs.TextBox(id + ":FilterType", "FilterType")
        filterType.addClass('filterType')
        filterType.attributes['type'] = "hidden"
        filterType.setValue("BaseFilter")
        self.filterType = filterInput.addChildElement(filterType)

        removeButton = Buttons.Link(id + ":Remove")
        removeButton.style['float'] = 'right'
        removeButton.style['display'] = 'none'
        removeButton.setText("")
        removeButton.addChildElement(DOM.Img()).setProperty("src", "images//close.gif")
        removeButton.addClass('Clickable')
        removeButton.addClass('WRemoveFilter')
        removeButton.addJavascriptEvent("onclick", CallBack(self, 'jsRemoveFilter'))
        removeButton.addJavascriptEvent("onmouseover",
                                        """WebElements.addClass(WebElements.parent(this,
                                                                      'WFilter'),
                                                        'WFilterHighlight');""")
        removeButton.addJavascriptEvent("onmouseout",
                                        """WebElements.removeClass(WebElements.parent(this,
                                                                      'WFilter'),
                                                        'WFilterHighlight');""")
        self.removeButton = filterContainer.addChildElement(removeButton)

        addFilter = Layout.Box()
        addFilter.addClass('WAddFilter')
        addFilter.style['clear'] = 'both'
        addAndFilter = Buttons.ToggleButton(id + ":And")
        addAndFilter.button.addClass('WAddFilterButton')
        addAndFilter.button.addClass('WAddAndFilter')
        addAndFilter.setValue("And")
        self.addAndFilter = addFilter.addChildElement(addAndFilter)
        addOrFilter = Buttons.ToggleButton(id + ":Or")
        addOrFilter.button.addClass('WAddFilterButton')
        addOrFilter.button.addClass('WAddOrFilter')
        addOrFilter.setValue("Or")
        self.addOrFilter = addFilter.addChildElement(addOrFilter)
        self.addFilter = filterContainer.addChildElement(addFilter)

        subFilter = Layout.Box()
        subFilter.addClass('subFilter')
        self.subFilter = self.addChildElement(subFilter)

        addOrFilter.connect('toggled', True, addAndFilter, 'toggleOff')
        addOrFilter.connect('jsToggled', None, self, 'jsAddOrFilter')
        addOrFilter.connect('jsToggled', True, addAndFilter, 'jsToggleOff')

        addAndFilter.connect('toggled', True, addOrFilter, 'toggleOff')
        addAndFilter.connect('jsToggled', None, self, 'jsAddAndFilter')
        addAndFilter.connect('jsToggled', True, addOrFilter, 'jsToggleOff')

        self.addJSFunctions(self.__class__)

    def jsAddAndFilter(self, toggledOn):
        """
            Return the javascript to add an And filter to the filter list clientside
        """
        return self.jsAddFilter("And", toggledOn)

    def jsAddOrFilter(self, toggledOn):
        """
            Return the javascript to add an Or filter to the filter list clientside
        """
        return self.jsAddFilter("Or", toggledOn)

    def jsAddFilter(self, filterType, toggledOn):
        """
            Return the javascript to add a filter to the filter list clientside
        """
        return "javascriptAddFilter(this, '" + filterType + "', " + \
                                    interpretAsString(toggledOn) + ");"

    def jsRemoveFilter(self):
        """
            Return the javascript to remove a filter to the filter list clientside
        """
        return "javascriptRemoveFilter(this);"

    @staticmethod
    def javascriptAddFilter(element, filterType, toggledOn):
        return """
            if(toggledOn){
                parentFilter = WebElements.parent(element, 'WFilter');
                filter = WebElements.getByClassName('WFilter', parentFilter);
                if(!filter){
                    filter = WebElements.copy(parentFilter,
                                    WebElements.getByClassName('subFilter',
                                                            parentFilter));
                    oldTerm = WebElements.getByClassName('WFilterTerm',
                                                        parentFilter);
                    newTerm = WebElements.getByClassName('WFilterTerm', filter);
                    newTerm.value = oldTerm.value;
                    newTerm.focus();
                    newTerm.select();
                    WebElements.getByClassName('RemoveFilter', filter).style.display = 'block';
                }
                WebElements.getByClassName('filterType', filter).value = filterType;
            }
            else{
                WebElements.removeElement(WebElements.getByClassName('WFilter',
                                        WebElements.parent(element, 'WFilter')));
            }"""

    @staticmethod
    def javascriptRemoveFilter(element):
        return """
                thisFilter = WebElements.parent(element, 'WFilter');
                childFilter = WebElements.getByClassName('WFilter', thisFilter);
                filterType = WebElements.getByClassName('filterType',
                                                     childFilter).value;

                AndButton = WebElements.getByClassName('WAddAndFilter', thisFilter);
                OrButton = WebElements.getByClassName('WAddOrFilter', thisFilter);
                parentFilter = WebElements.parent(thisFilter, 'WFilter');

                parentAndButton = WebElements.getByClassName('WAddAndFilter',
                                                          parentFilter);
                parentOrButton = WebElements.getByClassName('WAddOrFilter',
                                                         parentFilter);

                parentOrButton.className = OrButton.className;
                parentAndButton.className = AndButton.className;

                if(filterType == 'Or'){
                    WebElements.next(parentOrButton).value = 'on';
                    WebElements.next(parentAndButton).value = 'off';
                }
                else if(filterType == 'And'){
                    WebElements.next(parentAndButton).value = 'on';
                    WebElements.next(parentOrButton).value = 'off';
                }
                else{
                    WebElements.next(parentAndButton).value = 'off';
                    WebElements.next(parentOrButton).value = 'off';
                }

                if(childFilter)
                {
                    WebElements.move(childFilter,
                        WebElements.getByClassName('subFilter', parentFilter));
                }
                WebElements.removeElement(thisFilter);
               """

    def addSearchField(self, searchField):
        """
            Adds a search field (a filter) for rendering
        """
        field = Inputs.Option("field:" + searchField)
        field.setText(searchField)
        field.setValue(searchField)
        self.searchFieldList.append(searchField)
        self.searchFields.addChildElement(field)

    def insertVariables(self, valueDict=None):
        if valueDict is None: valueDict = {}

        if self.isSubFilter:
            return Layout.Box.insertVariables(self, valueDict)

        searchTerms = valueDict.get(self.searchTerm.name, '')
        if type(searchTerms) == list:
            currentFilter = self
            for index in xrange(1, len(searchTerms)):
                newFilter = Filter(self.id + unicode(index))
                newFilter.searchFields.addOptions(self.searchFields.options())
                newFilter.removeButton.style['display'] = 'block'
                newFilter.isSubFilter = True
                self.filters.append(newFilter)

                currentFilter = currentFilter.subFilter.addChildElement(newFilter)

        Layout.Box.insertVariables(self, valueDict)

    def filterList(self, valueDict=None):
        """
            Returns the set list of filters
        """
        filterList = []
        for filter in self.filters:
            if filter.searchTerm.value():
                filterList.append({'term':filter.searchTerm.value(),
                                   'field':filter.searchFields.value(),
                                   'type':filter.filterType.value()})

        return filterList

Factory.addProduct(Filter)
