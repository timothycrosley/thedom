'''
    PositionController.py

    Provides a class that isolates the logic of paging through long sets of data such as a db query

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

from .IteratorUtils import iterableLength
from .MultiplePythonSupport import *

class PositionController(object):
    """A simple way to control paging and positon within lists

        usage:
            positionController = PositionController(databaseQueryResults, startIndex, itemsPerPage)

            results = positionController.currentPageItems
            back = positionController.prevPageIndex
            next = positionController.nextPageIndex

            moreResults = positionController.areMore
            lessResults = positionController.arePrev
    """

    def __init__(self, items=[], startIndex=0, itemsPerPage=25, pagesShownAtOnce=15):
        """
            Constructs a new Position Controller Object:

            allItems = a python list, you are trying to retrieve sections from
            startIndex = where to start getting list elements from
            itemsPerPage = How many list elements to get on each page

            usage:
                positionController = PositionController(databaseQueryResults, startIndex, )
        """
        self.pagesShownAtOnce = pagesShownAtOnce
        self.allItems = items
        self.length = iterableLength(self.allItems)
        self.empty = not self.length
        self.itemsPerPage = itemsPerPage

        self.numberOfPages = self.length // self.itemsPerPage
        if self.numberOfPages < (float(self.length) // float(self.itemsPerPage)):
            self.numberOfPages += 1

        self.allPages = []
        for count in range(self.numberOfPages):
            self.allPages.append(self.pageIndex(count))

        self.lastPageIndex = 0
        if self.length > self.itemsPerPage:
            self.lastPageIndex = self.allPages[-1]

        self.setIndex(startIndex)

    def setIndex(self, index):
        """
            Sets the index to start returning results from:
                index - the offset to start at
        """
        self.startIndex = index
        if self.startIndex > self.length:
            self.startIndex = 0

        self.startPosition = self.startIndex + 1
        self.arePrev = bool(self.startPosition > 1)

        self.page = self.startIndex // self.itemsPerPage
        if self.empty:
            self.pageNumber = 0
        else:
            self.pageNumber = self.page + 1

        self.nextPageIndex = self.startIndex + self.itemsPerPage
        if self.nextPageIndex >= self.length:
            self.nextPageIndex = self.length
            self.areMore = False
        else:
            self.areMore = True

        self.currentPageItems = self.allItems[self.startIndex : self.startIndex + self.itemsPerPage]

        self.prevPageIndex = self.startPosition - (self.itemsPerPage + 1)
        if self.prevPageIndex < 0:
            self.prevPageIndex = 0

    def nextPage(self):
        """
            Selects the next available page
        """
        self.setIndex(self.nextPageIndex)

    def prevPage(self):
        """
            Selects the previouse page
        """
        self.setIndex(self.prevPageIndex)

    def setPage(self, page):
        """
            Sets the index to the start index of pageNumber
        """
        if page >= self.numberOfPages:
            page = self.numberOfPages - 1
        if page < 0:
            page = 0
        self.setIndex(self.pageIndex(page))

    def pageIndex(self, page=0):
        """
            Returns the index where a particular page starts:
                page = the page to retreive the index for
        """
        pageIndex = self.itemsPerPage * page
        if pageIndex > self.length:
            pageIndex = self.last()

        return pageIndex

    def pageList(self):
        """
            Returns a list of the pages around the current page, limited to pagesShownAtOnce
        """
        pageStart = 0

        if self.page > self.pagesShownAtOnce // 2:
            pageStart = self.page - self.pagesShownAtOnce // 2

        pageEnd = pageStart + self.pagesShownAtOnce
        if pageEnd > self.numberOfPages - 1:
            if pageEnd - pageStart >= self.numberOfPages:
                pageStart = 0
            else:
                pageStart -= pageEnd - self.numberOfPages
            pageEnd = self.numberOfPages

        return self.allPages[pageStart:pageEnd]
