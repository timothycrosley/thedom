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
        Will force a page break before printing any additional elements
    """
    def __init__(self, id=None, name=None, parent=None):
        Layout.Box.__init__(self, id=id, name=name, parent=parent)

        self.style['page-break-before'] = "always"

Factory.addProduct(PageBreak)


class HidePrint(Layout.Box):
    """
        Will hide any child elements from printing
    """
    def __init__(self, id=None, name=None, parent=None):
        Layout.Box.__init__(self, id=id, name=name, parent=parent)

        self.addClass('hidePrint')

Factory.addProduct(HidePrint)
