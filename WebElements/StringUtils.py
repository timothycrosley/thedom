'''
    StringUtils.py

    Provides methods that ease complex python string operations

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

import random
import re
import string
import types
from urllib import urlencode

from .MultiplePythonSupport import *
from . import ClientSide

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
    """
        Splits a string into a list of strings at each point it matches a pattern:
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
    """
        Returns a string removed of any extra formatting in the string or combined numbers and characters.
    """
    newValue = ''
    for part in value:
        if part.isdigit():
            newValue += part
    return newValue

def convertIterableToString(iterable):
    """
        Returns a string representation of an iterable value.
    """
    return ' '.join([interpretAsString(item) or '' for item in iterable])

def convertBoolToString(boolean):
    """
        Returns a string representation of a boolean value.
    """
    return unicode(boolean).lower()

def convertFloatToString(value):
    """
        Returns a string representation of a float value.
    """
    return "%f%%" % (value * 100.0)

typeDict = {bool:convertBoolToString, float:convertFloatToString}
for pythonType in (str, unicode) + (int, long):
    typeDict[pythonType] = unicode
for pythonType in (types.GeneratorType, list, tuple, set):
    typeDict[pythonType] = convertIterableToString

getTypeDict = typeDict.get

def interpretAsString(value):
    """
        returns a string from lists, booleans, dictionaries or a
        callbacks, or function/instance methods
    """
    if value is None:
        return ''
    call = getTypeDict(type(value), None)
    if call:
        return call(value)
    elif not value:
        return None
    elif isinstance(value, dict):
        asString = ""
        for dictKey, dictValue in iteritems(value):
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
    """
        Replaces instaces of items withing listOfItems with replacement:
           inString - the string to do replacements on
           listOfItems - a list of strings to replace
           replacement - what to replace it with (or a list of replacements the same lenght as the list of items)
    """
    isStringReplace = type(replacement) in (str, unicode)
    for item in listOfItems:
        if isStringReplace:
            inString = inString.replace(item, replacement)
        else:
            inString = inString.replace(item, replacement[listOfItems.index(item)])

    return inString

def removeDelimiters(inString, replacement=""):
    """
        Removes the specified delimiters from the inString.
    """
    return listReplace(inString, ['.', ',', '+', '-', '/', '\\'], replacement)

def stripControlChars(text, fromFront=True, fromBack=True):
    """
        Removes control characters from supplied text.
    """
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
    """
        Returns a set of all indexes of subString in text.
    """
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
    """
        Returns any data that is passed in encoded into the specified encoding or throws an exception.
    """
    if type(anything) in (str, unicode):
        return unicode(anything).encode(encoding)
    if isinstance(anything, list):
        for index, thing in enumerate(anything):
            anything[index] = encodeAnything(thing, encoding)
        return anything
    if isinstance(anything, dict):
        for key, thing in iteritems(anything):
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
    """
       Splits a directory to get every directory and subdirectory as a list.
    """
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

def scriptURL(argumentDictionary):
    """
        Encodes a dictionary into a URL, while allowing scripts to be ran to form the URL client side
    """
    scriptParams = []
    for argumentName, argumentValue in argumentDictionary.items():
        if isinstance(argumentValue, ClientSide.Script):
            argumentDictionary.pop(argumentName)
            scriptParams.append('%s=" + %s' % (argumentName, argumentValue.claim()))
    if not scriptParams:
        return urlencode(argumentDictionary)
    elif argumentDictionary:
        scriptParams += urlencode(argumentDictionary)

    urlScript = ' + "'.join(scriptParams)
    if not argumentDictionary:
        urlScript = '"' + urlScript

    return ClientSide.Script(urlScript)
