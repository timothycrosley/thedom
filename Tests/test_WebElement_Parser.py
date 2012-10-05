"""
    Tests that the WebElement parser is correctly turning html in parse-able WebElements and correctly outputting
    those elements as valid well indented HTML
"""

from WebElements.Parser import WebElementTree

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
    print TREE.toHtml()
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
    output = TREE.toHtml()
    assert output == '<html><head></head><body><br /><div id="myDiv"></div></body></html>'

def test_formattedOutput():
    """
        Test that the WebElement tree correctly produces formatted (pretty) html
    """
    output = TREE.toHtml(formatted=True)
    assert output == EXPECTED_FORMATTED_OUTPUT