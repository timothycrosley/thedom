"""
    Name:
        MethodUtils.py

    Description:
        A collection of functions to aid in method introspection and usage

"""


def acceptsArguments(method, numberOfArguments):
    """Returns True if the given method will accept the given number of arguments:
            method - the method to perform introspection on
            numberOfArguments - the numberOfArguments
    """
    if method.__class__.__name__ == 'instancemethod':
        numberOfArguments += 1
        numberOfDefaults = method.im_func.func_defaults and len(method.im_func.func_defaults) or 0
    elif method.__class__.__name__ == 'function':
        # static method being passed in
        numberOfDefaults = method.func_defaults and len(method.func_defaults) or 0
    if(method.func_code.co_argcount >= numberOfArguments and
       method.func_code.co_argcount - numberOfDefaults <= numberOfArguments):
        return True

    return False


class CallBack(object):
    """ Enables objects to be passed around in a copyable/pickleable way """

    def __init__(self, obj, method, argumentDict=None):
        """ Creates the call back object:
                obj - the actual object that the method will be called on
                method - the name of the method to call
        """
        self.toCall = method
        self.obj = obj
        self.argumentDict = argumentDict

    def __call__(self):
        return self.call()

    def call(self):
        """ Calls the method """
        if self.argumentDict:
            return self.obj.__getattribute__(self.toCall)(**self.argumentDict)
        else:
            return self.obj.__getattribute__(self.toCall)()
