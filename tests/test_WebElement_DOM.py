'''
    test_DOM.py

    Tests the functionality of thedom/DOM.py

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
from thedom.DOM import Factory


class TestA(ElementTester):

    def setup_class(self):
        self.element = Factory.build("a", "test")


class TestAbr(ElementTester):

    def setup_class(self):
        self.element = Factory.build("abr", "test")



class TestAddress(ElementTester):

    def setup_class(self):
        self.element = Factory.build("address", "test")


class TestArea(ElementTester):

    def setup_class(self):
        self.element = Factory.build("area", "test")


class TestBase(ElementTester):

    def setup_class(self):
        self.element = Factory.build("base", "test")


class TestBDO(ElementTester):

    def setup_class(self):
        self.element = Factory.build("bdo", "test")


class TestBlockQuote(ElementTester):

    def setup_class(self):
        self.element = Factory.build("blockquote", "test")

class TestBody(ElementTester):

    def setup_class(self):
        self.element = Factory.build("body", "test")

class TestBr(ElementTester):

    def setup_class(self):
        self.element = Factory.build("br", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestButton(ElementTester):

    def setup_class(self):
        self.element = Factory.build("button", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestCite(ElementTester):

    def setup_class(self):
        self.element = Factory.build("cite", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestCode(ElementTester):

    def setup_class(self):
        self.element = Factory.build("code", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestCol(ElementTester):

    def setup_class(self):
        self.element = Factory.build("col", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestColGroup(ElementTester):

    def setup_class(self):
        self.element = Factory.build("colgroup", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDD(ElementTester):

    def setup_class(self):
        self.element = Factory.build("col", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDel(ElementTester):

    def setup_class(self):
        self.element = Factory.build("del", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDfn(ElementTester):

    def setup_class(self):
        self.element = Factory.build("dfn", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDiv(ElementTester):

    def setup_class(self):
        self.element = Factory.build("div", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDL(ElementTester):

    def setup_class(self):
        self.element = Factory.build("dl", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDT(ElementTester):

    def setup_class(self):
        self.element = Factory.build("dt", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestEm(ElementTester):

    def setup_class(self):
        self.element = Factory.build("em", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestFieldSet(ElementTester):

    def setup_class(self):
        self.element = Factory.build("fieldset", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestForm(ElementTester):

    def setup_class(self):
        self.element = Factory.build("form", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH1(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h1", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH2(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h2", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH3(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h3", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH4(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h4", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH5(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h5", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestH6(ElementTester):

    def setup_class(self):
        self.element = Factory.build("h6", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestHead(ElementTester):

    def setup_class(self):
        self.element = Factory.build("head", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestHR(ElementTester):

    def setup_class(self):
        self.element = Factory.build("hr", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestHTML(ElementTester):

    def setup_class(self):
        self.element = Factory.build("html", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestI(ElementTester):

    def setup_class(self):
        self.element = Factory.build("i", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestIFrame(ElementTester):

    def setup_class(self):
        self.element = Factory.build("iframe", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestImg(ElementTester):

    def setup_class(self):
        self.element = Factory.build("img", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestInput(ElementTester):

    def setup_class(self):
        self.element = Factory.build("input", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestIns(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ins", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestKbd(ElementTester):

    def setup_class(self):
        self.element = Factory.build("kbd", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestLabel(ElementTester):

    def setup_class(self):
        self.element = Factory.build("kbd", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestLegend(ElementTester):

    def setup_class(self):
        self.element = Factory.build("legend", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestLI(ElementTester):

    def setup_class(self):
        self.element = Factory.build("li", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestLink(ElementTester):

    def setup_class(self):
        self.element = Factory.build("link", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestMap(ElementTester):

    def setup_class(self):
        self.element = Factory.build("map", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestMeta(ElementTester):

    def setup_class(self):
        self.element = Factory.build("meta", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestNoScript(ElementTester):

    def setup_class(self):
        self.element = Factory.build("noscript", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestObject(ElementTester):

    def setup_class(self):
        self.element = Factory.build("object", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestOL(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ol", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestOptGroup(ElementTester):

    def setup_class(self):
        self.element = Factory.build("optgroup", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestOption(ElementTester):

    def setup_class(self):
        self.element = Factory.build("option", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestP(ElementTester):

    def setup_class(self):
        self.element = Factory.build("p", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestParam(ElementTester):

    def setup_class(self):
        self.element = Factory.build("param", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == True
        assert self.element.allowsChildren == False


class TestPre(ElementTester):

    def setup_class(self):
        self.element = Factory.build("pre", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestQ(ElementTester):

    def setup_class(self):
        self.element = Factory.build("q", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSamp(ElementTester):

    def setup_class(self):
        self.element = Factory.build("samp", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestScript(ElementTester):

    def setup_class(self):
        self.element = Factory.build("script", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSelect(ElementTester):

    def setup_class(self):
        self.element = Factory.build("select", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSmall(ElementTester):

    def setup_class(self):
        self.element = Factory.build("small", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestP(ElementTester):

    def setup_class(self):
        self.element = Factory.build("p", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSpan(ElementTester):

    def setup_class(self):
        self.element = Factory.build("span", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestStrong(ElementTester):

    def setup_class(self):
        self.element = Factory.build("strong", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestStyle(ElementTester):

    def setup_class(self):
        self.element = Factory.build("style", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSub(ElementTester):

    def setup_class(self):
        self.element = Factory.build("sub", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSup(ElementTester):

    def setup_class(self):
        self.element = Factory.build("sup", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSub(ElementTester):

    def setup_class(self):
        self.element = Factory.build("sub", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTable(ElementTester):

    def setup_class(self):
        self.element = Factory.build("table", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTBody(ElementTester):

    def setup_class(self):
        self.element = Factory.build("tbody", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTD(ElementTester):

    def setup_class(self):
        self.element = Factory.build("td", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTextArea(ElementTester):

    def setup_class(self):
        self.element = Factory.build("textarea", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTFoot(ElementTester):

    def setup_class(self):
        self.element = Factory.build("tfoot", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTH(ElementTester):

    def setup_class(self):
        self.element = Factory.build("th", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTHead(ElementTester):

    def setup_class(self):
        self.element = Factory.build("thead", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTitle(ElementTester):

    def setup_class(self):
        self.element = Factory.build("title", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTR(ElementTester):

    def setup_class(self):
        self.element = Factory.build("tr", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestU(ElementTester):

    def setup_class(self):
        self.element = Factory.build("u", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestUL(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ul", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestVar(ElementTester):

    def setup_class(self):
        self.element = Factory.build("var", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestArticle(ElementTester):

    def setup_class(self):
        self.element = Factory.build("article", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestAside(ElementTester):

    def setup_class(self):
        self.element = Factory.build("aside", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestAudio(ElementTester):

    def setup_class(self):
        self.element = Factory.build("audio", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestB(ElementTester):

    def setup_class(self):
        self.element = Factory.build("b", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestBDI(ElementTester):

    def setup_class(self):
        self.element = Factory.build("bdi", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestCanvas(ElementTester):

    def setup_class(self):
        self.element = Factory.build("canvas", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == False


class TestCaption(ElementTester):

    def setup_class(self):
        self.element = Factory.build("caption", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestCommand(ElementTester):

    def setup_class(self):
        self.element = Factory.build("command", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDataList(ElementTester):

    def setup_class(self):
        self.element = Factory.build("datalist", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestDetails(ElementTester):

    def setup_class(self):
        self.element = Factory.build("details", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestEmbed(ElementTester):

    def setup_class(self):
        self.element = Factory.build("embed", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestFigCaption(ElementTester):

    def setup_class(self):
        self.element = Factory.build("figcaption", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestFigure(ElementTester):

    def setup_class(self):
        self.element = Factory.build("figure", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestFooter(ElementTester):

    def setup_class(self):
        self.element = Factory.build("footer", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestHeader(ElementTester):

    def setup_class(self):
        self.element = Factory.build("header", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestHGroup(ElementTester):

    def setup_class(self):
        self.element = Factory.build("hgroup", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestKeyGen(ElementTester):

    def setup_class(self):
        self.element = Factory.build("keygen", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestMark(ElementTester):

    def setup_class(self):
        self.element = Factory.build("mark", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestMeter(ElementTester):

    def setup_class(self):
        self.element = Factory.build("meter", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestNav(ElementTester):

    def setup_class(self):
        self.element = Factory.build("nav", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestOutput(ElementTester):

    def setup_class(self):
        self.element = Factory.build("output", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestProgress(ElementTester):

    def setup_class(self):
        self.element = Factory.build("progress", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestRP(ElementTester):

    def setup_class(self):
        self.element = Factory.build("rp", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestRT(ElementTester):

    def setup_class(self):
        self.element = Factory.build("rt", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestRuby(ElementTester):

    def setup_class(self):
        self.element = Factory.build("ruby", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestS(ElementTester):

    def setup_class(self):
        self.element = Factory.build("s", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSection(ElementTester):

    def setup_class(self):
        self.element = Factory.build("section", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSource(ElementTester):

    def setup_class(self):
        self.element = Factory.build("source", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestSummary(ElementTester):

    def setup_class(self):
        self.element = Factory.build("summary", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTime(ElementTester):

    def setup_class(self):
        self.element = Factory.build("time", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestTrack(ElementTester):

    def setup_class(self):
        self.element = Factory.build("track", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestVideo(ElementTester):

    def setup_class(self):
        self.element = Factory.build("video", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True


class TestWbr(ElementTester):

    def setup_class(self):
        self.element = Factory.build("wbr", "test")

    def test_attributes(self):
        assert self.element.tagSelfCloses == False
        assert self.element.allowsChildren == True
