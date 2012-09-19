#!/usr/bin/python
"""
   Name:
       Layout

   Description:
       Contains Elements that will replace standard elements in a future iteration

"""

import Base
import Factory
from Layout import Box, LineBreak

Factory = Factory.Factory("Future")

class Horizontal(Box):
    """
        A container element that adds child elements horizontally.
        Updates: Future version removes the complexity of having to worry about seperate places to set the style,
                 supports fractional width, and creates an extra box for width to force width to be correct in
                 all browsers.
    """
    def __modifyChild__(self, childElement):
        width = childElement.style.pop('width', '')
        align = childElement.style.pop('float', 'left')

        if width == "0" or width == "hide":
            self.childElements.append(childElement)
        if not childElement.displayable:
            self.childElements.append(childElement)
            return

        if not childElement.tagName or width:
            container = Box.addChildElement(self, Box())
            container.addChildElement(childElement)
        else:
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            container = childElement
            self.childElements.append(childElement)

        container.style['float'] = align
        if width:
            container.style['vertical-align'] = 'middle'
            container.style['width'] = width

    def toHtml(self, formatted=False):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        lineBreak = Box.addChildElement(self, LineBreak())
        returnValue = Box.toHtml(self, formatted=formatted)
        self.childElements = oldChildElements
        return returnValue

Factory.addProduct(Horizontal)


class Vertical(Box):
    """
        A container that encourage elements to be added vertically with minimum html
    """
    def __modifyChild__(self, childElement):
        height = childElement.style.pop('height', '')

        if not childElement.displayable:
            self.childElements.append(childElement)
        elif not childElement.tagName or height:
            container = Box()
            container.style['height'] = height
            childElement.style['height'] = "100%"
            container.style['clear'] = "both"
            container.addChildElement(childElement)
            return Box.addChildElement(self, container)
        else:
            childElement.style['clear'] = "both"
            if not childElement.isBlockElement():
                childElement.addClass("WBlock")
            self.childElements.append(childElement)


    def toHtml(self, formatted=False):
        oldChildElements = self.childElements
        self.reset()
        for childElement in oldChildElements:
            self.__modifyChild__(childElement)
        lineBreak = Box.addChildElement(self, LineBreak())
        returnValue = Box.toHtml(self, formatted=formatted)
        self.childElements = oldChildElements
        return returnValue

Factory.addProduct(Vertical)
