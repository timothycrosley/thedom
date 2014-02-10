'''
    CodeDocumentation.py

    Contains elements that are used for displaying and documenting code
    uses pygments to enable code highlighting

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

try:
    hasPygments = True
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
except ImportError:
    hasPygments = False

from . import Base, DictUtils, DOM, Factory
from .Inputs import ValueElement
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("CodeDocumentation")


class CodeSnippet(DOM.Pre):
    """
        Enables adding a snippet of code directly to a page.
    """
    __slots__ = ('code', 'lexer', 'showLineNumbers', '_textNode')
    tagName = "pre"
    properties = Base.WebElement.properties.copy()
    properties['code'] = {'action':'classAttribute'}
    properties['lexer'] = {'action':'classAttribute'}
    properties['showLineNumbers'] = {'action':'classAttribute', 'type':'bool'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        DOM.Pre._create(self, id, name, parent, **kwargs)

        self._textNode = self.addChildElement(Base.TextNode())

        self.showLineNumbers = False
        self.lexer = "python"
        self.code = ""

    def _getCode(self):
        return self.code.replace("\\n", "\n")

    def _getLexer(self):
        return get_lexer_by_name(self.lexer)

    def _render(self):
        """
           Renders the code with pygments if it is available otherwise with a simple pre-tag
        """
        DOM.Pre._render(self)
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
