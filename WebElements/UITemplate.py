#!/usr/bin/python
'''
   Name:
       UITemplate

   Description:
       UITemplate builds easily parsable dictionaries from User Interface Templates
'''

from xml.dom import minidom

from StringUtils import interpretFromString

def fromFile(templateFile):
    """
        Returns a parsable dictionary representation of the interface:
            templateFile - a file containing an xml representation of the interface
    """
    xmlStructure = minidom.parse(templateFile)
    return __createDictionaryFromXML(xmlStructure.childNodes[0])


def fromXML(xml):
    """
        Returns a parsable dictionary representation of the interface:
            xml - a string contianing an xml representation of the interface
    """
    xmlStructure = minidom.parseString(xml)
    return __createDictionaryFromXML(xmlStructure.childNodes[0])


def __createDictionaryFromXML(xml):
    """
        Parses an xml string converting it to an easily parseble dictionary representation:
            xml - a string containing an xml representation of the interface
    """
    if isinstance(xml, minidom.Text):
        return xml.nodeValue

    (name, attributes, children) = (xml.tagName, xml.attributes, xml.childNodes)

    dictionary = {'create':name}
    for key, value in attributes.items():
        dictionary[key] = interpretFromString(value)

    if children:
        dictionary['childElements'] = []
        for childElement in children:
            if childElement.__class__ in (minidom.Element, minidom.Text):
                dictionary['childElements'].append(__createDictionaryFromXML(childElement))

    return dictionary

