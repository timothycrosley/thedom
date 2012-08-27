from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Link", "TestLink")

    def test_destination(self):
        assert not self.element.destination()

        self.element.setDestination("www.google.com")
        assert self.element.destination() == "www.google.com"
        assert self.element.toHtml().find("www.google.com") > 0

    def test_text(self):
        assert not self.element.text()
        self.element.setText("TEXT!")
        assert self.element.text() == "TEXT!"


class TestPopupLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build('PopupLink', 'myPopupLink')


class TestButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Button", name="Test")
        self.submitElement = Factory.build("SubmitButton")

    def test_attributes(self):
        assert self.element.attributes['type'] == 'button'
        assert 'button' in self.element.classes
        assert self.submitElement.attributes['type'] == 'submit'
        assert 'button' in self.submitElement.classes


class TestPrintButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build('PrintButton', 'test')


class TestSubmitButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build('SubmitButton', 'test')


class TestToggleButton(ElementTester):

    def setup_method(self, obj):
        self.element = Factory.build("ToggleButton", "Test")

    def test_attributes(self):
        assert self.element.button.id == "Test"

    def test_toggle(self):
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "ToggledOn" in self.element.button.classes

        self.element.toggle()
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "ToggledOn" in self.element.button.classes

        self.element.toggle()
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "ToggledOn" in self.element.button.classes

        self.element.toggleOff()
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "ToggledOn" in self.element.button.classes

        self.element.toggleOn()
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "ToggledOn" in self.element.button.classes

    def test_value(self):
        assert self.element.value() == ""
        assert self.element.button.value() == ""
        self.element.setValue("I changed the value")
        assert self.element.value() == "I changed the value"
        assert self.element.button.value() == "I changed the value"

    def test_insertVariablesToggledOn(self):
        self.element.insertVariables({'Test:Toggled':"on"})
        assert self.element.toggled()
        assert self.element.toggledState.value() == 'on'
        assert "ToggledOn" in self.element.button.classes


    def test_insertVariablesToggledFalse(self):
        self.element.insertVariables({'Test:Toggled':"off"})
        assert not self.element.toggled()
        assert self.element.toggledState.value() == 'off'
        assert not "ToggledOn" in self.element.button.classes


class TestToggleLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build('ToggleLink', 'test')

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("py.test test_WebElement_Buttons.py", shell=True).wait()
