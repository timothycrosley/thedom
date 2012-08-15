#!/usr/bin/python
"""
   Name:
       StringUtils.py

   Description:
   String Utils -- provides utilities for string's

"""

import random
import re
import string
import types

INVALID_CONTROL_CHARACTERS = [
    chr(0x00),
    chr(0x01),
    chr(0x02),
    chr(0x03),
    chr(0x04),
    chr(0x05),
    chr(0x06),
    chr(0x07),
    chr(0x08),
    chr(0x0b),
    chr(0x0c),
    chr(0x0e),
    chr(0x0f),
    chr(0x10),
    chr(0x11),
    chr(0x12),
    chr(0x13),
    chr(0x14),
    chr(0x15),
    chr(0x16),
    chr(0x17),
    chr(0x18),
    chr(0x19),
    chr(0x1a),
    chr(0x1b),
    chr(0x1c),
    chr(0x1d),
    chr(0x1e),
    chr(0x1f)
]

def patternSplit(text, pattern):
    """Splits a string into a list of strings at each point it matches a pattern:
        test - the text to match against
        pattern - a regex pattern to match against
    """
    matchObj = re.compile(pattern).split(text)
    tokenList = []
    for element in matchObj:
        if element != "":
            tokenList.append(element.upper())
    return tokenList


def removeAlphas(value):
    '''remove any extra formatting in a string of combined numbers and characters, returns a string'''
    newValue = ''
    for part in value:
        if part.isdigit():
            newValue += part
    return newValue


def convertIterableToString(iterable):
    newValues = []
    for item in iterable:
        item = interpretAsString(item)
        if item is not None:
            newValues.append(item)
    return ' '.join(newValues)

def convertBoolToString(boolean):
    return unicode(boolean).lower()

def convertFloatToString(value):
    return "%f%%" % (value * 100.0)

typeDict = {bool:convertBoolToString, float:convertFloatToString}
for pythonType in types.StringTypes + (types.IntType, types.LongType):
    typeDict[pythonType] = unicode
for pythonType in (types.GeneratorType, types.ListType, types.TupleType, set):
    typeDict[pythonType] = convertIterableToString

def interpretAsString(value):
    """returns a string from lists, booleans, dictionaries or a
        callbacks, or function/instance methods"""
    if value is None:
        return ''
    call = typeDict.get(type(value), None)
    if call:
        return call(value)
    elif not value:
        return None
    elif isinstance(value, dict):
        asString = ""
        for dictKey, dictValue in value.iteritems():
            dictValue = interpretAsString(dictValue)
            if dictValue is not  None:
                asString += unicode(dictKey) + ':' + dictValue + ';'
        return asString
    elif hasattr(value, "__call__"):
        return interpretAsString(value())
    elif type(value) == float:
        return "%f%%" % (value * 100.0)

    return unicode(value)

def interpretFromString(value):
    """
        returns the python equivalent value from an xml string (such as an attribute value):
            value - the html value to interpret
    """
    lowerCaseValue = value.lower()
    if lowerCaseValue == "true":
        return True
    elif lowerCaseValue == "false":
        return False
    elif lowerCaseValue == "none":
        return None

    return value

def listReplace(inString, listOfItems, replacement):
    """ Replaces instaces of items withing listOfItems with replacement:
           inString - the string to do replacements on
           listOfItems - a list of strings to replace
           replacement - what to replace it with (or a list of replacements the same lenght as the list of items)
    """
    isStringReplace = type(replacement) in types.StringTypes
    for item in listOfItems:
        if isStringReplace:
            inString = inString.replace(item, replacement)
        else:
            inString = inString.replace(item, replacement[listOfItems.index(item)])

    return inString

def removeDelimiters(inString, replacement=""):
    return listReplace(inString, ['.', ',', '+', '-', '/', '\\'], replacement)

def stripControlChars(text, fromFront=True, fromBack=True):
    """removes control characters from supplied text"""

    if not text:
        return ''

    invalidChars = ''.join(INVALID_CONTROL_CHARACTERS)
    if fromFront and fromBack:
        return text.strip(invalidChars)
    elif fromFront:
        return text.lstrip(invalidChars)
    elif fromBack:
        return text.rstrip(invalidChars)
    else:
        return text

def findIndexes(text, subString):
    """Returns a set of all indexes of subString in text"""
    indexes = set()
    lastFoundIndex = 0
    while True:
        foundIndex = text.find(subString, lastFoundIndex)
        if foundIndex == -1:
            break
        indexes.add(foundIndex)
        lastFoundIndex = foundIndex + 1
    return indexes

def encodeAnything(anything, encoding='utf8'):
    if type(anything) in types.StringTypes:
        return unicode(anything).encode(encoding)
    if isinstance(anything, list):
        for index, thing in enumerate(anything):
            anything[index] = encodeAnything(thing, encoding)
        return anything
    if isinstance(anything, dict):
        for key, thing in anything.iteritems():
            anything[key] = encodeAnything(thing, encoding)
        return anything
    if type(anything) == tuple:
        return tuple([encodeAnything(thing) for thing in anything])

    return anything

def generateRandomKey(size=20, chars=string.ascii_uppercase + string.digits):
    """
        Generates a random key of a certain length, based on a given pool of characters
        size - the lenght of the random key
        chars - the pool of characters from which to pool each item
    """
    return ''.join(random.choice(chars) for x in range(size))

def everyDirAndSub(directory):
    '''
       Splits a directory to get every directory and subdirectory as a list.
    '''
    ret = []
    idx = 0
    while True:
        try:
            idx = directory.index('/', idx + 1)
        except:
            break
        ret += [directory[:idx]]
    ret += [directory]
    return ret
