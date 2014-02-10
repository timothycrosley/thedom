'''
    Charts.py

    Contains elements that utilize the google charts public API to produce charts based on common data

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

from . import Base, Factory
from .Display import Image
from .MultiplePythonSupport import *

Factory = Factory.Factory("Charts")


class GoogleChart(Image):
    """
        Provides a way for the google chart api to be used via WebElements
    """
    __slots__ = ('__dataPoints__', '__height__', '__width__')
    chartType = None
    url = ('http://chart.apis.google.com/chart?cht='
           '%(chart)s&chs=%(width)sx%(height)s&chd=t:%(data)s&chl=%(labels)s&chbh=a'
           '&chxt=y&chds=0,%(max)f&chxr=0,0,%(max)f&chco=4D89F9')
    properties = Image.properties.copy()
    properties['height'] = {'action':'setHeight', 'type':'int'}
    properties['width'] = {'action':'setWidth', 'type':'int'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Image._create(self, id, name, parent)
        self.__dataPoints__ = {}
        self.__height__ = 100
        self.__width__ = 100

    def setWidth(self, width):
        """
            Set the width of the google chart in pixels (maximum allowed by google is 1000 pixels)
        """
        width = int(width)
        if width > 1000:
            raise ValueError("Google charts has a maximum width limit of 1000 pixels")
        self.__width__ = width

    def width(self):
        """
            Returns the set width of the google chart in pixels
        """
        return self.__width__

    def setHeight(self, height):
        """
            Set the height of the google chart in pixels (maximum allowed by google is 1000 pixels)
        """
        height = int(height)
        if height > 1000:
            raise ValueError("Google charts has a maximum height limit of 1000 pixels")
        self.__height__ = height

    def height(self):
        """
            Returns the set height of the google chart in pixels
        """
        return self.__height__

    def addData(self, label, value):
        """
            Adds a data point to the chart,
                  label: the label to associate with the data point
                  value: the numeric value of the data
        """
        self.__dataPoints__[str(label)] = value

    def _render(self):
        Image._render(self)

        # Update Source data
        data = self.__dataPoints__ or {'No Data!':'100'}
        self.style['width'] = self.__width__

        items = []
        for key, value in iteritems(data):
            items.append((value, key))
        items.sort()
        keys = [key for value, key in items]
        values = [value for value, key in items]

        self.style['height'] = self.__height__
        self.setProperty('src', self.getURL(keys, values))

    def getURL(self, keys, values):
        """
            Returns the google chart url based on the data points given
        """
        return self.url % {'chart':self.chartType, 'width':str(self.__width__),
                           'height':str(self.__height__),
                           'data':",".join([str(value) for value in values]),
                           'labels':"|".join(keys),
                           'max':float(max(values)),
                           }


class PieChart(GoogleChart):
    """
        Implementation of Google's pie chart
    """
    __slots__ = ()
    chartType = "p"

Factory.addProduct(PieChart)


class PieChart3D(GoogleChart):
    """
        Implementation of Google's 3d pie chart
    """
    __slots__ = ()
    chartType = "p3"

Factory.addProduct(PieChart3D)


class HorizontalBarChart(GoogleChart):
    """
        Implementation of Googles Horizontal Bar Chart
    """
    __slots__ = ()
    chartType = "bhs"
    url = ('http://chart.apis.google.com/chart?cht='
           '%(chart)s&chs=%(width)sx%(height)s&chd=t:%(data)s&chxl=1:|%(labels)s&chbh=a'
           '&chxt=x,y&chds=0,%(max)f&chxr=0,0,%(max)f&chco=4D89F9')

    def getURL(self, keys, values):
        """
            Returns the google chart url based on the data points given
        """
        return self.url % {'chart':self.chartType, 'width':str(self.__width__),
                           'height':str(self.__height__),
                           'data':",".join([str(value) for value in values]),
                           'labels':"|".join(reversed(keys)),
                           'max':float(max(values)),
                           }

Factory.addProduct(HorizontalBarChart)


class VerticalBarChart(GoogleChart):
    """
        Implementation of Google's Vertical Bar Chart
    """
    __slots__ = ()
    chartType = "bvs"

Factory.addProduct(VerticalBarChart)


class LineChart(GoogleChart):
    """
        Implementation of Google's Line Chart
    """
    __slots__ = ()
    chartType = "lc"

Factory.addProduct(LineChart)
