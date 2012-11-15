"""
    Contains basic web validators - that validate both ClientSide and server side.
"""

import re
import string

import Factory
import Base
import Display
import Layout
from ClientSide import do, regexp, var, Script
from MethodUtils import CallBack

Factory = Factory.Factory("Validators")

class Validation(Display.Message):
    """
        Processes child validators to render validation results
    """
    __slots__ = ('userInput', )

    def value(self):
        """
            Returns the value that all validators should validate
        """
        return self.userInput.value()

    def addChildElement(self, childElement, ensureUnique=True):
        """
            Adds the validation control to all child elements
        """
        childElement.control = self



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

        def validate(self, data):
            pass

        def message(self, message):
            """
                Expands and returns a message based on a message key
            """
            return self.expandTemplate(self.serverSide.messages[message], self.associatedData())

        def error(self, message):
            return (self.serverSide.ERROR, self.message(message))

        def info(self, message):
            return (self.serverSide.INFO, self.message(message))

        def warning(self, message):
            return (self.serverSide.WARNING, self.message(message))

        def success(self, message):
            return (self.serverSide.SUCCESS, self.message(message))

    def validate(self):
        pass

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
                context(self.showError(self.serverSide.message('notEmpty')))
            return context

    def validate(self):
        if not self.forElement.value():
            self.showError(self.message("notEmpty"))

Factory.addProduct(NotEmpty)


class Int(Validator):
    messages = {'notInt':'Please enter an integer value'}

    class ClientSide(Validator.ClientSide):
        def validate(self):
            assignment = self.assign('value', self.serverSide.forElement.clientSide.value())
            with self.value.IF != do.parseInt(self.value, 10) as context:
                context(self.showError(self.serverSide.message("notInt")))

            return assignment(context)

    def validate(self):
        try:
            self.forElement.setValue(int(self.forElement.value()))
        except ValueError:
            return self.showError(self.message("notInt"))

Factory.addProduct(Int)


class PatternValidator(Validator):
    """
        Base class for validating a field against a regular expression
    """
    pattern = r''
    messages = {'format':'Please enter a value using the specified format'}

    class ClientSide(Validator.ClientSide):
        def validate(self):
            assignment = self.assign('value', self.serverSide.forElement.clientSide.value())
            with regexp(self.serverSide.pattern).do('test', self.value).IF != True as context:
                context(self.showError(self.message("format")))
            return assignment(context)

    def validate(self):
        if not self.pattern.match(self.forElement.value):
            self.shorError(self.message("format"))


class ValidEmail(PatternValidator):
    """
        Validates that an email matches a specified format
    """
    pattern = re.compile('''[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:[\.a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*''' \
                         '''[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])+''')
    messages = {'format':'Please enter an email in the form: email@domain.tld'}

Factory.addProduct(ValidEmail)


class ValidPhoneNumber(PatternValidator):
    """
        Validates that a phone number is defined with a valid format
    """
    pattern = re.compile(r'^\s*(?:1-)?(\d\d\d)[\- \.]?(\d\d\d)[\- \.]?(\d\d\d\d)(?:\s*ext\.?\s*(\d+))?\s*$', re.I)
    messages = {'format':'Please enter a number, with area code, in the form ###-###-####, optionally with "ext.####"'}

class All(Validator):
    """
        Validates using short circuit logic with all defined validators
    """
    __slots__ = ('validators', )

    def __init__(self, id, name=None, parent=None, key=None, **kwargs):
        Validator.__init__(self, id, name, parent, **kwargs)

        self.validators = []

