import unittest
from controller import OSAcontroller

# create a class called testOSA that inherits from unittest.TestCase, which is passed an instance of OSAcontroller as an argument.
class testOSA:

    def __init__(self):
        self.controller = OSAcontroller(self)

    def test_controller(self):
        print("test ")
        
        # test traces
        self.controller.set_current_trace('A')
        assert self.controller.get_current_trace() == 'A', "Trace A failed"


if __name__ == '__main__':
    testOSA()
