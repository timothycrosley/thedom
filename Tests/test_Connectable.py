'''
    Tests that Connectable can correctly create and act upon connections between objects
'''

from WebElements.Connectable import Connectable

class Value(Connectable):
    signals = ['valueChanged']

    def __init__(self, value):
        super(Value, self).__init__()
        self.value = value

    def setValue(self, value):
        self.value = value
        self.emit('valueChanged', value)

    def clearValue(self):
        self.value = ""

    def tooManyParmsToBeSlot(self, param1, param2):
        pass


class TestConnectable(object):

    def setup_method(self, method):
        self.value1 = Value(1)
        self.value2 = Value(2)

    def test_incorrectSignalSlotConnections(self):
        #emit fake signal
        assert self.value1.emit("fake signal") == []

        #connect using fake signal
        assert self.value1.connect("fake signal", None, self, 'setValue') is None

        #connect to fake slot
        self.value1.connect("valueChanged", None, self.value1, 'fake slot')
        assert self.value1.emit('valueChanged') is False

    def test_connectWithoutCondition(self):
        #test without value overide
        self.value1.connect('valueChanged', None, self.value2, 'setValue')
        self.value1.setValue("This is a test")
        assert self.value2.value == "This is a test"
        self.value1.disconnect()

        #test with value overide
        self.value1.connect('valueChanged', None,
                            self.value2, 'setValue', 'I changed the value')
        self.value1.setValue("This is a test")
        assert self.value2.value == "I changed the value"

    def test_connectWithCondition(self):
        #test without value overide
        self.value1.connect('valueChanged', 'Hello', self.value2, 'setValue')
        self.value1.setValue('Goodbye')
        assert self.value2.value == 2
        self.value1.setValue('Hello')
        assert self.value2.value == 'Hello'
        self.value1.disconnect()

        #test with value overide
        self.value1.connect('valueChanged', 'Hello',
                            self.value2, 'setValue', 'Goodbye')
        self.value1.setValue('Goodbye')
        assert self.value2.value == 'Hello'
        self.value1.setValue('Hello')
        assert self.value2.value == 'Goodbye'

        #Test on slot that takes no arguments
        self.value1.connect('valueChanged', 'Die!!', self.value2, 'clearValue')
        assert self.value1.emit('valueChanged', 'Die!!') == [None]
        self.value1.connect('valueChanged', None, self.value2, 'clearValue')
        assert self.value1.emit('valueChanged') == [None]
        self.value1.disconnect()

        #Test method with too many params to be a slot
        self.value1.connect('valueChanged', 'False', self.value2, 'tooManyParmsToBeSlot')
        assert self.value1.emit('valueChanged', 'False') == ['']

    def test_disconnect(self):
        self.value1.connect('valueChanged', None, self.value2, 'setValue')
        self.value1.setValue('It changes the value')
        assert self.value2.value == 'It changes the value'

        self.value1.disconnect('valueChanged', None, self.value2, 'setValue')
        self.value1.setValue('But not anymore')
        assert self.value2.value == 'It changes the value'

        self.value1.connect('valueChanged', None, self.value2, 'setValue')
        self.value1.disconnect('valueChanged', None, self.value2)
        self.value1.setValue('Still Wont')
        assert self.value2.value == 'It changes the value'

        self.value1.connect('valueChanged', None, self.value2, 'setValue')
        self.value1.disconnect('valueChanged')
        self.value1.setValue('Still Wont')
        assert self.value2.value == 'It changes the value'
