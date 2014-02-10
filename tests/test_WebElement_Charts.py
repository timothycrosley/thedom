'''
    test_Charts.py

    Tests the functionality of thedom/Charts.py

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

from test_WebElement_Base import ElementTester
from thedom.All import Factory


class ChartTester(ElementTester):

    def setup_class(self):
        self.element = None

    def test_loadProperties(self):
        variableDict = {'height':200,
                        'width':300,
                        'meaninglessProperty':None}

        self.element.setProperties(variableDict)

        assert self.element.height() == 200
        assert self.element.width() == 300


    def test_setWidth(self):
        self.element.setWidth(400)
        assert self.element.width() == 400

        self.element.setWidth(500)
        assert self.element.width() == 500

        try:
            self.element.setWidth(99999999)
            assert False
        except ValueError:
            assert True
        except:
            assert False

        assert self.element.width() == 500


    def test_setHeight(self):
        self.element.setHeight(400)
        assert self.element.height() == 400

        self.element.setHeight(500)
        assert self.element.height() == 500

        try:
            self.element.setHeight(99999999)
            assert False
        except ValueError:
            assert True
        except:
            assert False

        assert self.element.height() == 500


class TestPieChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts-PieChart")


class TestPieChart3D(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts-PieChart3D")


class TestHorizontalBarChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts-HorizontalBarChart")


class TestVerticalBarChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts-VerticalBarChart")


class TestLineChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts-LineChart")

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("py.test test_WebElement_Charts.py", shell=True).wait()
