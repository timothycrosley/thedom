from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestHiddenValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenValue", name="Test")

    def test_attributes(self):
        assert self.element.attributes['type'] == 'hidden'

    def test_text(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("I changed the value")
        assert self.element.value() == "I changed the value"
        assert self.element.text() == "I changed the value"
        self.element.setText("I changed the text")
        assert self.element.text() == "I changed the text"
        assert self.element.value() == "I changed the text"


class TestHiddenBooleanValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenBooleanValue", name="Test")

    def test_value(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("1")
        assert self.element.value() is True
        self.element.setText(True)
        assert self.element.value() is True
        self.element.setValue("")
        assert self.element.value() is False
        self.element.setValue(False)
        assert self.element.value() is False


class TestHiddenIntValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("HiddenIntValue", name="Test")

    def test_value(self):
        assert not self.element.text()
        assert not self.element.value()
        self.element.setValue("1")
        assert self.element.value() == 1
        assert self.element.text() == 1
        self.element.setText("")
        assert self.element.text() == 0
        assert self.element.value() == 0
        self.element.setText(None)
        assert self.element.text() == 0
        assert self.element.value() == 0
        self.element.setText(2)
        assert self.element.text() == 2
        assert self.element.value() == 2
        self.element.setText(0)
        assert self.element.text() == 0
        assert self.element.value() == 0

