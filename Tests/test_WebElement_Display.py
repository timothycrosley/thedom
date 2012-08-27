#!/usr/bin/python

from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestImage(ElementTester):

    def setup_method(self, element):
        self.element = Factory.build("Image", name="Test")

    def test_loadFromDictionary(self):
        self.element.loadFromDictionary({'value':'images/lightbulb.png'})
        assert self.element.value() == 'images/lightbulb.png'

    def test_value(self):
        assert not self.element.value()
        self.element.setValue("images/lightbulb.png")
        assert self.element.value() == "images/lightbulb.png"
        assert self.element.attributes['src'] == "images/lightbulb.png"


class TestList(ElementTester):

    def setup_class(self):
        self.element = Factory.build('List', 'testList')


class TestLabel(object):

    def setup_method(self, method):
        self.element = Factory.build("Label", "Test")

    def test_text(self):
        assert not self.element.text()
        self.element.setText("I changed the text")
        assert self.element.text() == "I changed the text"
        assert "I changed the text" in self.element.toHtml()

    def test_loadFromDictionary(self):
        assert self.element.text() == ""
        self.element.loadFromDictionary({'text':'I set the text'})
        assert self.element.text() == "I set the text"
        assert "I set the text" in self.element.toHtml()


class TestPreformattedText(TestLabel):

    def setup_method(self, method):
        self.element = Factory.build("PreformattedText", "Test")


class TestError(ElementTester):

    def setup_class(self):
        self.element = Factory.build("error", name="Test")


class TestFormError(ElementTester):

    def setup_class(self):
        self.element = Factory.build("formError", name="TestFormError")


class TestEmpty(ElementTester):

    def setup_class(self):
        self.element = Factory.build("box")
        self.element.addChildElement(Factory.build("empty", name="Test"))

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("py.test test_WebElement_Display.py", shell=True).wait()
