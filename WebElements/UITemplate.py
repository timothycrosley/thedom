#!/usr/bin/python
'''
   Name:
       UITemplate

   Description:
       UITemplate builds easily parsable dictionaries from User Interface Templates
'''

from xml.dom import minidom

from StringUtils import interpretFromString

try:
    import shpaml
    HAS_SHPAML = True
except ImportError:
    HAS_SHPAML = False

# Supported format types
XML = 0
SHPAML = 1

def fromFile(templateFile, formatType=XML):
    """
        Returns a parsable dictionary representation of the interface:
            templateFile - a file containing an xml representation of the interface
    """
    if formatType == XML:
        return __createDictionaryFromXML(minidom.parse(templateFile).childNodes[0])
    elif formatType == SHPAML:
        with open(templateFile) as openFile:
            return fromSHPAML(openFile.read())

def fromXML(xml):
    """
        Returns a parsable dictionary representation of the interface:
            xml - a string containing an xml representation of the interface
    """
    xmlStructure = minidom.parseString(xml)
    return __createDictionaryFromXML(xmlStructure.childNodes[0])

def fromSHPAML(shpamlTemplate):
    """
        Returns a parsable dictionary representation of the interface:
            shpaml - a string containing a shpaml representation of the interface
    """
    if not HAS_SHPAML:
        raise ImportError("shpaml import not found and it is a requirement to expand shpaml templates")

    xmlStructure = minidom.parseString(shpaml.convert_text(shpamlTemplate))
    return __createDictionaryFromXML(xmlStructure.childNodes[0])

def __createDictionaryFromXML(xml):
    """
        Parses an xml string converting it to an easily parseble dictionary representation:
            xml - a string containing an xml representation of the interface
    """
    if isinstance(xml, minidom.Text):
        return xml.nodeValue.strip()

    (name, attributes, children) = (xml.tagName, xml.attributes, xml.childNodes)

    dictionary = {'create':name}
    for key, value in attributes.items():
        dictionary[key] = interpretFromString(value)

    if children:
        dictionary['childElements'] = []
        for childElement in children:
            if childElement.__class__ in (minidom.Element, minidom.Text):
                newElement = __createDictionaryFromXML(childElement)
                if newElement:
                    dictionary['childElements'].append(newElement)

    return dictionary

