"""
    Validators.py

    Contains elements that validate data both server-side and client-side for a unique all-in-one solution

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
"""

import re
import string

from . import Factory
from . import Base
from . import Display
from . import ClientSide
from .ClientSide import do, regexp, var, Script
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("Validators")

class Validation(Display.Message):
    """
        Processes child validators to render validation results
    """
    __slots__ = ('_lastScript')

    class ClientSide(Display.Message.ClientSide):
        """
            Defines the client-side behavior of a the validation controller.
        """

        def validate(self):
            """
                Specifies how a validation should be handled client-side.
            """
            stack = self.assign('value', self.serverSide.forElement.clientSide.value())
            stack(self.hide())
            for validator in self.serverSide:
                if isinstance(validator, Validator):
                    if not validator.required:
                        with self.value.IF.exists as condition:
                            condition(validator.clientSide.validate())
                        stack(condition)
                    else:
                        stack = stack(validator.clientSide.validate())

            stack = self.assign('result', stack.inlineFunction().do())
            with self.result.IF.exists as context:
                context(self.showMessage(self.result[0], self.result[1]))
                context(self.show())

            return stack(context)

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Display.Message._create(self, id=id, name=name, parent=parent, **kwargs)
        self._lastScript = None

    def _render(self):
        Display.Message._render(self)
        if not self.forElement or not [match for match in self if isinstance(match, Validator)]:
            return

        if self._lastScript:
            self.removeScript(self._lastScript)
        self._lastScript = self.forElement.clientSide.on(self.forElement.ClientSide.CHANGE_EVENT,
                                                         self.clientSide.validate())

    def value(self):
        """
            Returns the value that all validators should validate
        """
        return self.forElement.value()

    def addChildElement(self, childElement, ensureUnique=True):
        """
            Adds the validation control to all child elements
        """
        if isinstance(childElement, Validator):
            childElement.control = self
        return Display.Message.addChildElement(self, childElement, ensureUnique)

    def validate(self):
        """
            Defines how validation should be handled.
        """
        self.hide()
        for validator in (element for element in self if isinstance(element, Validator)):
            if validator.required or self.forElement.value():
                message = validator.validate()
                if message:
                    self.showMessage(*message)
                    self.show()
                    break


class Validator(Base.WebElement):
    """
        The base abstract validator that should be sub-classed to define new validators
    """
    __slots__ = ('control', 'required')
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    messages = {'empty':'A value is required for this field'}
    properties = Base.WebElement.properties.copy()
    properties['required'] = {'action':'classAttribute'}

    class ClientSide(Display.Message.ClientSide):

        def validate(self):
            """
                Stub method for validating client-side, child classes should implement.
            """
            pass

        def message(self, message):
            """
                Expands and returns a message based on a message key.
            """
            return self.expandTemplate(self.serverSide.messages[message], self.associatedData())

        def error(self, message):
            """
                Returns a client-side error message.
            """
            return (ClientSide.MessageTypes.ERROR, self.message(message))

        def info(self, message):
            """
                Returns a client-side info message.
            """
            return (ClientSide.MessageTypes.INFO, self.message(message))

        def warning(self, message):
            """
                Returns a client-side warning message.
            """
            return (ClientSide.MessageTypes.WARNING, self.message(message))

        def success(self, message):
            """
                Returns a client-side success message.
            """
            return (ClientSide.MessageTypes.SUCCESS, self.message(message))

        def associatedData(self):
            """
                Returns the client-side data associated with this validator.
            """
            return {'field':self.value}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.WebElement._create(self, id=id, name=name, parent=parent, **kwargs)
        self.required = False
        self.control = None

    def validate(self):
        """
            Defines the validator action server side, should be implemented by sub-classes.
        """
        pass

    def error(self, message):
        """
            Returns an error message.
        """
        return (ClientSide.MessageTypes.ERROR, self.message(message))

    def info(self, message):
        """
            Returns an info message.
        """
        return (ClientSide.MessageTypes.INFO, self.message(message))

    def warning(self, message):
        """
            Returns an warning message.
        """
        return (ClientSide.MessageTypes.WARNING, self.message(message))

    def success(self, message):
        """
            Returns a success message.
        """
        return (ClientSide.MessageTypes.SUCCESS, self.message(message))

    def associatedData(self):
        """
            Defines a dictionary of data that can be used to populate messages
        """
        return {'field':self.value()}

    def message(self, message):
        """
            Expands and returns a message based on a message key
        """
        return string.Template(self.messages[message]).safe_substitute(self.associatedData())

    def value(self):
        """
            Returns the value that this validator is validating
        """
        return self.control.value()

    @property
    def forElement(self):
        """
            Returns the element associated with the validator.
        """
        return self.control and self.control.forElement


class Or(Validator):
    """
        Defines a validator that will pass when any of the child validators pass.
    """
    def _render(self):
        Validator._render(self)
        for element in self:
            element.control = self.control

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Validator._create(self, id=id, name=name, parent=parent, **kwargs)
        self.required = True

    def addChildElement(self, element):
        element.control = self.control
        return Validator.addChildElement(self, element)

    class ClientSide(Validator.ClientSide):
        def validate(self):
            stack = self.assign('messageResult', None)
            for validator in self.serverSide:
                if not validator.required:
                    with self.value.IF.exists as condition:
                        condition(validator.clientSide.validate())
                    stack(self.assign('result', condition.inlineFunction().do()))
                else:
                    stack(self.assign('result', validator.clientSide.validate().inlineFunction().do()))

                with self.result.IF.notExists as condition:
                    condition(Script("return;"))
                stack(condition)

                stack(self.assign('messageResult', self.result))
            return stack.RETURN(self.messageResult)

    def validate(self):
        for element in self:
            element.control = self
        return self.validateAll()

    def validateAll(self):
        message = None
        for validator in self:
            result = validator.validate()
            if not result:
                return
            message = message or result
        return message

Factory.addProduct(Or)


class And(Or):
    """
        Defines a validator that will only pass when all the child validators pass.
    """
    class ClientSide(Validator.ClientSide):
        def validate(self):
            stack = Script("")
            for validator in self.serverSide:
                stack(validator.clientSide.validate())
            return stack

    def validateAll(self):
        for validator in self:
            result = validator.validate()
            if result:
                return result

Factory.addProduct(And)


class NotEmpty(Validator):
    """
        Defines a validator that will pass if any value is supplied.
    """
    messages = {'notEmpty':'Please enter a value'}
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Validator._create(self, id=id, name=name, parent=parent, **kwargs)
        self.required = True

    class ClientSide(Validator.ClientSide):
        def validate(self):
            with self.value.IF == "" as context:
                context(self.error('notEmpty').RETURN())
            return context

    def validate(self):
        if not self.forElement.value():
            return self.error("notEmpty")

Factory.addProduct(NotEmpty)


class Int(Validator):
    """
        Defines a validator that will pass if a whole number is supplied.
    """
    messages = {'notInt':'Please enter an integer value'}
    __slots__ = ()

    class ClientSide(Validator.ClientSide):
        def validate(self):
            with self.value.IF != do.parseInt(self.value, 10) as context:
                context(self.error('notInt').RETURN())
            return context

    def validate(self):
        try:
            self.forElement.setValue(int(self.forElement.value()))
        except ValueError:
            return self.error("notInt")

Factory.addProduct(Int)


class PatternValidator(Validator):
    """
        Base class for validating a field against a regular expression
    """
    pattern = r''
    messages = {'format':'Please enter a value using the specified format'}
    __slots__ = ()

    class ClientSide(Validator.ClientSide):
        def validate(self):
            with regexp(self.serverSide.pattern).do('test', self.value).IF != True as context:
                context(self.error("format").RETURN())
            return context

    def validate(self):
        if not self.pattern.match(self.forElement.value()):
            return self.error("format")


class Email(PatternValidator):
    """
        Validates that an email matches a specified format
    """
    pattern = re.compile('''[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:[\.a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*''' \
                         '''[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])+''')
    messages = {'format':'Please enter an email in the form: email@domain.tld'}
    __slots__ = ()

Factory.addProduct(Email)


class PhoneNumber(PatternValidator):
    """
        Validates that a phone number is defined with a valid format
    """
    pattern = re.compile(r'^\s*(?:1-)?(\d\d\d)[\- \.]?(\d\d\d)[\- \.]?(\d\d\d\d)(?:\s*ext\.?\s*(\d+))?\s*$', re.I)
    messages = {'format':'Please enter a number, with area code, in the form ###-###-####, optionally with "ext.####"'}
    __slots__ = ()

Factory.addProduct(PhoneNumber)


