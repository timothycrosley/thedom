#!/usr/bin/python
"""
   Name:
       Printing

   Description:
       Contains Elements that make it easy to modify the printing output of a page

"""

import Base
import Factory
import Layout
from MethodUtils import CallBack

Factory = Factory.Factory("Printing")

class PageBreak(Layout.Box):
    """
        Defines an area where a break in the page would be logical
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id=id, name=name, parent=parent)

        self.style['page-break-before'] = "always"

Factory.addProduct(PageBreak)


class UnPrintable(Layout.Box):
    """
        Defines content as being unprintable and therefore should be hidden from printing
    """
    __slots__ = ()

    def __init__(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box.__init__(self, id=id, name=name, parent=parent)

        self.addClass('hidePrint')

Factory.addProduct(UnPrintable)
