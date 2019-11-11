# coding=utf-8

"""
说明：
    此py文件是框架中编写测试案例的示例文件（以百度搜索作为示例）

    初次使用者可以参考本文件进行编写案例。

    如有修改的需要，建议复制一份此文件副本到TestCase目录下编写。
"""

import unittest

from src.testcasemore.testcasemore import TestCaseMore  # 扩展unittest.TestCase功能的类 [必写]
from src.newselenium.driver import Driver               # 浏览器驱动 [必写]

from Elements.百度 import 首页                           # 元素库 [依据实际需求编写]
from src.log.log import Log                             # 日志记录 [依据实际需求编写]
from src.newselenium.by import By                       # 提供多种定位方式 [依据实际需求编写]

logger = Log()                                          # 创建日志对象 [依据实际需求编写]


# 继承TestCaseMore 和 unittest.TestCase两个类 [必写]
class TestCaseDemo(unittest.TestCase, TestCaseMore):
    @classmethod                                        # 执行整个TestCase中只调用一次setUp [必写]
    def setUpClass(cls):                                # 案例初始化时执行 [必写]
        cls.driver = Driver("https://www.baidu.com")    # 初始化驱动，指定浏览器类型并打开url [依据实际需求编写]

    @classmethod                                        # 执行整个TestCase中只调用一次tearDown [必写]
    def tearDownClass(cls):                             # 案例结束时执行 [必写]
        cls.driver.quit()                               # 关闭浏览器进程 [依据实际需求编写]

    def test_1_scenario(self):                                      # 在此方法中编写测试用例场景 [每个类中至少定义一个场景]
        logger.info("正在执行 TestCaseDemo.test_1_scenario")         # 记录日志，级别为info [依据实际需求编写]
        self.driver.getelement(*首页.输入框).clear()                 # 操作步骤 [依据实际需求编写]
        self.driver.getelement(*首页.输入框).send_keys("Python")     # 操作步骤 [依据实际需求编写]
        self.driver.getelement(*首页.确定按钮).click()               # 操作步骤 [依据实际需求编写]
        self.get_screenshot()                                       # 截图，可在报告中查看 [依据实际需求编写]
        self.checkElement(*(By.CSS_SELECTOR, "#kw"))                # 检查指定元素是否存在，选择使用CSS选择器定位 [依据实际需求编写]
        self.assertEqual(self.driver.title, "Python_百度搜索")       # 断言标题是否为“Python_百度搜索” [依据实际需求编写]


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()