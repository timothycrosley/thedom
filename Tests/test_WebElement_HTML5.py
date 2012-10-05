"""
    Test all HTML5 elements
"""

from test_WebElement_Base import ElementTester
from WebElements.HTML5 import Factory


class TestFileUploader(ElementTester):

    def setup_class(self):
        self.element = Factory.build("fileuploader", "test")