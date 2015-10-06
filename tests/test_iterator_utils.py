'''
    test_IteratorUtils.py

    Tests the functionality of thedom/IteratorUtils.py

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

from thedom.IteratorUtils import IterableCollection, Queryable, SortedSet
from thedom.MultiplePythonSupport import *


def test_iterableCollection():
    """Test basic functionality of iterable collection works as expected"""
    collection = IterableCollection()
    tims = collection.extend(['Crosley', 'Savannah'], "Timothy")
    ryans = collection.extend(['Scaife'], "Ryan")
    garys = collection.extend(['Cusimano', 'Gambarani'], "Gary")

    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Ryan', 'Scaife'),
                             ('Gary', 'Cusimano'),
                             ('Gary', 'Gambarani')]

    tims.append('Fritz')
    ryans.append('Frankhouser')
    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Timothy', 'Fritz'),
                             ('Ryan', 'Scaife'),
                             ('Ryan', 'Frankhouser'),
                             ('Gary', 'Cusimano'),
                             ('Gary', 'Gambarani')]

    assert collection[1:6] == [('Timothy', 'Savannah'),
                               ('Timothy', 'Fritz'),
                               ('Ryan', 'Scaife'),
                               ('Ryan', 'Frankhouser'),
                               ('Gary', 'Cusimano')]

    assert collection.pop() == ('Gary', 'Gambarani')
    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Timothy', 'Fritz'),
                             ('Ryan', 'Scaife'),
                             ('Ryan', 'Frankhouser'),
                             ('Gary', 'Cusimano')]

    for first, last in collection:
        assert first and last

    looped = 0
    for first, last in collection.islice()[1:3]:
        assert first and last
        looped += 1

    assert looped == 2

def test_sortedSet():
    mySortedSet = SortedSet([4, 1, 5, 2, 3])
    assert mySortedSet[:] == [4, 1, 5, 2, 3]
    mySortedSet.add(4)
    assert mySortedSet[:] == [4, 1, 5, 2, 3]
    mySortedSet.add(6)
    assert mySortedSet[:] == [4, 1, 5, 2, 3, 6]
    assert mySortedSet[0] == 4
    assert mySortedSet[1] == 1
    assert mySortedSet[2] == 5
    assert mySortedSet[3] == 2
    assert mySortedSet[4] == 3
    assert mySortedSet[5] == 6

def test_Queryable():
    queryable = Queryable(['a', 'b'])
    assert queryable.count() == 2
    assert queryable.__lowerStrings__('hi there') == 'hi there'
    assert queryable.__lowerStrings__('Hi There') == 'hi there'
    assert queryable.__lowerStrings__('HI THERE') == 'hi there'
    assert queryable.__lowerStrings__(u('hi there')) == u('hi there')
    assert queryable.__lowerStrings__(u('Hi There')) == u('hi there')
    assert queryable.__lowerStrings__(u('HI THERE')) == u('hi there')
    assert queryable.__lowerStrings__(57) == 57
