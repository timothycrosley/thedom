"""
    Contains basic web validators - that validate both ClientSide and server side.
"""

import re
import string

import Factory
import Base
import Display
import Layout
import ClientSide
from ClientSide import do, regexp, var, Script
from MethodUtils import CallBack

Factory = Factory.Factory("Validators")

class Validation(Display.Message):
    """
        Processes child validators to render validation results
    """
    __slots__ = ('_lastScript')

    class ClientSide(Display.Message.ClientSide):

        def validate(self):
            stack = self.assign('value', self.serverSide.userInput.clientSide.value())
            stack(self.hide())
            for validator in self.serverSide:
                if isinstance(validator, Validator):
                    stack = stack(validator.clientSide.validate())

            stack = self.assign('result', stack.inlineFunction().do())
            with self.result.IF.exists as context:
                context(self.showMessage(self.result[0], self.result[1]))
                context(self.show())

            return stack(context)

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Display.Message.__init__(self, id=id, name=name, parent=parent, **kwargs)
        self._lastScript = None

    @property
    def userInput(self):
        return self.forElement

    @userInput.setter
    def userInput(self, userInput):
        if self._lastScript:
            self.removeScript(self._lastScript)

        self.forElement = userInput
        self._lastScript = userInput.clientSide.on(userInput.ClientSide.CHANGE_EVENT, self.clientSide.validate())

    def value(self):
        """
            Returns the value that all validators should validate
        """
        return self.userInput.value()

    def addChildElement(self, childElement, ensureUnique=True):
        """
            Adds the validation control to all child elements
        """
        if isinstance(childElement, Validator):
            childElement.control = self
        return Display.Message.addChildElement(self, childElement, ensureUnique)

    def validate(self):
        self.hide()
        for validator in (element for element in self if isinstance(element, Validator)):
            message = validator.validate()
            if message:
                self.showMessage(*message)
                self.show()
                break


class Validator(Base.WebElement):
    """
        The base abstract validator that should be sub-classed to define new validators
    """
    __slots__ = ('control', )
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    messages = {'empty':'A value is required for this field'}

    class ClientSide(Display.Message.ClientSide):

        def validate(self):
            pass

        def message(self, message):
            """
                Expands and returns a message based on a message key
            """
            return self.expandTemplate(self.serverSide.messages[message], self.associatedData())

        def error(self, message):
            return (ClientSide.MessageTypes.ERROR, self.message(message))

        def info(self, message):
            return (ClientSide.MessageTypes.INFO, self.message(message))

        def warning(self, message):
            return (ClientSide.MessageTypes.WARNING, self.message(message))

        def success(self, message):
            return (ClientSide.MessageTypes.SUCCESS, self.message(message))

        def associatedData(self):
            return {'field':self.value}

    def validate(self):
        pass

    def error(self, message):
        return (ClientSide.MessageTypes.ERROR, self.message(message))

    def info(self, message):
        return (ClientSide.MessageTypes.INFO, self.message(message))

    def warning(self, message):
        return (ClientSide.MessageTypes.WARNING, self.message(message))

    def success(self, message):
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


class NotEmpty(Validator):
    messages = {'notEmpty':'Please enter a value'}

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
    messages = {'notInt':'Please enter an integer value'}

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

Factory.addProduct(Email)


class PhoneNumber(PatternValidator):
    """
        Validates that a phone number is defined with a valid format
    """
    pattern = re.compile(r'^\s*(?:1-)?(\d\d\d)[\- \.]?(\d\d\d)[\- \.]?(\d\d\d\d)(?:\s*ext\.?\s*(\d+))?\s*$', re.I)
    messages = {'format':'Please enter a number, with area code, in the form ###-###-####, optionally with "ext.####"'}

Factory.addProduct(PhoneNumber)


