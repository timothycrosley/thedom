'''
    MethodUtils.py

    A collection of functions to aid in method introspection and usage

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

from .MultiplePythonSupport import *

def acceptsArguments(method, numberOfArguments):
    """
        Returns True if the given method will accept the given number of arguments:
            method - the method to perform introspection on
            numberOfArguments - the numberOfArguments
    """
    if 'method' in method.__class__.__name__:
        numberOfArguments += 1
        func = getattr(method, 'im_func', getattr(method, '__func__'))
        funcDefaults = getattr(func, 'func_defaults', getattr(func, '__defaults__'))
        numberOfDefaults = funcDefaults and len(funcDefaults) or 0
    elif method.__class__.__name__ == 'function':
        funcDefaults = getattr(method, 'func_defaults', getattr(method, '__defaults__'))
        numberOfDefaults = funcDefaults and len(funcDefaults) or 0
    coArgCount = getattr(method, 'func_code', getattr(method, '__code__')).co_argcount
    if(coArgCount >= numberOfArguments and coArgCount - numberOfDefaults <= numberOfArguments):
        return True

    return False


class CallBack(object):
    """
        Enables objects to be passed around in a copyable/pickleable way
    """

    def __init__(self, obj, method, argumentDict=None):
        """
            Creates the call back object:
                obj - the actual object that the method will be called on
                method - the name of the method to call
        """
        self.toCall = method
        self.obj = obj
        self.argumentDict = argumentDict

    def __call__(self):
        return self.call()

    def call(self):
        """
            Calls the method
        """
        if self.argumentDict:
            return self.obj.__getattribute__(self.toCall)(**self.argumentDict)
        else:
            return self.obj.__getattribute__(self.toCall)()
