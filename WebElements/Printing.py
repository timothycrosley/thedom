'''
    Printing.py

    Contains Elements that make it easy to modify the printed output of a page

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

from . import Base
from . import Factory
from . import Layout
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("Printing")

class PageBreak(Layout.Box):
    """
        Defines an area where a break in the page would be logical
    """
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id=id, name=name, parent=parent)

        self.style['page-break-before'] = "always"

Factory.addProduct(PageBreak)


class UnPrintable(Layout.Box):
    """
        Defines content as being unprintable and therefore should be hidden from printing
    """
    __slots__ = ()

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box._create(self, id=id, name=name, parent=parent)

        self.addClass('hidePrint')

Factory.addProduct(UnPrintable)
