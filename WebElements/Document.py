#!/usr/bin/python
"""
   Name:
       Layout

   Description:
       Contains Elements that make it easy to layout pages exactly like you want.

"""

import Base
import Factory
from MethodUtils import CallBack

Factory = Factory.Factory(Base.Invalid, name="Document")

DOCTYPE_XHTML_TRANSITIONAL = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
                              '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
DOCTYPE_XHTML_STRICT = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
                        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
DOCTYPE_XHTML_FRAMESET = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
                          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">')
DOCTYPE_HTML4_TRANSITIONAL = ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" '
                              '"http://www.w3.org/TR/REC-html40/loose.dtd">')
DOCTYPE_HTML4_STRICT = ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"'
                        '"http://www.w3.org/TR/html4/strict.dtd">')
DOCTYPE_HTML4_FRAMESET = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
                          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">')

class MetaData(Base.WebElement):
    """
        A webelement implementation of the meta tag
    """
    tagName = "meta"
    displayable = False

    properties = Base.WebElement.properties.copy()
    properties['value'] = {'action':'setValue'}
    properties['name'] = {'action':'setName'}

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self)

    def value(self):
        """
            Returns the meta tags value
        """
        return self.attributes.get('content')

    def setValue(self, value):
        """
            Sets the meta tags value
        """
        self.attributes['content'] = value

    def getName(self):
        """
            Returns the name of the meta tag
         """
        return self.name

    def setName(self, name):
        """
            Sets the name of the meta tag
        """
        self.name = name

    def shown(self):
        """
            Meta tags are never visible
        """
        return False

Factory.addProduct(MetaData)


class HTTPHeader(MetaData):
    """
        A webelement that represents an http header meta tag
    """
    def getName(self):
        """
            Returns the headers name
        """
        return self.attributes.get('http-equiv')

    def setName(self, name):
        """
            Sets the headers name
        """
        self.attributes['http-equiv'] = name

Factory.addProduct(HTTPHeader)


class Document(Base.WebElement):
    """
        A WebElement representation of the overall document that fills a single page
    """
    doctype = DOCTYPE_HTML4_TRANSITIONAL
    tagName = "html"
    properties = Base.WebElement.properties.copy()
    properties['doctype'] = {'action':'classAttribute'}
    properties['title'] = {'action':'title.setText'}
    properties['contentType'] = {'action':'contentType.setValue'}
    properties['xmlns'] = {'action':'attribute'}

    class Head(Base.WebElement):
        """
            Documents Head
        """
        tagName = "head"

    class Body(Base.WebElement):
        """
            Documents Body
        """
        tagName = "body"

    class Title(Base.WebElement):
        """
            Documents Title
        """
        tagName = "title"

        def setText(self, text):
            """
                Sets the document title
            """
            self.textBeforeChildren = text

        def text(self):
            """
                Returns the document title
            """
            return self.textBeforeChildren

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self)
        self.head = self.addChildElement(self.Head())
        self.body = self.addChildElement(self.Body())
        self.title = self.head.addChildElement(self.Title())
        self.contentType = self.addHeader('Content-Type', 'text/html; charset=UTF-8')

    def addMetaData(self, name, value):
        """
            Will add a meta tag based on name+value pair
        """
        metaTag = self.head.addChildElement(MetaData())
        metaTag.setName(name)
        metaTag.setValue(value)
        return metaTag

    def addHeader(self, name, value):
        """
            Will add an http header pair based on name+value pair
        """
        header = self.head.addChildElement(HTTPHeader())
        header.setName(name)
        header.setValue(value)
        return header

    def toHtml(self, variableDict=None, formatted=False):
        return self.doctype + "\n" + Base.WebElement.toHtml(self, variableDict, formatted)

    def addChildElement(self, childElement, ensureUnique=True):
        if type(childElement) in [self.Head, self.Body]:
            return Base.WebElement.addChildElement(self, childElement, ensureUnique)
        elif childElement.tagName in ['title', 'base', 'link', 'meta', 'script', 'style']:
            return self.head.addChildElement(childElement, ensureUnique)
        else:
            return self.body.addChildElement(childElement, ensureUnique)

Head = Document.Head
Body = Document.Body
Title = Document.Title
Factory.addProduct(Document)
