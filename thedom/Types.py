'''
    Types.py

    Defines Node DataTypes, mainly overrides of built-ins with guaranteed HTML aware string representations
    and safety markings.

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


import cgi

from .MultiplePythonSupport import *


class WebDataType(object):
    __slots__ = ()

    def __unicode__(self):
        return cgi.escape(unicode(self))

    def __str__(self):
        return self.__unicode__()

class SafeDataType(WebDataType):
    __slots__ = ()

    def __unicode__(self):
        return unicode(self)

    def __str__(self):
        return self.__unicode__()

class Unsafe(unicode, WebDataType):
    """
        Explicitly marks a string as being unsafe so it will be cgi escaped
    """
    def __unicode__(self):
        return cgi.escape(self)

    def __str__(self):
        return self.__unicode__()

class Safe(unicode, SafeDataType):
    """
        Explicitly marks a string as safe so it will not be cgi escaped
    """
    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()

class Set(set, WebDataType):
    __slots__ = ()

    def __unicode__(self):
        return cgi.escape(" ".join(self))

    def __str__(self):
        return self.__unicode__()


class StyleDict(dict, WebDataType):
    __slots__ = ()

    def __unicode__(self):
        return cgi.escape(";".join([unicode(dictKey) + ':' + unicode(dictValue) for dictKey, dictValue in iteritems(self)]))

    def __str__(self):
        return self.__unicode__()
    
    @classmethod
    def fromString(cls, styleString):
        styleDict = cls()

        styleDefinitions = styleString.split(';')
        for definition in styleDefinitions:
            if definition:
                name, value = definition.split(':')
                styleDict[name.strip()] = value.strip()

        return styleDict


class Scripts(list, SafeDataType):
    __slots__ = ()

    def __unicode__(self):
        return ";".join([unicode(item) for item in self])

    def __str__(self):
        return self.__unicode__()


class Bool(SafeDataType):
    __slots__ = ('boolean', )

    def __init__(self, boolean):
        self.boolean = boolean

    def __nonzero__(self):
        return self.boolean

    def __unicode__(self):
        return cgi.escape(unicode(self.boolean).lower())

    def __str__(self):
        return self.__unicode__()
