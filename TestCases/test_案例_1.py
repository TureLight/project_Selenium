# coding:utf-8

import unittest
import time

from Elements.百度 import 首页  # 元素库
from src.log.log import Log  # 日志记录功能
from src.testcasemore.testcasemore import TestCaseMore  # 集成扩展unittest.TestCase功能的类
from src.newselenium.driver import Driver  # 使用经过二次封装的Dirver
from src.newselenium.by import By
from src.public.public import DataDrive
from src.config.config import Config
from src.database.db import test_dbcheck

logger = Log()  # 创建日志记录对象,记录日志信息通过logger.info logger.error选择不同级别来记录


# 继承TestCaseMore 和 unittest.TestCase两个类，必填
# TODO: 将 TestCaseMore 重新定义成混入类 后缀加上 *Mixin
class 案例1_搜索测试(unittest.TestCase, TestCaseMore):
    @classmethod  # 执行整个TestCase中只调用一次setUp
    def setUpClass(cls):  # 案例初始化时执行 必填
        cls.driver = Driver("https://www.baidu.com")  # 初始化驱动，指定浏览器类型并打开初始url

    @classmethod  # 执行整个TestCase中只调用一次tearDown
    def tearDownClass(cls):  # 案例结束时执行 必填
        cls.driver.quit()

    def test_1_百度搜索测试(self):  # 测试用例函数 类中至少要有一个
        logger.info("正在执行 案例1_搜索测试.test_1_百度搜索测试")  # 记录日志，级别为info
        self.driver.getelement(*首页.输入框).clear()  # 操作步骤
        self.driver.getelement(*首页.输入框).send_keys("Python")
        self.driver.getelement(*首页.确定按钮).click()
        time.sleep(2)
        logger.debug(self.driver.title)  # 记录日志，级别为debug
        self.driver.get_screenshot()  # 截图，自动保存在log目录下
        print("测试报告打印")
        self.get_screenshot()
        # 断言
        print(self.checkElement(*(By.CSS_SELECTOR, "#kw")))     # 检查指定元素是否存在
        self.assertEqual(self.driver.title, "Python_百度搜索")   # 断言标题是否为“Python_百度搜索”

    @test_dbcheck(sql="select * from hs_user.sysarg;")
    def test_2_百度搜索测试(self):
        # 数据驱动测试
        self.search()

    @DataDrive.testDateFromExcel(path=Config.projectDir + r"\Data\TestData.xlsx")
    def search(self, 搜索内容, 显示条数, 是否存在):
        print(搜索内容, 显示条数, 是否存在)
        # ...
        # 自动化场景
        # ...


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()
