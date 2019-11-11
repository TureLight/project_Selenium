# coding=utf-8

import unittest
import time

from Elements.百度 import 首页
from src.testcasemore.testcasemore import TestCaseMore  # 继承一些公共方法
from src.config.config import Config
from src.newselenium.driver import Driver
from src.log.log import Log

logger = Log()


class 案例2_搜索测试(TestCaseMore, unittest.TestCase):
    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def setUpClass(cls):
        cls.driver = Driver("https://www.baidu.com")  # 根据配置文件获取相应版本的浏览器Driver
        cls.base_url = "https://www.baidu.com"

    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def tearDownClass(cls):
        cls.driver.quit()

    def test_2_百度搜索测试(self):
        logger.info("正在执行 Test_2.test_baidu_2_search")
        self.driver.getelement(*首页.输入框).clear()
        self.driver.getelement(*首页.输入框).send_keys("Selenium")
        self.driver.getelement(*首页.确定按钮).click()
        time.sleep(2)
        self.get_screenshot()
        # 断言
        self.assertEqual(self.driver.title, "Selenium_百度搜索")

    def test_3_百度搜索测试(self):
        logger.info("正在执行 Test_2.test_baidu_3_search")
        excel_path = Config.projectDir + r"\Data\TestData.xlsx"
        self.driver.get(url=self.base_url)
        self.driver.getelement(*首页.输入框).clear()
        self.driver.getelement(*首页.输入框).send_keys(
            self.readExcel(path=excel_path, sheet=1, row=2, column="搜索内容")
        )
        self.driver.getelement(*首页.确定按钮).click()
        time.sleep(2)
        # 断言
        self.get_screenshot()
        self.assertEqual(self.driver.title, "Selenium_百度搜索_断言")


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()
