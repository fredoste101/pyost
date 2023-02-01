import unittest

from pyost.verboser.verboser import Verboser


class VerboserTest(unittest.TestCase):
    def test_1(self):
        verboser = Verboser()
        verboser.enableError    = True
        verboser.inColor        = True
        verboser.withTime       = True

        verboser.addInfoLevel(0)
        verboser.addInfoLevel(1)

        verboser.info("THIS IS A UNITTEST!", 0)

        verboser.error("This is an error") 
        verboser.info("information about something")
        verboser.info("hello", 1)

        verboser.enableWarning  = True
        verboser.warning("warning") 

        verboser.enableSuccess  = True
        verboser.success("yes it worked")

        verboser.addDebugLevel(0)
        verboser.debug("debugging")

        verboser.removeInfoLevel(1)

        verboser.info("I will not be printed", 1)

        verboser.saveToHistory = True
        
        verboser.info("This")
        verboser.info("Is")
        verboser.info("In")
        verboser.info("History")
        
        verboser.printMessageHistory()
        
        self.assertTrue(True)



