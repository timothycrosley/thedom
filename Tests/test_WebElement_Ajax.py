from test_WebElement_Base import ElementTester
from WebElements.Ajax import AjaxController, AJAXScriptContainer, ControlInstance

class TestAJAXScriptContainer(ElementTester):

    def setup_class(self):
        self.element = AJAXScriptContainer()


class CustomControl(AjaxController):
    hidden = True
    autoload = "AJAX"
    autoreload = 1000

class TestAjaxController(ElementTester):

    def setup_class(self):
        self.element = AjaxController('control')

    def test_customControl(self):

        control = CustomControl('control')
        control.addJavascriptEvent('onload', control.update())
        control.addJavascriptEvent('onload', control.submit())

        assert control.shown() == False
        self._parseElement(control)


class TestControlInstance(ElementTester):

    def setup_class(self):
        control = AjaxController('control')
        self.element = ControlInstance(control)
