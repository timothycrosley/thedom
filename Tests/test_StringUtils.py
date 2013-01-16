'''
    test_StringUtils.py

    Tests the functionality of WebElements/StringUtils.py

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

from WebElements import StringUtils
from WebElements.MultiplePythonSupport import *

def test_removeAlphas():
    """ Ensure that the utility function to remove alpha characters works successfully """
    assert StringUtils.removeAlphas('afjsafdl121323213adfas1231321') == "1213232131231321"
    assert StringUtils.removeAlphas('213123123123231') == "213123123123231"


def test_interpretAsString():
    """Ensure the interpret as string utility function correctly takes objects and turns them into
       strings
    """
    testList = ['1a', '2b', '3c', '4d']
    assert StringUtils.interpretAsString(testList) == "1a 2b 3c 4d"

    testTuple = ('1a', '2b', '3c', '4d')
    assert StringUtils.interpretAsString(testTuple) == "1a 2b 3c 4d"

    testDictionary = {1:'a', 2:'b', 3:'c', 4:'d'}
    assert StringUtils.interpretAsString(testDictionary) == "1:a;2:b;3:c;4:d;"

    testBoolean = True
    assert StringUtils.interpretAsString(testBoolean) == "true"

    testBoolean = False
    assert StringUtils.interpretAsString(testBoolean) == "false"

    testFloat = 1.0 / 4.0
    assert StringUtils.interpretAsString(testFloat) == "25.000000%"

    def testFunction():
        return "hello"
    assert StringUtils.interpretAsString(testFunction) == "hello"

    assert StringUtils.interpretAsString("") == u("")

def test_interpretFromString():
    """Ensure the interpret from string utility method correctly takes strings and turns them into
       objects
    """
    assert StringUtils.interpretFromString("True") == True
    assert StringUtils.interpretFromString("trUE") == True

    assert StringUtils.interpretFromString("False") == False
    assert StringUtils.interpretFromString("fAlSe") == False

    assert StringUtils.interpretFromString("None") == None
    assert StringUtils.interpretFromString("NOnE") == None

    assert StringUtils.interpretFromString("Some other value") == "Some other value"

def test_stripControlChars():
    """Ensure we properly remove control characters (not including \r\n\t"""
    controlCharText = ''.join(StringUtils.INVALID_CONTROL_CHARACTERS) + \
                      "THE STRING" + ''.join(StringUtils.INVALID_CONTROL_CHARACTERS)
    assert StringUtils.stripControlChars(controlCharText) == "THE STRING"
    assert StringUtils.stripControlChars(controlCharText, fromFront=False) == \
              ''.join(StringUtils.INVALID_CONTROL_CHARACTERS) + "THE STRING"
    assert StringUtils.stripControlChars(controlCharText, fromBack=False) == \
              "THE STRING" + ''.join(StringUtils.INVALID_CONTROL_CHARACTERS)
    assert StringUtils.stripControlChars(controlCharText, fromFront=False, fromBack=False) == \
              ''.join(StringUtils.INVALID_CONTROL_CHARACTERS) + "THE STRING" + \
              ''.join(StringUtils.INVALID_CONTROL_CHARACTERS)

def test_listReplace():
    """Ensure replacing a list of items from a string works correctly"""
    myString = "A string of text"
    assert StringUtils.listReplace(myString, ['A', 'text', 'string'], "AHH") == "AHH AHH of AHH"
    assert StringUtils.listReplace(myString, ['A', 'text', 'string'], ["1", "2", "3"]) == "1 3 of 2"

def test_removeDelimiters():
    """Ensure removing delimeters works correctly"""
    string = "Th.is, shou+ld wo-rk /I thi\\nk"
    assert StringUtils.removeDelimiters(string) == "This should work I think"
    assert StringUtils.removeDelimiters(string, replacement=" ") == "Th is  shou ld wo rk  I thi nk"

def test_findIndexes():
    string = "There is an A here and an A here there is an A everywhere"
    assert StringUtils.findIndexes(string, "A") == set((12, 26, 45))
    assert StringUtils.findIndexes(string, "is an") == set((6, 39))
    assert StringUtils.findIndexes(string, "monkey") == set()

def test_generateRandomKey():
    randomKey1 = StringUtils.generateRandomKey()
    randomKey2 = StringUtils.generateRandomKey()
    assert randomKey1 != randomKey2
    assert len(randomKey1) == len(randomKey2) == 20

    randomKey1 = StringUtils.generateRandomKey(40)
    randomKey2 = StringUtils.generateRandomKey(40)
    assert randomKey1 != randomKey2
    assert len(randomKey1) == len(randomKey2) == 40

