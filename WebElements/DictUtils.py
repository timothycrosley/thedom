'''
    DictUtils.py

    Utility methods and classes that provide more efficient ways of handling python dictionaries

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

from .MultiplePythonSupport import *

def missingKey(d1, d2):
    """
        Returns a list of name value pairs for all the elements that are present in one dictionary and not the other
    """
    l = []
    l += [ {k:d1[k]} for k in d1 if k not in d2 ]
    l += [ {k:d2[k]} for k in d2 if k not in d1 ]
    return l

def dictCompare(d1, d2):
    """
        Returns a list of name value pairs for all the elements that are different between the two dictionaries
    """
    diffs = missingKey(d1, d2)
    diffs += [ {k:str(d1[k]) + '->' + str(d2[k])} for k in d1 if k in d2 and d1[k] != d2[k]]
    return diffs

def userInputStrip(uDict):
    """
        Strip whitespace out of input provided by the user
    """
    dictList = map(lambda x: (x[1] and type(x[1]) == type('')) and (x[0], x[1].strip()) or (x[0], x[1]), uDict.items())
    return dict(dictList)

def setNestedValue(d, keyString, value):
    """
        Sets the value in a nested dictionary where '.' is the delimiter
    """
    keys = keyString.split('.')
    currentValue = d
    for key in keys:
        previousValue = currentValue
        currentValue = currentValue.setdefault(key, {})
    previousValue[key] = value

def getNestedValue(dictionary, keyString, default=None):
    """
        Returns the value from a nested dictionary where '.' is the delimiter
    """
    keys = keyString.split('.')
    currentValue = dictionary
    for key in keys:
        if not isinstance(currentValue, dict):
            return default
        currentValue = currentValue.get(key, None)
        if currentValue is None:
            return default

    return currentValue

def stringKeys(dictionary):
    """
        Modifies the passed in dictionary to ensure all keys are string objects, converting them when necessary.
    """
    for key, value in dictionary.items():
        if type(key) != str:
            dictionary.pop(key)
            dictionary[str(key)] = value

    return dictionary

def iterateOver(dictionary, key):
    """
        Returns a list version of the value associated with key in dictionary.
    """
    results = dictionary.get(key, [])
    if type(results) != list:
        results = [results]

    return enumerate(results)

def twoWayDict(dictionary):
    """
        Doubles the size of the dictionary, by making every reverse lookup work.
    """
    for key, value in dictionary.items():
        dictionary[value] = key

    return dictionary

class OrderedDict(dict):
    """
        Defines a dictionary which maintains order - only necessary in older versions of python.
    """
    class ItemIterator(dict):

        def __init__(self, orderedDict, includeIndex=False):
            self.orderedDict = orderedDict
            self.length = len(orderedDict)
            self.index = 0
            self.includeIndex = includeIndex

        def next(self):
            if self.index < self.length:
                key = self.orderedDict.orderedKeys[self.index]
                value = self.orderedDict[key]
                to_return = (self.includeIndex and (self.index, key, value)) or (key, value)
                self.index += 1
                return to_return
            else:
                raise StopIteration

        def __iter__(self):
            return self

    def __init__(self, tuplePairs=()):
        self.orderedKeys = []

        for key, value in tuplePairs:
            self[key] = value

    def __add__(self, value):
        if isinstance(value, OrderedDict):
            newDict = self.copy()
            newDict.update(value)
            return newDict

        return dict.__add__(self, value)

    def copy(self):
        newDict = OrderedDict()
        newDict.update(self)
        return newDict

    def update(self, dictionary):
        for key, value in iteritems(dictionary):
            self[key] = value

    def items(self):
        items = []
        for key in self.orderedKeys:
            items.append((key, self[key]))

        return items

    def values(self):
        values = []
        for key in self.orderedKeys:
            values.append(self[key])

        return values

    def keys(self):
        return self.orderedKeys

    def iterkeys(self):
        return self.orderedKeys.__iter__()

    def __iter__(self):
        return self.iterkeys()

    def iteritems(self):
        return self.ItemIterator(self)

    def iteritemsWithIndex(self):
        return self.ItemIterator(self, includeIndex=True)

    def __setitem__(self, keyString, value):
        if not keyString in self.orderedKeys:
            self.orderedKeys.append(keyString)
        return dict.__setitem__(self, keyString, value)

    def setdefault(self, keyString, value):
        if not keyString in self.orderedKeys:
            self.orderedKeys.append(keyString)
        return dict.setdefault(self, keyString, value)

def getAllNestedKeys(dictionary, prefix=""):
    """
        Returns all keys nested within nested dictionaries.
    """
    keys = []
    for key, value in iteritems(dictionary):
        if isinstance(value, dict):
            keys.extend(getAllNestedKeys(value, prefix=prefix + key + '.'))
            continue

        keys.append(prefix + key)

    return keys


class NestedDict(dict):
    """
        Defines a dictionary that enables easy safe retrieval of nested dict keys.
    """
    def __init__(self, d=None):
        if d:
            self.update(d)

    def setValue(self, keyString, value):
        """
            Sets the value of a nested dict key.
        """
        setNestedValue(self, keyString, value)

    def allKeys(self):
        """
            Returns all keys, including nested dict keys.
        """
        return getAllNestedKeys(self)

    def difference(self, otherDict):
        """
            returns a list of tuples [(key, myValue, otherDictValue),]
            allowing you to do:
                for fieldName, oldValue, newValue in oldValues.difference(newValues)
        """
        differences = []
        for key in set(self.allKeys() + otherDict.allKeys()):
            myValue = self.getValue(key, default=None)
            otherDictValue = otherDict.getValue(key, default=None)
            if myValue != otherDictValue:
                differences.append((key, myValue, otherDictValue))

        return differences


    def getValue(self, keyString, **kwargs):
        """
            Returns a nested value if it exists.
        """
        keys = keyString.split('.')
        currentNode = self
        for key in keys:
            if not key:
                continue
            currentNode = currentNode.get(key, None)
            if not currentNode:
                break

        if currentNode:
            return currentNode
        elif 'default' in kwargs:
            return kwargs.get('default')
        else:
            raise KeyError(keyString)


def createDictFromString(string, itemSeparator, keyValueSeparator, ordered=False):
    """
        Creates a new dictionary based on the passed in string, itemSeparator and keyValueSeparator.
    """
    if ordered:
        newDict = OrderedDict()
    else:
        newDict = {}
    if not string:
        return newDict
    for item in string.split(itemSeparator):
        key, value = item.split(keyValueSeparator)
        oldValue = newDict.get(key, None)
        if oldValue is not None:
            if type(oldValue) == list:
                newDict[key].append(value)
            else:
                newDict[key] = [oldValue, value]
        else:
            newDict[key] = value

    return newDict
