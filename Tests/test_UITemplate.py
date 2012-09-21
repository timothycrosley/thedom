'''
    Test UITemplate correctly builds parseble interface structures
'''

from WebElements import UITemplate

EXPECTED_STRUCTURE = {'childElements': [
                        {'childElements':
                            [{'create': u'childishchildelement'}],
                              'create': u'childelement',
                              u'id': u'SomeRandomeId',
                              u'name': u'SomeRandomeName'}],
                        'create': u'container',
                        u'randomattribute': u'Hello'}

def test_fromFile():
    """
        Ensure UITemplate creates a dictionary structure from an XML File correctly
    """
    assert UITemplate.fromFile("testTemplate.xml") == EXPECTED_STRUCTURE #xml template file
    assert UITemplate.fromFile("testTemplate.shpaml", formatType=UITemplate.SHPAML) == EXPECTED_STRUCTURE #

def test_fromXML():
    """
        Ensure UITemplate creates a dictionary structure from XML correctly
    """
    xml = """<container randomattribute="Hello">
                <childelement id="SomeRandomeId" name="SomeRandomeName">
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
                childelement#SomeRandomeId name=SomeRandomeName
                    > childishchildelement
             """

    assert UITemplate.fromSHPAML(shpmal) == EXPECTED_STRUCTURE


