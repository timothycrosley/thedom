"""
    Tests elements that have to do explicitly with the physical printing of content
"""

from test_WebElement_Base import ElementTester
from WebElements.All import Factory


class TestPageBreak(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build('pagebreak', 'test')


class TestUnPrintable(ElementTester):

    def setup_method(self, method):
        self.element = Factory.build('unprintable', 'test')
