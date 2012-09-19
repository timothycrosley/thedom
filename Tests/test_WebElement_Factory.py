#!/usr/bin/python
"""
    Name:
        test_WebElements_Factory.py
    Description:
        Test the functionality of the webelement Factory classes
"""

from WebElements.All import Factory
from WebElements.Base import Invalid, WebElement
from WebElements.Factory import Composite as CompositeFactory, Factory as FactoryClass

class FakeWebElement(WebElement):
    def __init__(self, id=None, name=None, parent=None):
        WebElement.__init__(self, "Id", "Name")


class TestFactory(object):

    def setup_class(self):
        baseElement = Factory.build("box")
        baseElement.setPrefix("myPrefix-")
        self.base = baseElement

    def test_build(self):
        """test to ensure using the factory to create a webelement object works"""
        createdObject = Factory.build("textbox", "myId", "myName")
        self.base.addChildElement(createdObject)

        assert createdObject.fullId() == "myPrefix-myId"
        assert createdObject.fullName() == "myPrefix-myName"
        assert createdObject.parent == self.base

    def test_buildNonExistant(self):
        """test to ensure that an attempt to build an non existant webElement
           will create an Invalid webElement"""
        createdObject = Factory.build("SomeRandomThingThatDoesNotExist")
        assert type(createdObject) == Invalid

    def test_addProduct(self):
        """test to ensure adding a new webelement to the factory works"""
        class FakeWebElement(WebElement):
            def __init__(self, id=None, name=None, parent=None):
                WebElement.__init__(self, "Id", "Name")

        Factory.addProduct(FakeWebElement)

        createdObject = Factory.build("fakewebelement")
        self.base.addChildElement(createdObject)

        assert createdObject.fullId() == "myPrefix-Id"
        assert createdObject.fullName() == "myPrefix-Name"
        assert createdObject.parent == self.base

    def test_buildFromDictionary(self):
        """test to ensure creating a webelement from a dictionary works"""

        #Try invalid input
        assert type(Factory.buildFromDictionary({})) == Invalid
        assert Factory.buildFromDictionary({'doesNotContainCreate':True}) is False
        assert type(Factory.buildFromDictionary({'create':'SomeElementThatDoesNotExist'})) == Invalid

        paramDict = {'create':'box',
                     'style':'margin:5px;',
                     'childElements':
                        [{'create':'textfield',
                          'id':'My Field A',
                          'style':'margin-bottom:4px; margin-top:7px; clear:both;',
                          'text':'Field 1:',
                          'accessor':'Field1'},
                         {'create':'textfield',
                          'id':'My Field B',
                          'style':'margin-bottom:4px; margin-top:7px; clear:both;',
                          'text':'Field 2:'},
                         {'create':'textareafield',
                          'id':'My Field C',
                          'style':'margin-bottom:4px; margin-top:7px; clear:both;',
                          'text':'Field 3:'}]}

        Factory.addProduct(FakeWebElement)

        accessors = {}
        testObject = Factory.buildFromDictionary(paramDict, {'InputField1':"value"}, accessors=accessors)
        assert testObject.__class__.__name__ == "Box"
        assert testObject.style['margin'] == '5px'

        #Field 1
        childElement = testObject.childElements[0]
        assert childElement.__class__.__name__ == "TextField"
        assert childElement.style == \
                    {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 1:"
        assert childElement.userInput.fullId() == "My Field A"
        assert childElement.userInput.__class__.__name__ == "TextBox"
        assert childElement == accessors['Field1']

        #Field 2
        childElement = testObject.childElements[1]
        assert childElement.__class__.__name__ == "TextField"
        assert childElement.style == {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 2:"
        assert childElement.userInput.fullId() == "My Field B"
        assert childElement.userInput.__class__.__name__ == "TextBox"

        #Field 3
        childElement = testObject.childElements[2]
        assert childElement.__class__.__name__ == "TextAreaField"
        assert childElement.style == \
                    {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 3:"
        assert childElement.userInput.fullId() == "My Field C"
        assert childElement.userInput.__class__.__name__ == "TextArea"


class TestCompositeFactory(object):

    def test_composite(self):
        generalMotors = FactoryClass()
        class Volt(object):
            pass
        generalMotors.addProduct(Volt)

        toyota = FactoryClass()
        class Prius(object):
            pass
        toyota.addProduct(Prius)

        # oh no! both companies were bought out!
        electricCarCompanyOfTheFuture = CompositeFactory((generalMotors, toyota))
        assert electricCarCompanyOfTheFuture.products == {'volt':Volt, 'prius':Prius}

