# coding=utf-8

"""
说明：
    此py文件是一个数据驱动测试的示例

    是通过 from src.public.public import DataDrive 中的两个装饰器实现
        1. testDateFromExcel
        2. testDateFromCsv

     如有修改的需要，建议复制一份此文件副本到TestCase目录下编写。
"""

import unittest

from src.testcasemore.testcasemore import TestCaseMore  # 扩展unittest.TestCase功能的类 [必写]
from src.newselenium.driver import Driver               # 浏览器驱动 [必写]

from src.log.log import Log                             # 日志记录 [依据实际需求编写]
from src.public.public import DataDrive                 # 数据驱动类，里面提供数据驱动装饰器 [依据实际需求编写]
from src.config.config import Config                    # 获取配置信息 [依据实际需求编写]



logger = Log()                                          # 创建日志对象 [依据实际需求编写]


# 继承TestCaseMore 和 unittest.TestCase两个类 [必写]
class TestCaseDemo(unittest.TestCase, TestCaseMore):
    @classmethod                                        # 执行整个TestCase中只调用一次setUp [必写]
    def setUpClass(cls):                                # 案例初始化时执行 [必写]
        cls.driver = Driver("https://www.baidu.com")    # 初始化驱动，指定浏览器类型并打开url [依据实际需求编写]

    @classmethod                                        # 执行整个TestCase中只调用一次tearDown [必写]
    def tearDownClass(cls):                             # 案例结束时执行 [必写]
        cls.driver.quit()                               # 关闭浏览器进程 [依据实际需求编写]

    def test_1_datadriven(self):                                      # 在此方法中编写测试用例场景 [每个类中至少定义一个场景]
        logger.info("正在执行 TestCaseDemo.test_1_datadriven")         # 记录日志，级别为info [依据实际需求编写]
        self.search()                                                 # 执行数据驱动的场景

    @DataDrive.testDateFromExcel(path=Config.projectDir + r"\Data\TestData.xlsx")  # 选择数据驱动的数据文件 [依据实际需求编写]
    def search(self, 搜索内容, 显示条数, 是否存在):                     # 这里参数名字必须和数据文件中字段名一致 [依据实际需求编写]
        print(搜索内容, 显示条数, 是否存在)                             # 执行场景 [依据实际需求编写]
        # ...
        # 执行场景
        # ...


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()