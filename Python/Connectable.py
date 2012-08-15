#!/usr/bin/python
'''
   Name:
       Connectable.py

   Description:
       Connectable enables child object to create dynamic connections
       (via signals/slots) at run-time.
'''

import types

import MethodUtils


class Connectable(object):

    signals = []

    def __init__(self):
        self.connections = {}

    def emit(self, signal, value=None):
        """
            Calls all slot methods connected with signal,
            optionally passing in a value

            signal - the name of the signal to emit, must be defined in the classes 'signals' list.
            value - the value to pass to all connected slot methods.
        """
        results = []
        if self.connections and signal in self.connections:
            for obj, conditions in self.connections[signal].iteritems():
                for condition, values in conditions.iteritems():
                    if condition == None or condition == value:
                        for overrideValue, slots in values.iteritems():
                            if overrideValue != None:
                                usedValue = overrideValue
                                if type(overrideValue) in types.StringTypes:
                                    usedValue = usedValue.replace('${value}', str(value))
                            else:
                                usedValue = value

                            for slot in slots:
                                if not hasattr(obj, slot):
                                    print(obj.__class__.__name__ +
                                            " slot not defined: " + slot)
                                    return False

                                slotMethod = obj.__getattribute__(slot)
                                if usedValue != None:
                                    if(MethodUtils.acceptsArguments(slotMethod, 1)):
                                        results.append(slotMethod(usedValue))
                                    elif(MethodUtils.acceptsArguments(slotMethod, 0)):
                                        results.append(slotMethod())
                                    else:
                                        results.append('')

                                else:
                                    results.append(slotMethod())

        return results

    def connect(self, signal, condition, receiver, slot, value=None):
        """
            Defines a connection between this objects signal
            and another objects slot:

            signal - the signal this class will emit, to cause the slot method to be called.
            condition - only call the slot method if the value emitted matches this condition.
            receiver - the object containing the slot method to be called.
            slot - the name of the slot method to call.
            value - an optional value override to pass into the slot method as the first variable.
        """
        if not signal in self.signals:
            print("%(name)s is trying to connect a slot to an undefined signal: %(signal)s" %
                      {'name':self.__class__.__name__, 'signal':unicode(signal)})
            return

        connections = self.connections.setdefault(signal, {})
        connection = connections.setdefault(receiver, {})
        connection = connection.setdefault(condition, {})
        connection = connection.setdefault(value, [])
        if not slot in connection:
            connection.append(slot)

    def disconnect(self, signal=None, condition=None,
                   obj=None, slot=None, value=None):
        """
            Removes connection(s) between this objects signal
            and connected slot(s):

            signal - the signal this class will emit, to cause the slot method to be called.
            condition - only call the slot method if the value emitted matches this condition.
            receiver - the object containing the slot method to be called.
            slot - the name of the slot method to call.
            value - an optional value override to pass into the slot method as the first variable.
        """
        if slot:
            connection = self.connections[signal][obj][condition][value]
            connection.remove(slot)
        elif obj:
            self.connections[signal].pop(obj)
        elif signal:
            self.connections.pop(signal, None)
        else:
            self.connections = {}
