'''
    test_UITemplate.py

    Tests the functionality of thedom/UITemplate.py

    Copyright (C) 2015  Timothy Edmund Crosley

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

from thedom import UITemplate

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
