'''
    test_DictUtils.py

    Tests the functionality of WebElements/DictUtils.py

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

from WebElements import DictUtils

class TestDictUtilsTest(object):
    def __init__(self, needsdb=1, db=None):
        pass

    def test_MissingKey(self):
        assert (DictUtils.missingKey({}, {})  ==  [])
        assert (DictUtils.missingKey({'A':'1'}, {'A':'1'})  ==  [])
        assert (DictUtils.missingKey({'A':'1'}, {})  ==  [{'A':'1'}])
        assert (DictUtils.missingKey({}, {'A':'1'})  ==  [{'A':'1'}])

    def test_DictCompare(self):
        assert (DictUtils.dictCompare({}, {})  ==  [])
        assert (DictUtils.dictCompare({'A':'1'}, {'A':'1'})  ==  [])
        assert (DictUtils.dictCompare({'A':'1'}, {})  ==  [{'A':'1'}])
        assert (DictUtils.dictCompare({}, {'A':'1'})  ==  [{'A':'1'}])
        assert (DictUtils.dictCompare({'A':'0'}, {'A':'1'})  ==  [{'A':'0->1'}])
        assert (DictUtils.dictCompare({'A':'0', 'B':'2'}, {'A':'1'})  ==  [{'B':'2'}, {'A':'0->1'}])
        assert (DictUtils.dictCompare({'A':'0'}, {'A':'1', 'B':'2'})  ==  [{'B':'2'}, {'A':'0->1'}])

    def test_UserInputStrip(self):
        assert (DictUtils.userInputStrip({})  ==  {})
        assert (DictUtils.userInputStrip({'a':' b '})  ==  {'a':'b'})
        assert (DictUtils.userInputStrip({'a':None})  ==  {'a':None})
        assert (DictUtils.userInputStrip({'a':1})  ==  {'a':1})
        assert (DictUtils.userInputStrip({'a':[' beta ']})  ==  {'a':[' beta ']})

    def test_SetNestedValue(self):
        d = {}
        DictUtils.setNestedValue(d, 'hello', 'world')
        assert (d ==  {'hello':'world'})
        d = {'hello':'goodbye'}
        assert (d ==  {'hello':'goodbye'})
        DictUtils.setNestedValue(d, 'hello', 'world')
        assert (d ==  {'hello':'world'})
        d = {}
        DictUtils.setNestedValue(d, 'hello.there', 'world')
        assert (d ==  {'hello':{'there':'world'}})
        d = {'hello':{'there':'goodbye'}}
        assert (d ==  {'hello':{'there':'goodbye'}})
        DictUtils.setNestedValue(d, 'hello.there', 'world')
        assert (d ==  {'hello':{'there':'world'}})

    def test_GetNestedValue(self):
        d = {}
        assert (DictUtils.getNestedValue(d, 'hello')  ==  None)
        d = {'hello':{'there':'goodbye'}}
        assert (DictUtils.getNestedValue(d, 'hello')  ==  {'there':'goodbye'})
        assert (DictUtils.getNestedValue(d, 'hello.there')  ==  'goodbye')

    def test_createDictFromString(self):
        string = "hello[-EQUALS-]goodbye[-AND-]monkey[-EQUALS-]tim[-AND-]tim[-EQUALS-]monkey"
        assert (DictUtils.createDictFromString(string, '[-AND-]', '[-EQUALS-]') ==
                {'hello':'goodbye', 'monkey':'tim', 'tim':'monkey'})

    def test_NestedDict(self):
        nd = DictUtils.NestedDict()
        assert (nd !=  None)
        assert (nd.keys()  ==  [])
        nd.setValue('hello', 'world')
        assert (nd.keys()  ==  ['hello'])
        assert (nd['hello'] ==  'world')
        assert (nd.getValue('hello')  ==  'world')
        assert ( nd.getValue !=  'jello')
        assert (nd.getValue('jello', default='yellow')  ==  'yellow')
        nd = DictUtils.NestedDict()
        assert (nd !=  None)
        nd.setValue('hello.there', 'world')
        assert (nd.keys()  ==  ['hello'])
        assert (nd['hello'] ==  {'there':'world'})
        assert (nd.getValue('hello')  ==  {'there':'world'})
        assert (nd.getValue('hello.there')  ==  'world')
        assert ( nd.getValue !=  'hello.bear')
        assert (nd.getValue('hello.bear', default='grizzly')  ==  'grizzly')
        nd = DictUtils.NestedDict({})
        assert (nd !=  None)
        assert (nd.keys()  ==  [])
        nd = DictUtils.NestedDict({'alpha':'beta'})
        assert (nd.keys()  ==  ['alpha'])
        assert (nd.getValue('alpha')  ==  'beta')
        nd = DictUtils.NestedDict({'alpha':{'beta':'gamma'}})
        assert (nd.keys()  ==  ['alpha'])
        assert (nd.getValue('alpha')  ==  {'beta':'gamma'})
        assert (nd.getValue('alpha.beta')  ==  'gamma')

        #test difference
        myNestedDict = DictUtils.NestedDict()
        myNestedDict.setValue("dude.1.name", "Tim")
        myNestedDict.setValue("dude.2.name", "Tim2")
        myNestedDict.setValue("dude.3.name", "Mike")
        myNestedDict.setValue("dude.1.type", "Monkey")
        myNestedDict.setValue("dudette.1.name", "Susan")
        myNestedDict.setValue("dudette.2.name", "Karen")

        myNestedDict2 = DictUtils.NestedDict()
        myNestedDict2.setValue("dude.1.name", "Mike")
        myNestedDict2.setValue("dude.2.name", "Tim2")
        myNestedDict2.setValue("dude.3.name", "Tim")
        myNestedDict2.setValue("dude.3.type", "Monkey")
        myNestedDict2.setValue("dudette.1.name", "Susan")
        myNestedDict2.setValue("dudette.2.name", "Stella")

        assert myNestedDict.allKeys() == ['dudette.1.name', 'dudette.2.name', 'dude.1.type',
                                          'dude.1.name', 'dude.3.name', 'dude.2.name']
        assert myNestedDict2.allKeys() == ['dudette.1.name', 'dudette.2.name', 'dude.1.name',
                                           'dude.3.type', 'dude.3.name', 'dude.2.name']
        assert myNestedDict.difference(myNestedDict2) == [('dudette.2.name', 'Karen', 'Stella'),
                                                          ('dude.1.type', 'Monkey', None),
                                                          ('dude.1.name', 'Tim', 'Mike'),
                                                          ('dude.3.type', None, 'Monkey'),
                                                          ('dude.3.name', 'Mike', 'Tim')]
