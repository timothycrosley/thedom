'''
    test_Factory.py

    Tests the functionality of thedom/Factory.py

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from thedom.All import Factory
from thedom.Base import Invalid, WebElement
from thedom.Factory import Composite as CompositeFactory
from thedom.Factory import Factory as FactoryClass
from thedom.UITemplate import Template


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

    def test_buildFromTemplate(self):
        """test to ensure creating a webelement from a dictionary works"""

        #Try invalid input
        assert type(Factory.buildFromTemplate(None)) == Invalid
        assert type(Factory.buildFromTemplate(Template(create=None))) == Invalid
        assert type(Factory.buildFromTemplate(Template('SomeElementThatDoesNotExist'))) == Invalid

        template = Template('box', properties=(('style', 'margin:5px;'),),
                            childElements=(Template('button', id='My Field A', accessor="Field1",
                                                properties=(('style', 'margin-bottom:4px; margin-top:7px; clear:both;'),
                                                            ('text', 'Field 1:'))),
                                           Template('button', id='My Field B',
                                                properties=(('style', 'margin-bottom:4px; margin-top:7px; clear:both;'),
                                                            ('text', 'Field 2:'))),
                                           Template('label', id='My Field C',
                                                properties=(('style', 'margin-bottom:4px; margin-top:7px; clear:both;'),
                                                            ('text', 'Field 3:'))),
                                                            ))

        Factory.addProduct(FakeWebElement)

        accessors = {}
        testObject = Factory.buildFromTemplate(template, {'InputField1':"value"}, accessors=accessors)
        assert testObject.__class__.__name__ == "Box"
        assert testObject.style['margin'] == '5px'

        #Field 1
        childElement = testObject.childElements[0]
        assert childElement.__class__.__name__ == "Button"
        assert childElement.style == \
                    {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 1:"
        assert childElement == accessors['Field1']

        #Field 2
        childElement = testObject.childElements[1]
        assert childElement.__class__.__name__ == "Button"
        assert childElement.style == {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 2:"

        #Field 3
        childElement = testObject.childElements[2]
        assert childElement.__class__.__name__ == "Label"
        assert childElement.style == \
                    {'margin-bottom':'4px', 'margin-top':'7px', 'clear':'both'}
        assert childElement.text() == "Field 3:"


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
