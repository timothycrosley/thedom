'''
    Test UITemplate correctly builds python parse-able interface structures
'''

from WebElements import UITemplate

EXPECTED_STRUCTURE = UITemplate.Template('container', properties=(("randomattribute", "Hello"),),
                                         childElements=(
                                           UITemplate.Template('childelement', id="SomeRandomId", name="SomeRandomName",
                                                                childElements=(
                                                                    UITemplate.Template("childishchildelement"),
                                                            )),))

def test_fromFile():
    """
        Ensure UITemplate creates a dictionary structure from an XML File correctly
    """
    assert UITemplate.fromFile("testTemplate.xml", formatType=UITemplate.XML) == EXPECTED_STRUCTURE #xml file
    assert UITemplate.fromFile("testTemplate.shpaml", formatType=UITemplate.SHPAML) == EXPECTED_STRUCTURE #shpaml file

def test_fromXML():
    """
        Ensure UITemplate creates a dictionary structure from XML correctly
    """
    xml = """<container randomattribute="Hello">
                <childelement id="SomeRandomId" name="SomeRandomName">
                    <childishchildelement />
                </childelement>
             </container>"""

    assert UITemplate.fromXML(xml) == EXPECTED_STRUCTURE

def test_fromSHPAML():
    """
        Ensure UITemplate creates a dictionary structure from SHPAML correctly
    """
    shpmal = """
             container randomattribute=Hello
                childelement#SomeRandomId name=SomeRandomName
                    > childishchildelement
             """

    assert UITemplate.fromSHPAML(shpmal) == EXPECTED_STRUCTURE


