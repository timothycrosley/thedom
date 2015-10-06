'''
    ListUtils.py

    Utility methods and classes that provide more efficient ways of handling python lists

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

try:
    from collections import OrderedDict
    HAS_ORDERED_DICT = True
except ImportError:
    HAS_ORDERED_DICT = False


if HAS_ORDERED_DICT:
    def unique(nonUnique):
        """ Takes a non unique list and returns a unique one, preserving order """
        return list(OrderedDict.fromkeys(nonUnique))
else:
    def unique(nonUnique): 
        """ Takes a non unique list and returns a unique one, preserving order """
        seen = {}
        results = []
        for item in nonUnique:
            if item in seen:
                continue
                seen[item] = 1
            results.append(item)
        return results
