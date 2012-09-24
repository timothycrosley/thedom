#!/usr/bin/python
"""
   Name:
       Layout Elements

   Description:
       Contains Elements that make it easy to layout pages exactly like you want.

"""

import types

from Base import Invalid, TextNode

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
        className = className.lower()
        if self.products.has_key(className):
            return self.products[className](id, name, parent)
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
        if variableDict == None: variableDict = {}

        if not template:
            return Invalid()

        if type(template) in types.StringTypes:
            return TextNode(template)

        elementType = template.create
        if elementType == None:
            return False
        elementType = elementType.lower()

        id = template.id
        name = template.name
        accessor = template.accessor

        elementObject = self.build(elementType, id, name, parent)
        if elementObject:
            if idPrefix and not elementObject._prefix:
                elementObject.setPrefix(idPrefix)
            elementObject.setScriptContainer(scriptContainer)
            elementObject.setProperties(template.properties)
            if accessors != None:
                if accessor:
                    accessors[accessor] = elementObject
                elif  id:
                    accessors[id] = elementObject

            if elementObject.allowsChildren:
                for child in template.childElements or ():
                    childElement = self.buildFromTemplate(child,
                                        parent=elementObject.addChildElementsTo,
                                        accessors=accessors)
                    elementObject.addChildElement(childElement)
            if variableDict:
                elementObject.insertVariables(variableDict)
            return elementObject

        return Invalid()


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
                for productName, product in factory.products.iteritems():
                    self.products[factory.name.lower() + "." + productName] = product
