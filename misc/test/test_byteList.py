import unittest

from pyost.misc.byteList import ByteList


class ByteListTest(unittest.TestCase):
    def test_0(self):
        testStringList = ["AD", "05", "5E", "DE", "0F", "3B", "71", "A0", "AA", "25"]

        byteList = ByteList()

        byteList.stringList = testStringList

        for testString in testStringList:
            parsedValue = hex(byteList.parseItem(8))[2:].upper().rjust(2, "0")
            self.assertEqual(testString, parsedValue)

    def test_1(self):
        testStringList = ["AD", "05", "5E", "DE", "0F", "3B", "71", "A0", "AA", "25"]

        byteList = ByteList()

        byteList.stringList = testStringList

        for testString0, testString1 in zip(testStringList[::2], testStringList[1::2]):
            parsedValue = hex(byteList.parseItem(16))[2:].upper().rjust(4, "0")
            self.assertEqual(testString0 + testString1, parsedValue)


    def test_2(self):
        testStringList = ["AD", "05", "5E", "DE", "0F", "3B", "71", "A0", "AA", "25"]

        byteList = ByteList()

        byteList.stringList = testStringList

        for testString in testStringList:
            bitString = bin(int(testString, 16))[2:].rjust(8, "0")

            for bit in bitString:
                self.assertEqual(int(bit), byteList.parseItem(1))


    def test_3(self):
        testStringList = ["AD", "05", "5E", "DE", "0F", "3B", "71", "A0", "AA", "25"]

        byteList = ByteList()

        byteList.stringList = testStringList

        for testString in testStringList:
            bitString = bin(int(testString, 16))[2:].rjust(8, "0")

            for bit0, bit1 in zip(bitString[::2], bitString[1::2]):
                self.assertEqual(bit0 + bit1, bin(byteList.parseItem(2))[2:].rjust(2, "0"))

            
    def test_4(self):
        testStringList = ["AD", "05", "5E", "DE", "0F", "3B", "71", "A0", "AA", "25"]

        byteList = ByteList()

        byteList.stringList = testStringList

        for testString in testStringList:
            for char in testString:
                self.assertEqual(char, hex(byteList.parseItem(4))[2:].upper())