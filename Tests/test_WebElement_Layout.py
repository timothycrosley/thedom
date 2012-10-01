from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestStack(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Stack", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("box", name="box"))


class TestBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Box", name="Test")


class TestFlow(ElementTester):

    def setup_class(self):
        self.element = Factory.build("box", name="Test")
        self.flowContainer = self.element.addChildElement(Factory.build("flow", name="flow"))
        self.flowContainer.addChildElement(Factory.build("Button", name="Button"))
        self.flowContainer.addChildElement(Factory.build("box", name="box"))

class TestHorizontal(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Horizontal", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Container", name="Container"))


class TestVertical(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Vertical", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Container", name="Container"))


class TestFields(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Fields", name="Test")


class TestLineBreak(ElementTester):

    def setup_class(self):
        self.element = Factory.build("lineBreak", name="Test")


class TestHorizontalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('HorizontalRule', 'test')


class TestVerticalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('VerticalRule', 'test')

