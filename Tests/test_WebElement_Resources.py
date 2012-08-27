from test_WebElement_Base import ElementTester
from WebElements.All import Factory
from WebElements.Resources import ScriptContainer

class TestResourceFile(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ResourceFile", "Test")
        self.element.setFile("javascript.js")

    def test_setFile(self):
        self.element.setFile("")
        assert self.element.resourceType == None
        assert self.element.fileName == ""

        self.element.setFile("Style.css")
        assert self.element.resourceType == "css"
        assert self.element.fileName == "Style.css"

        self.element.setFile("Javascript.js")
        assert self.element.resourceType == "javascript"
        assert self.element.fileName == "Javascript.js"


class TestScriptContainer(ElementTester):

    def setup_method(self, method):
        self.element = ScriptContainer()

    def test_addScript(self):
        assert self.element._scripts == []

        self.element.addScript("alert('I am a script :D');")
        self.element.addScript("var value = 'I am another script';")
        assert self.element._scripts == ["alert('I am a script :D');",
                                                 "var value = 'I am another script';"]
        assert "alert('I am a script :D');" in self.element.toHtml()
        assert "var value = 'I am another script';" in self.element.toHtml()

    def test_removeScript(self):
        assert self.element._scripts == []

        self.element.addScript("alert('I am a script :D');")
        assert self.element._scripts == ["alert('I am a script :D');"]

        self.element.removeScript("alert('I am a script :D');")
        assert self.element._scripts == []

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("GoodTests.py test_WebElement_Resources.py", shell=True).wait()
