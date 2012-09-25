#!/usr/bin/python
"""
   Name:
       CodeDocumentation

   Description:
       Contains elements that are used for displaying and documenting code

"""

try:
    hasPygments = True
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
except ImportError:
    hasPygments = False

import Base
import DictUtils
import Factory
from Inputs import ValueElement
from MethodUtils import CallBack


Factory = Factory.Factory("CodeDocumentation")


class CodeSnippet(Base.WebElement):
    """
        Enables adding a snippet of code directly to a page.
    """
    __slots__ = ('code', 'lexer', 'showLineNumbers', '_textNode')
    tagName = "pre"
    properties = Base.WebElement.properties.copy()
    properties['code'] = {'action':'classAttribute'}
    properties['lexer'] = {'action':'classAttribute'}
    properties['showLineNumbers'] = {'action':'classAttribute', 'type':'bool'}

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name, parent)

        self._textNode = self.addChildElement(Base.TextNode())

        self.showLineNumbers = False
        self.lexer = "python"
        self.code = ""

        self.connect("beforeToHtml", None, self, "_render")

    def _getCode(self):
        return self.code.replace("\\n", "\n")

    def _getLexer(self):
        return get_lexer_by_name(self.lexer)

    def _render(self):
        """
           Renders the code with pygments if it is available otherwise with a simple pre-tag
        """
        if not hasPygments:
            self._textNode.setText(self.code)
            return

        self._tagName = "span"
        formatter = HtmlFormatter(linenos=self.showLineNumbers)
        self._textNode.setText(highlight(self._getCode(), self._getLexer(), formatter))

Factory.addProduct(CodeSnippet)


class SourceFile(CodeSnippet):
    """
        Enables adding a formatted source file directly to a page.
    """

    def _getCode(self):
        if self.code:
            with open(self.code, "r") as openFile:
                return openFile.read()
        return ""

    def _getLexer(self):
        if self.lexer:
            return get_lexer_by_name(self.lexer)
        return get_lexer_for_filename(self.code)

Factory.addProduct(SourceFile)
