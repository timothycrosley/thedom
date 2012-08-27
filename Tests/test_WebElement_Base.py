import cPickle as pickle

from WebElements.All import Factory
from WebElements.Base import Invalid, TemplateElement, WebElement
from WebElements.Resources import ScriptContainer
from lxml import etree

parser = etree.XMLParser()

class TestWebElement(object):

    def setup_method(self, method):
        self.container = Factory.build('Box', '1')
        self.container.key = 'my.test.container'

        self.firstChild = self.container.addChildElement(Factory.build('Textbox',
                                                                       '2'))
        self.firstChild.key = 'my.test.firstChild'

    def test_addChildElement(self):
        #Ensure element adds correctly if parent element allows children
        addElement = WebElement()
        assert self.container.addChildElement(addElement) == addElement
        assert self.container.childElements[1] == addElement

        #Ensure element is not added if parent element does not allow children
        assert not self.firstChild.addChildElement(WebElement())
        assert len(self.container.childElements) == 2

        #Ensure child element will not add twice
        self.container.addChildElement(addElement)
        assert len(self.container.childElements) == 2
        assert self.container.childElements[1] == addElement

        #Ensure child element will add if ensure unique is false
        self.container.addChildElement(addElement, ensureUnique=False)
        assert len(self.container.childElements) == 3
        assert self.container.childElements[1] == addElement
        assert self.container.childElements[2] == addElement

    def test_editable(self):
        self.firstChild.setEditable(False)
        self.container.setEditable(False)

        assert not self.container.editable()
        assert not self.firstChild.editable()

    def test_hideAndShow(self):
        assert self.container.shown()
        self.container.hide()
        assert not self.container.shown()
        self.container.show()
        assert self.container.shown()

    def test_validators(self):
        #test to ensure all set validators are returned correctly
        self.container.validator = 'MyContainerValidator'
        self.firstChild.validator = 'MyFirstChildValidator'

        assert self.container.validators() == {'1':'MyContainerValidator',
                                               '2':'MyFirstChildValidator'}
        assert self.firstChild.validators() == {'2':'MyFirstChildValidator'}

    def test_fullName(self):
        #Ensure stored values are returned correctly
        assert self.container.fullName() == "1"
        assert self.firstChild.fullName() == "2"

        #Change names and add a prefix
        self.container.name = "NewName1"
        self.firstChild.name = "NewName2"
        self.container.setPrefix("NewPrefix1-")
        self.firstChild.setPrefix("NewPrefix2-")

        #Ensure changes are reflectet correctly
        assert self.container.fullName() == "NewPrefix1-NewName1"
        assert self.firstChild.fullName() == "NewPrefix2-NewName2"

    def test_fullId(self):
        #Ensure stored values are returned correctly
        assert self.container.fullId() == "1"
        assert self.firstChild.fullId() == "2"

        #Change names and add a prefix
        self.container.id = "NewId1"
        self.firstChild.id = "NewId2"
        self.container.setPrefix("IdPrefix1-")
        self.firstChild.setPrefix("IdPrefix2-")

        #Ensure changes are reflectet correctly
        assert self.container.fullId() == "IdPrefix1-NewId1"
        assert self.firstChild.fullId() == "IdPrefix2-NewId2"

    def test_jsId(self):
        assert self.container.jsId() == "1"

    def test_reset(self):
        assert len(self.container.childElements) > 0
        self.container.reset()
        assert len(self.container.childElements) == 0

    def test_javascriptEvents(self):
        """Test to ensure that adding and removing javascript events works correctly"""
        #add javascript events
        self.container.addJavascriptEvent("onload",
                                          "alert('ALERT!! You hava a virus on your"\
                                          +" computer!!!!');")
        self.container.addJavascriptEvent("onload",
                                          "alert('please go to freevirusscanner.com');")
        self.container.addJavascriptEvent("onload",
                                          "alert('there (for only $14.95) we can remove "\
                                          +"all your viruses forever. Seriously. I mean why "\
                                          +"would we lie about this? After all no one on "\
                                          +"the  interwebs lies anyways ;-)');")
        self.firstChild.addJavascriptEvent("onclick", "alert('hello');")
        self.firstChild.addJavascriptEvent("onclick",
                                                 "alert('why are you clicking me?');")

        #ensure correct results are returned
        assert self.container.javascriptEvent("onload") == \
                                       "alert('ALERT!! You hava a virus on your"\
                                       + " computer!!!!'); "\
                                       +"alert('please go to freevirusscanner.com'); "\
                                       +"alert('there (for only $14.95) we can remove "\
                                       + "all your viruses forever. Seriously. I mean why "\
                                       + "would we lie about this? After all no one on "\
                                       + "the  interwebs lies anyways ;-)');"
        assert self.firstChild.javascriptEvent("onclick") == \
                          "alert('hello'); alert('why are you clicking me?');"

        #remove javascript events
        self.container.removeJavascriptEvent("onload",
                                         "alert('there (for only $14.95) we can remove "\
                                         + "all your viruses forever. Seriously. I mean why "\
                                         + "would we lie about this? After all no one on "\
                                         + "the  interwebs lies anyways ;-)');")
                                         # ^ The marking department told me to remove
                                         # the above alert message. They said it wasn't
                                         # proffesional enough :(.
        self.firstChild.removeJavascriptEvent("onclick")
                                        # ^ Appearently they were also against having
                                        # an alert pop up when clicking a textbox :o


        #ensure event removals are reflected correctly
        assert self.container.javascriptEvent("onload") == \
                                       "alert('ALERT!! You hava a virus on your"\
                                       +" computer!!!!'); "\
                                       +"alert('please go to freevirusscanner.com');"
        assert self.firstChild.javascriptEvent("onclick") == ''

    def test_prefix(self):
        """Test to ensure that setting and viewing the prefix works correctly"""

        #set the innertext
        self.container.setPrefix("MyAmazingPrefix-")

        #ensure it is returned correctly
        assert self.container.prefix() == "MyAmazingPrefix-"
        assert self.container.fullId() == "MyAmazingPrefix-1"
        assert self.firstChild.prefix() == "MyAmazingPrefix-"
        assert self.firstChild.fullId() == "MyAmazingPrefix-2"

        #set it to nothing
        self.container.setPrefix(" ")
        #ensure it is returned correctly
        assert self.container.prefix() == ""
        assert self.container.fullId() == "1"
        assert self.firstChild.prefix() == ""
        assert self.firstChild.fullId() == "2"



    def test_startTag(self):
        """Test to ensure startTag() works correctly"""
        assert self.container.startTag() == '<div name="1" id="1">'
        assert self.firstChild.startTag() == '<input name="2" id="2" type="text" class="WETextBox" />'

    def test_endTag(self):
        """Test to ensure endTag() works correctly"""
        self.container.tagName = 'div'
        assert self.container.endTag() == '</div>'
        assert self.firstChild.endTag() == ''

    def test_content(self):
        """Test to ensure content() works correctly"""
        assert self.container.content() == '<input name="2" id="2" type="text" class="WETextBox" />'
        assert self.firstChild.content() == ''

    def test_toHtml(self):
        """Test to ensure toHtml() works correctly"""
        assert self.container.toHtml() == '<div name="1" id="1"><input' + \
                                          ' name="2" id="2" type="text" class="WETextBox" /></div>'
        assert self.firstChild.toHtml({}) == '<input name="2" id="2" type="text" class="WETextBox" />'

    def test_insertExportVariables(self):
        """Test to ensure inserting variables updates a webElement correctly,
            so that it can then export those same variables"""

        self.container.setPrefix("MyPrefix-")
        self.firstChild.name = "name"

        #Test inserting by Id works correctly
        self.container.insertVariables({'2':'MyTestValue'})
        assert self.firstChild.value() == 'MyTestValue'
        assert self.firstChild.exportVariables()['my']['test']['firstChild'] == 'MyTestValue'

        #Test inserting by FullId works correctly
        self.container.insertVariables({'MyPrefix-2':'MyNewTestValue'})
        assert self.firstChild.value() == 'MyNewTestValue'
        assert self.firstChild.exportVariables()['my']['test']['firstChild'] == 'MyNewTestValue'

        #Test inserting by key works correctly
        self.container.insertVariables({'my':{'test':{'firstChild':'MyEvenNewerTestValue'}}})
        assert self.firstChild.value() == 'MyEvenNewerTestValue'
        assert self.firstChild.exportVariables()['my']['test']['firstChild'] == 'MyEvenNewerTestValue'

        #Test to ensure correct variable priority (key > fullid > id > fullname > name)
        self.container.insertVariables({'my':{'test':{'firstChild':'keyValue'}},
                                        'MyPrefix-2':'fullIdValue',
                                        '2':'idValue',
                                        'MyPrefix-name':'fullNameValue',
                                        'name':'nameValue'})
        assert self.firstChild.value() == 'keyValue'
        self.container.insertVariables({'MyPrefix-2':'fullIdValue',
                                        '2':'idValue',
                                        'MyPrefix-name':'fullNameValue',
                                        'name':'nameValue'})
        assert self.firstChild.value() == 'fullIdValue'
        self.container.insertVariables({'2':'idValue',
                                        'MyPrefix-name':'fullNameValue',
                                        'name':'nameValue'})
        assert self.firstChild.value() == 'idValue'
        self.container.insertVariables({'MyPrefix-name':'fullNameValue',
                                        'name':'nameValue'})
        assert self.firstChild.value() == 'fullNameValue'
        self.container.insertVariables({'name':'nameValue'})
        assert self.firstChild.value() == 'nameValue'


class ElementTester(object):

    def test_validXML(self):
        self._parseElement(self.element)

    def _parseElement(self, element):
        if not element.scriptContainer():
            element.setScriptContainer(ScriptContainer())
            element.scriptContainer().toHtml()

        try:
            root = etree.fromstring(element.toHtml().replace("&amp;", "&").replace("&", "&amp;"). \
                                                     replace("&nbsp;", " ").replace("form:error", "span").
                                                     replace("error", "span"), parser)
        except Exception, e:
            print element.toHtml()
            raise e

    def test_isValid(self):
        assert not isinstance(self.element, Invalid)

    def test_pickleable(self):
        pickled = pickle.dumps(self.element)
        self._parseElement(pickle.loads(pickled))


class TestTemplateElement(ElementTester):

    def setup_class(self):
        self.element = TemplateElement(template={'create':'box',
                                                 'accessor':'container'},
                                       factory=Factory)

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("py.test test_WebElement_Base.py", shell=True).wait()
