# coding=utf-8

import unittest

from src.log.log import Log
from src.testcasemore.testcasemore import TestCaseMore


logger = Log()


class Test_4(TestCaseMore, unittest.TestCase):
    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def setUpClass(cls):
        pass

    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def tearDownClass(cls):
        pass

    def test_4_1(self):
        logger.info("正在执行 Test_4.test_4_1")
        print("test_4_1")

    def test_4_2(self):
        logger.info("正在执行 Test_4.test_4_2")
        print("test_4_2")


class Test_5(TestCaseMore, unittest.TestCase):
    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def setUpClass(cls):
        pass

    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def tearDownClass(cls):
        pass

    def test_5_1(self):
        logger.info("正在执行 Test_5.test_5_1")
        print("test_5_1")

    def test_5_2(self):
        logger.info("正在执行 Test_5.test_5_2")
        print("test_5_2")


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()
