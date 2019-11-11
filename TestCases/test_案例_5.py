# coding=utf-8

import unittest

from src.log.log import Log
from src.testcasemore.testcasemore import TestCaseMore
from src.gui import Operate


logger = Log()


class Test_4(TestCaseMore, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_gui_operte(self):
        Operate.mouse_click(x=500, y=300, button="right", speed=50)


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()
