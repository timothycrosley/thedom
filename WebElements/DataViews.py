#!/usr/bin/python
"""
   Name:
       Dataviews

   Description:
       Widgets that allow you to view data

"""

import os

import Base
import Buttons
import Display
import HiddenInputs
import Inputs
import Layout
import UITemplate
from Factory import Composite, Factory
from MethodUtils import CallBack

Factory = Factory("DataViews")


class Table(Base.WebElement):
    """
        Defines a table webelement - which is designed to be used as an actual table of data (not for alignment of
        child elements), you can quickly fill it with data, and it will take care of the display for you.
    """
    __slots__ = ('alignHeaders', 'header', 'rows', 'columns', 'columnMap', 'uniformStyle')
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
            self.connect("rendering", None, self, "addChildElement", self._textNode)

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
        self.columns = []
        self.columnMap = {}
        self.uniformStyle = ""
        self.addClass('GlobalTable')

        self.connect('columnAdded', None, header, 'addChildElement')

    def addSeparator(self, separatorName=""):
        """
            Adds a visual separator between the last row, and the next one with the given text
        """
        row = self.addChildElement(self.Row())
        column = row.addChildElement(self.Column())
        column.attributes['colspan'] = len(self.columns)
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

        for column in self.columns:
            row.addChildElement(self.Column(parent=row, id=column))

        self.emit('rowAdded', row)
        return row

    def addColumn(self, columnName, showName=True):
        """
            Adds a column to table (and therefore everyone within it)
        """
        if not columnName in self.columns:
            column = Table.Header(columnName)
            if self.fullId():
                column.addClass(self.fullId()[0].upper() + self.fullId()[1:] + columnName.replace(" ", "") + "Header")
            if self.alignHeaders:
                column.attributes['align'] = self.alignHeaders

            column.addChildElement(Base.TextNode((showName and (columnName or '')) or ''))
            self.columns.append(columnName)

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
            return self.rows[row].setCell(column)

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
            for col, value in row.iteritems():
                self.setCell(newRow, col, value)

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
