'''
    Dataviews.py

    Contains Elements that combine several base elements to enable complex views of data such as
    automatically building tables

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

import os

from . import Base, Buttons, Display, HiddenInputs, Inputs, Layout, UITemplate
from .Factory import Composite, Factory
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory("DataViews")


class Table(Base.WebElement):
    """
        Defines a table webelement - which is designed to be used as an actual table of data (not for alignment of
        child elements), you can quickly fill it with data, and it will take care of the display for you.
    """
    __slots__ = ('alignHeaders', 'header', 'rows', '_columns', 'columnMap', 'uniformStyle')
    tagName = "table"
    signals = Base.WebElement.signals + ['rowAdded', 'columnAdded']
    properties = Base.WebElement.properties.copy()
    properties['columns'] = {'action':'addColumns'}
    properties['rows'] = {'action':'addRows'}
    properties['border'] = {'action':'attribute'}
    properties['rules'] = {'action':'attribute'}
    properties['alignHeaders'] = {'action':'classAttribute'}
    properties['uniformStyle'] = {'action':'classAttribute'}

    class Header(Base.WebElement):
        """
            Defines a table header
        """
        __slots__ = ()
        tagName = "th"

    class Column(Base.WebElement):
        """
            Defines a table column
        """
        __slots__ = ('element', '_textNode')
        tagName = "td"
        signals = Base.WebElement.signals + ['textChanged']

        def _create(self, id=None, name=None, parent=None, **kwargs):
            Base.WebElement._create(self, id, name, parent, **kwargs)
            self.addClass((id or "").replace(" ", "") + "Column")
            self.addClass("WColumn")
            self.element = self.addChildElement(Display.FreeText())
            if self.parent and self.parent.parent and getattr(self.parent.parent, 'uniformStyle', None):
                self.setStyleFromString(self.parent.parent.uniformStyle)
            self._textNode = Base.TextNode()

        def _render(self):
            """
                Ensures that the text node is the last element upon rendering
            """
            Base.WebElement._render(self)
            self.addChildElement(self._textNode)

        def setText(self, text):
            """
                Sets the table columns visible text
            """
            if text != self._textNode.text():
                self._textNode.setText(text)
                self.emit('textChanged', text)

        def text(self):
            """
                Returns the table columns visible text
            """
            return self._textNode.text()

    class Row(Base.WebElement):
        """
            Defines a table row
        """
        __slots__ = ()
        tagName = "tr"

        def actualCell(self, columnName):
            """
                Returns the actual element that is placed within a cell
            """
            if columnName in self.parent.columns:
                columnIndex = self.parent.columns.index(columnName)
                return self.childElements[columnIndex]

        def expandColumn(self, columnName, additionalColumns=1):
            """
                Will this column of this row act like more then 1 column (removing the next column)
            """
            if columnName in self.parent.columns:
                columnIndex = self.parent.columns.index(columnName)
                self.childElements[columnIndex].attributes['colspan'] = 1 + additionalColumns
                for index in xrange(1, additionalColumns + 1):
                    self.childElements[columnIndex + index].replaceWith(Display.Empty())

        def __ensureColumn__(self, columnName):
            if not columnName in self.parent.columns:
                self.parent.addColumn(columnName)

        def cell(self, columnName):
            """
                Returns the element placed within the cell
            """
            self.__ensureColumn__(columnName)
            actualCell = self.actualCell(columnName)
            if actualCell:
                return actualCell.element

        def setCell(self, column, element):
            """
                Sets an element to be placed within the cell
            """
            self.__ensureColumn__(column)
            actualCell = self.actualCell(column)
            if actualCell:
                actualCell.element = actualCell.element.replaceWith(element)
                return element

            return False

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.WebElement._create(self, id, name, parent, **kwargs)

        header = self.Row('WTableHeader', parent=self)
        self.alignHeaders = ""
        self.header = self.addChildElement(header)
        self.rows = []
        self._columns = []
        self.columnMap = {}
        self.uniformStyle = ""
        self.addClass('GlobalTable')

        self.connect('columnAdded', None, header, 'addChildElement')

    @property
    def columns(self):
        """
            Returns the columns set on the table
        """
        return self._columns

    @columns.setter
    def columns(self, columns):
        """
            Setting columns allows you to change the ordering of columns after the fact
        """
        if set(columns) != set(self._columns):
            raise ValueError("Setting columns should only be used for reordering.")

        indexes = [self._columns.index(column) for column in columns]
        self._columns = columns

        self.header.childElements = [self.header.childElements[index] for index in indexes]
        for row in self.rows:
            row.childElements = [row.childElements[index] for index in indexes]

    def addSeparator(self, separatorName=""):
        """
            Adds a visual separator between the last row, and the next one with the given text
        """
        row = self.addChildElement(self.Row())
        column = row.addChildElement(self.Column())
        column.attributes['colspan'] = len(self._columns)
        column.addClass("WSeparator")
        column.setText(separatorName)
        return column

    def addRow(self):
        """
            Adds a new row and then returns it for manipulation
        """
        rowNumber = len(self.rows)
        row = self.addChildElement(self.Row())
        if rowNumber % 2:
            row.addClass('rowlight')
        else:
            row.addClass('rowdark')

        self.connect('columnAdded', None, row, 'addChildElement', self.Column)
        self.rows.append(row)

        for column in self._columns:
            row.addChildElement(self.Column(parent=row, id=column))

        self.emit('rowAdded', row)
        return row

    def addColumn(self, columnName, showName=True):
        """
            Adds a column to table (and therefore everyone within it)
        """
        if not columnName in self._columns:
            column = Table.Header(columnName)
            if self.fullId():
                column.addClass(self.fullId()[0].upper() + self.fullId()[1:] + columnName.replace(" ", "") + "Header")
            if self.alignHeaders:
                column.attributes['align'] = self.alignHeaders

            column.addChildElement(Base.TextNode((showName and (columnName or '')) or ''))
            self._columns.append(columnName)

            self.emit('columnAdded', column)
            self.columnMap[columnName] = column
            return column
        else:
            return self.columnMap[columnName]

    def actualCell(self, row, column):
        """
            Returns the actual cell element at row/column
        """
        if len(self.rows) >= row:
            return self.rows[row].actualCell(column)

    def cell(self, row, column):
        """
            Returns the element set at row/column
        """
        if len(self.rows) > row:
            return self.rows[row].cell(column)

    def setCell(self, row, column, element):
        """
            Sets a cell at row/column
        """
        if len(self.rows) > row:
            return self.rows[row].setCell(column, element)

        return False

    def addColumns(self, columns):
        """
            Adds a list of columns to the table
        """
        for column in columns:
            self.addColumn(column)

    def addRows(self, rows):
        """
            adds multiple rows, where the column data is defined in nested tuples
        """
        for row in rows:
            newRow = self.addRow()
            if type(row) in (list, tuple):
                for col, value in row:
                    newRow.cell(col).setText(value)
            else:
                for col, value in iteritems(row):
                    newRow.cell(col).setText(value)

    def joinRows(self, columnName, rows):
        """
            Will join a column across the given rows
        """
        row = rows.pop(0)
        row.actualCell(columnName).attributes['rowspan'] = len(rows) + 1
        for row in rows:
            row.actualCell(columnName).replaceWith(Display.Empty())

Factory.addProduct(Table)

Column = Table.Column
Row = Table.Row
Header = Table.Header


class StoredValue(Layout.Box):
    """
        Defines a label:value pair that will be passed into the request
    """
    __slots__ = ('label', 'value', 'valueDisplay')
    def _create(self, id=None, name=None, parent=None, **kwargs):
        Layout.Box._create(self, name=name + "Container", parent=parent)

        self.addClass("WStoredValue")
        label = Display.Label()
        label.setText(id + ": ")
        value = Display.Label()
        value.makeStrong()
        hiddenValue = HiddenInputs.HiddenValue(name=name)
        hiddenValue.addJavascriptEvent('onchange',
                                       "WebElements.prev(this).innerHTML = this.value;")

        hiddenValue.connect('valueChanged', None, value, 'setText')

        self.label = self.addChildElement(label)
        self.valueDisplay = self.addChildElement(value)
        self.value = self.addChildElement(hiddenValue)

Factory.addProduct(StoredValue)
