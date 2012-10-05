from WebElements.IteratorUtils import IterableCollection, Queryable, SortedSet

def test_iterableCollection():
    """Test basic functionality of iterable collection works as expected"""
    collection = IterableCollection()
    tims = collection.extend(['Crosley', 'Savannah'], "Timothy")
    ryans = collection.extend(['Scaife'], "Ryan")
    garys = collection.extend(['Cusimano', 'Gambarani'], "Gary")

    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Ryan', 'Scaife'),
                             ('Gary', 'Cusimano'),
                             ('Gary', 'Gambarani')]

    tims.append('Fritz')
    ryans.append('Frankhouser')
    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Timothy', 'Fritz'),
                             ('Ryan', 'Scaife'),
                             ('Ryan', 'Frankhouser'),
                             ('Gary', 'Cusimano'),
                             ('Gary', 'Gambarani')]

    assert collection[1:6] == [('Timothy', 'Savannah'),
                               ('Timothy', 'Fritz'),
                               ('Ryan', 'Scaife'),
                               ('Ryan', 'Frankhouser'),
                               ('Gary', 'Cusimano')]

    assert collection.pop() == ('Gary', 'Gambarani')
    assert collection[:] == [('Timothy', 'Crosley'),
                             ('Timothy', 'Savannah'),
                             ('Timothy', 'Fritz'),
                             ('Ryan', 'Scaife'),
                             ('Ryan', 'Frankhouser'),
                             ('Gary', 'Cusimano')]

    for first, last in collection:
        assert first and last

    looped = 0
    for first, last in collection.islice()[1:3]:
        assert first and last
        looped += 1

    assert looped == 2

def test_sortedSet():
    mySortedSet = SortedSet([4, 1, 5, 2, 3])
    assert mySortedSet[:] == [4, 1, 5, 2, 3]
    mySortedSet.add(4)
    assert mySortedSet[:] == [4, 1, 5, 2, 3]
    mySortedSet.add(6)
    assert mySortedSet[:] == [4, 1, 5, 2, 3, 6]
    assert mySortedSet[0] == 4
    assert mySortedSet[1] == 1
    assert mySortedSet[2] == 5
    assert mySortedSet[3] == 2
    assert mySortedSet[4] == 3
    assert mySortedSet[5] == 6

def test_Queryable():
    queryable = Queryable(['a', 'b'])
    assert queryable.count() == 2
    assert queryable.__lowerStrings__('hi there') == 'hi there'
    assert queryable.__lowerStrings__('Hi There') == 'hi there'
    assert queryable.__lowerStrings__('HI THERE') == 'hi there'
    assert queryable.__lowerStrings__(u'hi there') == u'hi there'
    assert queryable.__lowerStrings__(u'Hi There') == u'hi there'
    assert queryable.__lowerStrings__(u'HI THERE') == u'hi there'
    assert queryable.__lowerStrings__(57) == 57

