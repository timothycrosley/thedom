from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class ChartTester(ElementTester):

    def setup_class(self):
        self.element = None

    def test_loadProperties(self):
        variableDict = {'height':200,
                        'width':300,
                        'meaninglessProperty':None}

        self.element.loadFromDictionary(variableDict)

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
        print "Called"
        self.element = Factory.build("Charts.PieChart")


class TestPieChart3D(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts.PieChart3D")


class TestHorizontalBarChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts.HorizontalBarChart")


class TestVerticalBarChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts.VerticalBarChart")


class TestLineChart(ChartTester):

    def setup_class(self):
        self.element = Factory.build("Charts.LineChart")

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("GoodTests.py test_WebElement_Charts.py", shell=True).wait()
