import unittest

from pyost.verboser.verboser import Verboser


class VerboserTest(unittest.TestCase):
    def test_1(self):
        Verboser.enableError    = True
        Verboser.inColor        = True
        Verboser.withTime       = True

        Verboser.addInfoLevel(0)
        Verboser.addInfoLevel(1)

        Verboser.info("THIS IS A UNITTEST!", 0)

        Verboser.error("This is an error") 
        Verboser.info("information about something")
        Verboser.info("hello", 1)

        Verboser.enableWarning  = True
        Verboser.warning("warning") 

        Verboser.enableSuccess  = True
        Verboser.success("yes it worked")

        Verboser.addDebugLevel(0)
        Verboser.debug("debugging")

        Verboser.removeInfoLevel(1)

        Verboser.info("I will not be printed", 1)

        Verboser.saveToHistory = True
        
        Verboser.info("This")
        Verboser.info("Is")
        
        Verboser.info("In")
        Verboser.info("History")
        
        Verboser.printMessageHistory()


        Verboser.saveToHistory = False

        Verboser.addInfoLevel("MYINFO")

        Verboser.debug("Debug from verboser", "VERBOSER")

        Verboser.addDebugLevel("VERBOSER")

        Verboser.info("hello world", "MYINFO")
        Verboser.debug("Debug from verboser", "VERBOSER")

        Verboser.removeDebugLevel("VERBOSER")
        Verboser.debug("Debug from verboser", "VERBOSER")

        Verboser.removeInfoLevel("MYINFO")
        Verboser.info("hello world", "MYINFO")
        
        self.assertTrue(True)



