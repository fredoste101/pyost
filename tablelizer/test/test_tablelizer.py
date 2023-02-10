import unittest

from ..tablelizer import TablelizerTerminal


class TablelizerTest(unittest.TestCase):
    def test_terminal(self):
        tt = TablelizerTerminal()
        tt.headerList = ["x", "y"]

        tt.dataRowList = [["1", "0"], ["1", "0"], ["4", "this is a sentence\nThis is another"]]

        tt.config["align"] = "left"

        print(tt.getString())

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()