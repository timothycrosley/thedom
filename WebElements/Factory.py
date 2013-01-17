'''
    Factory.py

    The WebElement Factory provides a mechanism for building any element the factory has knowledge of
    simply by defining its name (as a string) and its main attributes, as well as providing the ability
    to combine multiple factories into one

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

import types

from .Base import Invalid, TextNode
from .MultiplePythonSupport import *

class Factory(object):
    def __init__(self, name=""):
        self.products = {}
        self.name = name

    def addProduct(self, productClass):
        """
            Adds a WebElement to the list of products that can be built from the factory:
                productClass - the WebElement's class
        """
        self.products[productClass.__name__.lower()] = productClass

    def build(self, className, id=None, name=None, parent=None):
        """
            Builds a WebElement instance from the className:
                className - the class name of the webElement (case insensitive)
                id - the unique id to assign to the newly built element
                name - the non-unique identifier to asign to the newly built element
                parent - the element that will contain the newly built element
        """
        className = className and className.lower() or ""
        product = self.products.get(className, None)
        if product:
            return product(id, name, parent)
        else:
            print(self.name + " has no product " + className + " sorry :(")
            return Invalid()

    def buildFromTemplate(self, template, variableDict=None, idPrefix=None, parent=None,
                            scriptContainer=None, accessors=None):
        """
            Builds an WebElement or a tree of web elements from a dictionary definition:
                template - the WebElement template node definition tree
                variableDict - a dictionary of variables (id/name/key):value to use to populate the
                               tree of WebElements
                idPrefix - a prefix to prepend before each element id in the tree to distinguish it
                           from a different tree on the page
                parent - the webElement that will encompass the tree
                scriptContainer - a container (AJAXScriptContainer/ScriptContainer) to throw scripts
                                  in
                accessors - pass in a dictionary to have it updated with element accessors
        """
        if not template:
            return Invalid()

        if type(template) in (str, unicode):
            return TextNode(template)

        ID = template.id
        accessor = template.accessor

        elementObject = self.build(template.create, ID, template.name, parent)
        if idPrefix and not elementObject._prefix:
            elementObject.setPrefix(idPrefix)
        elementObject.setScriptContainer(scriptContainer)
        elementObject.setProperties(template.properties)
        if accessors is not None:
            if accessor:
                accessors[accessor] = elementObject
            elif ID:
                accessors[ID] = elementObject

        if elementObject.allowsChildren:
            addChildElement = elementObject.addChildElement
            buildFromTemplate = self.buildFromTemplate
            addChildElementsTo = elementObject.addChildElementsTo
            for child in template.childElements or ():
                childElement = buildFromTemplate(child, parent=addChildElementsTo, accessors=accessors)
                addChildElement(childElement)
        if variableDict:
            elementObject.insertVariables(variableDict)

        return elementObject

class Composite(Factory):
    """
        Allows you to combine one or more web elements factories to build a composite factory.

        If two or more elements identically named elements are contained within the factories --
        the last factory passed in will override the definition of the element.
    """
    def __init__(self, factories):
        Factory.__init__(self)

        for factory in factories:
            self.products.update(factory.products)
            if factory.name:
                for productName, product in iteritems(factory.products):
                    self.products[factory.name.lower() + "-" + productName] = product
