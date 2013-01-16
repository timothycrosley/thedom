'''
    Parser.py

    Contains an object that will create a tree of WebElement objects when initialized with HTML

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

from . import Base
from .Base import WebElement, TextNode
from .MultiplePythonSupport import *

class WebElementTree(WebElement):
    """
        Creates a tree of webelement children from plain html
    """
    endTags = ["/>", ">"]
    startTags = ["</", "<"]
    whiteSpace = [' ', '\n', '\r', '\t']
    selfClosingTags = ['img', 'input', 'br', 'meta', 'link', 'hr', 'form:error']
    dontNest = ['td', 'tr', 'li']
    closeIfNested = ['a']
    forceTagEndBefore = ['body', 'head' , '']
    retainFormat = ['script', 'pre']
    missedEndTag = ("WARNING: end tag '</%(endTag)s>' " +
                    "at character %(endChar)i does not not match " +
                    "start tag '<%(startTag)s>' at character %(startChar)i line %(startLine)i " +
                    "resolving by closing '</%(startTag)s>' tag.")
    incorrectPlacement = ("WARNING: tag '</%(tag)s>' " +
                          "at character %(startChar)i must be ended before  " +
                          "'<%(forcedTag)s>' at character %(endChar)i line %(startLine)i " +
                          "resolving by closing '</%(tag)s>' tag.")

    def __init__(self, html="", tag="", parent=None):
        WebElement.__init__(self, parent=parent)
        self._tagName = tag
        if not parent:
            self._html = html
            self._length = len(html)
            self._index = 0
            self.startChar = 0

            self.parse()
        else:
            self.startChar = self.index() - len(self.startTag())

    def __representSelf__(self):
        return WebElement.__representSelf__(self).replace('WebElementTree', self._tagName)

    def html(self):
        """
            Returns the supplied html
        """
        if self.parent:
            return self.parent.html()

        return self._html

    def length(self):
        """
            Returns a length of the html
        """
        if self.parent:
            return self.parent.length()

        return self._length

    def index(self):
        """
            Returns the index within the html it is parsing
        """
        if self.parent:
            return self.parent.index()

        return self._index

    def setIndex(self, index):
        """
            Sets the parser index
        """
        if self.parent:
            return self.parent.setIndex(index)
        else:
            self._index = index

    def parse(self):
        """
            Commenses the parsing of the html
        """
        if not self.parent:
            self.reset()

        while self.more():
            (string, startTag) = self.textTillString(self.startTags + ['\n'])
            prevChar = self.index() - len(startTag)

            string = string.strip()
            if string:
                self.addChildElement(TextNode(string))

            if startTag == "<":
                (rawTagName, endedBy) = self.textTillString(self.endTags + self.whiteSpace + ['<'])
                tagName = rawTagName.lower().strip()
                if rawTagName.startswith('!'):#HTML Comment
                    if tagName.startswith('!--'):
                        (content, end) = self.textTillString('-->')
                        self.addChildElement(TextNode('<' + rawTagName + ' ' + content.replace('--', '==') + end))
                        continue
                    else:
                        (content, end) = self.textTillString('>')
                        self.addChildElement(TextNode('<' + rawTagName + ' ' + content + end))
                        continue
                elif endedBy == "<" or not tagName:
                    self.addChildElement(TextNode("&lt;" + tagName))
                    self.prev()
                    continue

                if((tagName in self.forceTagEndBefore and not self._tagName in ["html", '']) or
                   (self._tagName == tagName and (tagName in self.dontNest or tagName in self.closeIfNested))):

                    print(self.incorrectPlacement % {'tag':self._tagName,
                                                     'startChar':self.startChar,
                                                     'startLine':len(self.html()[:self.startChar].split("\n")),
                                                     'forcedTag':tagName,
                                                     'endChar':self.index()})
                    if not tagName in self.closeIfNested:
                        self.setIndex(prevChar)
                    break


                newTag = self.addChildElement(self.__class__(tag=tagName, parent=self))

                if endedBy in self.whiteSpace:
                    self.prev()
                    while self.more() and self.character() in self.whiteSpace:
                        newTag.addAttribute()

                    (text, endedBy) = self.textTillString(self.endTags)

                if tagName in self.selfClosingTags:
                    newTag._tagSelfCloses = True
                elif endedBy == "/>":
                    continue
                elif tagName in self.retainFormat:
                    (content, endTag) = self.textTillString('</' + tagName + '>')
                    content = content.strip()
                    if content:
                        newTag.addChildElement(TextNode(content + "\n"))
                    continue
                else:
                    newTag.parse()

            elif startTag == "</":
                (endTag, match) = self.textTillString(self.endTags + self.startTags)
                endTag = endTag.lower().strip()
                if endTag != self._tagName and not self._tagName in self.forceTagEndBefore:

                    print(self.missedEndTag % {'startTag':self._tagName,
                                               'endTag':endTag.strip(),
                                               'startChar':self.startChar,
                                               'startLine':len(self.html()[:self.startChar].split("\n")),
                                               'endChar':self.index()})
                    self.setIndex(prevChar)
                    break

                break

        if not self.parent:
            self.setIndex(0)

    def addAttribute(self):
        """
            Adds attributes to the newly created webelement based on the attributes within the html
        """
        (attribute, match) = self.textTillString(self.endTags + ['='])
        attribute = attribute.lower().strip()
        if attribute:
            if match == "=":
                while self.more() and self.character() in self.whiteSpace:
                    self.next()

                start = self.character()
                if start in ["'", '"']:
                    self.next()
                    (value, match) = self.textTillString(start)
                else:
                    (value, match) = self.textTillString(self.endTags + self.whiteSpace)
                    if match in self.whiteSpace:
                        self.prev(len(match))

            else:
                value = "true"

            if value == "":
                value = "_BLANK_"

            if attribute == "id":
                self.id = value
            elif attribute == "name":
                self.name = value
            elif attribute == "style":
                try:
                    self.setStyleFromString(value)
                except ValueError:
                    self.attributes['style'] = value
            elif attribute == "class":
                self.addClassesFromString(value)
            else:
                self.attributes[attribute] = value

        if match in self.endTags:
            self.prev(len(match))

    def more(self):
        """
            Returns true if there is more html to parse
        """
        return self.index() < self.length()

    def next(self, numberOfCharacters=1):
        """
            Increments the index by number of characters
        """
        self.setIndex(self.index() + numberOfCharacters)
        return self.index()

    def prev(self, numberOfCharacters=1):
        """
            Deincrements the index by number of characters
        """
        self.setIndex(self.index() - numberOfCharacters)
        return self.index()

    def character(self):
        """
            Returns the character in character at the current index
        """
        return self.html()[self.index()]

    def popCharacter(self):
        """
            removes the current character then moves to the next one, returning the current character
        """
        char = self.html()[self.index()]
        self.next()
        return char

    def characters(self, numberOfCharacters):
        """
            Returns characters at index + number of characters
        """
        return self.html()[self.index():self.index() + numberOfCharacters]

    def textTillString(self, strings):
        """
            Returns all text till it encounters the given string (or one of the given strings)
        """
        if type(strings) in (str, unicode):
            strings = [strings]

        text = ""
        matchedString = ""

        while self.more():
            for string in strings:
                if self.characters(len(string)) == string:
                    matchedString = string
                    break

            if matchedString:
                break

            text += self.popCharacter()

        self.next(len(matchedString))
        return (text, matchedString)
