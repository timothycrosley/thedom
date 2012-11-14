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


class Validator(Display.Message):
    """
        The base abstract validator that should be sub-classed to define new validators
    """
    __slots__ = ('input', 'formMessage')
    messages = {'empty':'A value is required for this field'}

    class ClientSide(Display.Message.ClientSide):

        def validate(self, data):
            pass

        def associatedData(self):
            """
                Defines the clientSide dictionary of data that can be used to populate messages
            """
            return Script(var({'field':self.element.forElement.clientSide.value()}))

        def message(self, message):
            """
                Expands and returns a message based on a message key
            """
            return self.expandTemplate(self.element.messages[message], self.associatedData())

    def validate(self):
        pass

    def associatedData(self):
        """
            Defines a dictionary of data that can be used to populate messages
        """
        return {'field':self.forElement.value()}

    def message(self, message):
        """
            Expands and returns a message based on a message key
        """
        return string.Template(self.messages[message]).safe_substitute(self.associatedData())


class NotEmpty(Validator):
    messages = {'notEmpty':'Please enter a value'}

    class ClientSide(Validator.ClientSide):
        def validate(self):
            with self.element.forElement.clientSide.value().IF == "" as context:
                context(self.showError(self.element.message('notEmpty')))
            return context

    def validate(self):
        if not self.forElement.value():
            self.showError(self.message("notEmpty"))

Factory.addProduct(NotEmpty)


class Int(Validator):
    messages = {'notInt':'Please enter an integer value'}

    class ClientSide(Validator.ClientSide):
        def validate(self):
            assignment = self.assign('value', self.element.forElement.clientSide.value())
            with self.value.IF != do.parseInt(self.value, 10) as context:
                context(self.showError(self.element.message("notInt")))

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
            assignment = self.assign('value', self.element.forElement.clientSide.value())
            with regexp(self.element.pattern).do('test', self.value).IF != True as context:
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
