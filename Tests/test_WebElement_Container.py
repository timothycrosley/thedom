from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestDropDownMenu(ElementTester):

    def setup_class(self):
        self.element = Factory.build("dropdownmenu", "Test")


class TestAutocomplete(ElementTester):

    def setup_class(self):
        self.element = Factory.build("autocomplete", "Test")


class TestTab(ElementTester):

    def setup_class(self):
        self.element = Factory.build("tab", "Test")


class TestTabContainer(ElementTester):

    def setup_class(self):
        self.element = Factory.build('TabContainer', 'Test')

    def test_tabs(self):
        tab1 = self.element.addChildElement(Factory.build('Tab', 'Tab1'))
        tab2 = self.element.addChildElement(Factory.build('Tab', 'Tab2'))
        tab3 = self.element.addChildElement(Factory.build('Tab', 'Tab3'))
        assert tab1.isSelected
        assert not tab2.isSelected
        assert not tab3.isSelected

        tab2.select()
        assert not tab1.isSelected
        assert tab2.isSelected
        assert not tab3.isSelected

        tab3.select()
        assert not tab1.isSelected
        assert not tab2.isSelected
        assert tab3.isSelected


class TestAccordion(ElementTester):

    def setup_class(self):
        self.element = Factory.build("accordion", "Test")


class TestAccordion(ElementTester):

    def setup_class(self):
        self.element = Factory.build("accordion", "Test")


class TestFormContainer(ElementTester):

    def setup_class(self):
        self.element = Factory.build("FormContainer", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Container", name="Container"))

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("GoodTests.py test_WebElement_Container.py", shell=True).wait()
