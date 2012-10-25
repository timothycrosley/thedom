"""
    Classes/functions that provide additional iterator functionality beyond what is provided by the
    standard libary.
"""

import time
import types

from DictUtils import OrderedDict

ITERATOR_TYPES = (types.GeneratorType, types.ListType, types.TupleType, set)

def iterableLength(iterable):
    if type(iterable) not in ITERATOR_TYPES and getattr(iterable, 'count'):
        return iterable.count()
    else:
        return len(iterable)

class IndexIterator(object):
    """ Simple index based iterator (you give the start and end index, and the indexable item) """
    def __init__(self, iteratorSlice, start, end):
        self.iteratorSlice = iteratorSlice
        self.end = end
        self.index = start

    def next(self):
        if self.index < self.end:
            value = self.iteratorSlice[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

    def __iter__(self):
        return self


class PopIterator(object):
    """ Queue processing based off poping from a list """
    def __init__(self, popable, interval=1):
        self.popable = popable
        self.interval = interval

    def __getValue__(self):
        try:
            return self.popable.pop()
        except IndexError:
            return None

    def next(self):
        value = self.__getValue__()
        while not value:
            time.sleep(self.interval)
            value = self.__getValue__()

        return value

    def __iter__(self):
        return self


class IteratorSlice(object):
    """ Allows you to iterate through a section of an indexable iterable without creating a new list
        or having step through every item till the start index (like islice does) """
    def __init__(self, iterable):
        self.iterable = iterable

    def __getitem__(self, index):
        if type(index) == slice:
            (start, end) = (index.start or 0, index.stop or len(self.iterable))
            if start < 0:
                start = 0
            if end > len(self.iterable):
                end = len(self.iterable)

            return IndexIterator(self, start, end)
        else:
            return self.iterable[index]


class IterableCollection(object):
    """ Provides a way to iterate through a collection of lists as if it where one really big list """

    def __init__(self, iterableDictionary=None):
        self.iterableItems = []
        self.identifiers = []
        if iterableDictionary:
            for identifier, iterableItem in iterableDictionary.iteritems():
                self.iterableItems.append(iterableItem)
                self.identifiers.append(identifier)

    def __nonzero__(self):
        return bool(self.__len__())

    def __contains__(self, value):
        for iterable in self.iterableItems:
            if value in iterable:
                return True

        return False

    def islice(self):
        return IteratorSlice(self)

    def __iter__(self):
        return IndexIterator(self, 0, len(self))

    def __len__(self):
        length = 0
        for iterable in self.iterableItems:
            length += iterableLength(iterable)
        return length

    def __getitem__(self, index):
        if type(index) == slice:
            results = []
            (start, end) = (index.start or 0, index.stop or len(self))
            if start < 0:
                start = 0
            if end > len(self):
                end = len(self)

            for num in range(start, end):
                results.append(self[num])

            return results
        else:
            currentSize = 0
            for iterableIndex, iterable in enumerate(self.iterableItems):
                if index >= currentSize and index < currentSize + iterableLength(iterable):
                    identifier = self.identifiers[iterableIndex]
                    return (identifier, iterable[index - currentSize])
                currentSize += iterableLength(iterable)

    def __setitem__(self, index, value):
        currentSize = 0
        for iterable in self.iterableItems:
            if index >= currentSize and index < currentSize + self.iterableLength(iterable):
                iterable[index - currentSize] = value
            currentSize += iterableLength(iterable)

    def __delitem__(self, index):
        currentSize = 0
        for iterable in self.iterableItems:
            if index >= currentSize and index < currentSize + iterableLength(iterable):
                del iterable[index - currentSize]
            currentSize += iterableLength(iterable)

    def pop(self, index=False):
        indexes = range(0, len(self.iterableItems))
        indexes.reverse()
        for index in indexes:
            iterable = self.iterableItems[index]
            if iterableLength(iterable):
                return (self.identifiers[index], iterable.pop())

    def getIterableIndex(self, index):
        currentSize = 0
        for index, iterable in enumerate(self.iterableItems):
            if index >= currentSize and index < currentSize + iterableLength(iterable):
                return index
            currentSize += iterableLength(iterable)

    def remove(self, value):
        for iterable in self.iterableItems:
            iterable.remove(value)

    def append(self, value):
        self.extend([value])

    def extend(self, valueList, identifier=None):
        self.iterableItems.append(valueList)
        self.identifiers.append(identifier)
        return valueList

    def count(self, value):
        count = 0
        for iterable in self.iterableItems:
            count += iterable.count(value)

        return count

class IterableCollectionList(IterableCollection):
    def __getitem__(self, index):
        if type(index) == slice:
            results = []
            (start, end) = (index.start or 0, index.stop or len(self))
            if start < 0:
                start = 0
            if end > len(self):
                end = len(self)

            for num in range(start, end):
                results.append(self[num])

            return results
        else:
            return IterableCollection.__getitem__(self, index)[1]

    def order(self, by):
        for iterable in self.iterableItems:
            iterable.order(by)

    def count(self):
        return len(self)

class SortedSet(set):
    """ A set that maintains order """

    def __init__(self, items):
        self.items = []
        for item in items:
            self.add(item)

    def __repr__(self):
        return "SortedSet(" + repr(self.items) + ")"

    def add(self, item):
        if not item in self:
            self.items.append(item)
            set.add(self, item)

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __eq__(self, value):
        return set.__eq__(self, value) or self.items == value

    def __iter__(self):
        return self.items.__iter__()

    def remove(self, item):
        return self.items.remove(item)


class Queryable(list):
    """ Lets you interact with a list as you would a django queryset - very useful for tests """
    def __init__(self, *kargs):
        list.__init__(self, *kargs)
        self.objects = self

    def __or__(self, other):
        inThisOnly = Queryable(other)
        for model in self:
            if model not in other:
                inThisOnly.append(model)

        return inThisOnly

    def __and__(self, other):
        inBoth = Queryable()
        for model in self:
            if model in other:
                inBoth.append(model)

        return inBoth

    def objects(self):
        return self

    def all(self):
        return self

    def get(self, **args):
        results = self.filter(**args)
        if results:
            return results[0]
        return None

    def filter(self, **args):
        return self.getMatches(args)[0]

    def exclude(self, **args):
        return self.getMatches(args)[1]

    @staticmethod
    def __lowerStrings__(value):
        if type(value) in types.StringTypes:
            return value.lower()
        else:
            return value

    def order_by(self, *fieldNames):
        order = OrderedDict()
        reverseSort = False
        for index, fieldName in enumerate(fieldNames):
            if fieldName.startswith("-"):
                reverseSort = True
                fieldNames[index] = fieldName[1:]
        for model in self:
            key = []
            for fieldName in fieldNames:
                value = str(model.__getattribute__(fieldName))
                if value.isdigit():
                    value = "%04d" % int(value)
                key.append(value)
            key += str(model.id)
            order["_".join(key)] = model
        order.orderedKeys.sort(key=self.__lowerStrings__)
        if reverseSort:
            order.orderedKeys.reverse()

        return Queryable(order.values())

    def values_list(self, columns, flat=False):
        resultList = []
        if type(columns) in types.StringTypes:
            columns = [columns]

        for item in self:
            for column in columns:
                if flat:
                    appendTo = resultList
                else:
                    appendTo = []
                    resultList.append(appendTo)
                appendTo.append(getattr(item, column, ''))
        return resultList

    def aggregate(self, **kwargs):
        """ XXX this is a dummy implementation ONLY so that tests will run when the aggregate method is used
            a full implementation should be created later when it is deemed nescarry """
        resultDict = {}
        for key, method in kwargs.iteritems():
            resultDict[key] = 0
        return resultDict

    def getMatches(self, queryDict):
        matches = Queryable()
        nonMatches = Queryable()
        for key, value in queryDict.iteritems():
            keys = key.split("__")
            filterType = "exact"
            caseInsensitive = False
            if keys[-1] in ['icontains', 'gte', 'gt', 'lte', 'lt', 'contains',
                            'iexact', 'exact', 'istartswith', 'startswith',
                            'className']:
                filterType = keys.pop(-1)
                if filterType.startswith('i'):
                    caseInsensitive = True
                    filterType = filterType[1:]

            key = None
            if keys:
                key = keys.pop(-1)

            for model in self:
                currentModel = model
                for modelName in keys:
                    if isinstance(currentModel, dict):
                        currentModel = currentModel[modelName]
                    else:
                        currentModel = currentModel.__getattribute__(modelName)

                if key == "in":
                    filterType = "in"
                    matchAgainst = currentModel
                elif key:
                    matchAgainst = getattr(currentModel, key, None)
                else:
                    matchAgainst = currentModel

                if caseInsensitive:
                    value = value.lower()
                    if not matchAgainst:
                        matchAgainst = ""
                    matchAgainst = matchAgainst.lower()

                matched = False
                if filterType == "in":
                    matched = matchAgainst in value
                elif filterType == "contains":
                    matched = value in matchAgainst
                elif filterType == "gte":
                    matched = matchAgainst >= value
                elif filterType == "lte":
                    matched = matchAgainst <= value
                elif filterType == "gt":
                    matched = matchAgainst > value
                elif filterType == "lt":
                    matched = matchAgainst < value
                elif filterType == "exact":
                    matched = value == matchAgainst
                elif filterType == "startswith":
                    matched = matchAgainst.startswith(value)
                elif filterType == "className":
                    matched = matchAgainst.__class__.__name__.lower() == value.lower()

                if matched == True:
                    if not model in nonMatches and not model in matches:
                        matches.append(model)
                else:
                    if not model in nonMatches:
                        nonMatches.append(model)
                    if model in matches:
                        matches.remove(model)

        return (matches, nonMatches)

    def count(self):
        return len(self)
