'''
    test_Parser.py

    Tests the functionality of thedom/Parser.py

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

from thedom.Parser import WebElementTree

TREE =  WebElementTree("""<html><head><body><br><div id="myDiv"></body></html>""")
EXPECTED_FORMATTED_OUTPUT = """<html>
 <head>
 </head>
 <body>
  <br />
  <div id="myDiv">
  </div>
 </body>
</html>"""

def test_tree():
    """
        Test that WebElementTree correctly produces a parse-able tree of elements
    """
    TREE.toHTML()
    assert TREE[0]._tagName == "html"
    assert TREE[0].count() == 2
    assert TREE[0][0]._tagName == "head"
    assert TREE[0][1]._tagName == "body"

    body = TREE[0][1]
    assert body.count() == 2
    assert body[0]._tagName == "br"
    assert body[0]._tagSelfCloses == True
    assert body[1]._tagName == "div"
    assert body[1]._tagSelfCloses == False
    assert body[1].id == "myDiv"

def test_condensedOutput():
    """
        Test that the WebElement tree correctly produces condensed html
    """
    output = TREE.toHTML()
    assert output == '<html><head></head><body><br /><div id="myDiv"></div></body></html>'

def test_formattedOutput():
    """
        Test that the WebElement tree correctly produces formatted (pretty) html
    """
    output = TREE.toHTML(formatted=True)
    assert output == EXPECTED_FORMATTED_OUTPUT
