# coding=utf-8

"""
说明：
    此py文件是做数据库检查（DB check）的示例

    是通过 from src.database.db import test_dbcheck test_dbcheck装饰器来实现
        每次执行完被装饰的场景后都会执行该条语句的数据比对。
        期望数据.xlsx与执行结果.xlsx都在当前案例目录中，执行完比对后会生成一份比较结果文件。而且当比对失败后也会在报告中提示出来。
        注意：当第一次执行时由于没有期望数据，不会成功比较，可以将第一次执生成的实际结果文件改成期望数据（修改文件名[执行结果]改为[期望数据]）。第二次执行时就可作为期望数据进行比对。

    如有修改此py文件的需要，建议复制一份此文件副本到TestCase目录下编写。
"""

import unittest

from src.testcasemore.testcasemore import TestCaseMore  # 扩展unittest.TestCase功能的类 [必写]
from src.newselenium.driver import Driver               # 浏览器驱动 [必写]

from src.log.log import Log                             # 日志记录 [依据实际需求编写]
from src.database.db import test_dbcheck                # 数据库比对装饰器 [依据实际需求编写]

logger = Log()                                          # 创建日志对象 [依据实际需求编写]


# 继承TestCaseMore 和 unittest.TestCase两个类 [必写]
class TestCaseDemo(unittest.TestCase, TestCaseMore):
    @classmethod                                        # 执行整个TestCase中只调用一次setUp [必写]
    def setUpClass(cls):                                # 案例初始化时执行 [必写]
        cls.driver = Driver("https://www.baidu.com")    # 初始化驱动，指定浏览器类型并打开url [依据实际需求编写]

    @classmethod                                        # 执行整个TestCase中只调用一次tearDown [必写]
    def tearDownClass(cls):                             # 案例结束时执行 [必写]
        cls.driver.quit()                               # 关闭浏览器进程 [依据实际需求编写]

    @test_dbcheck(sql="select * from hs_user.sysarg;")             # 需要检查的数据 [依据实际需求编写]
    def test_1_dbcheck(self):                                      # 在此方法中编写测试用例场景 [每个类中至少定义一个场景]
        logger.info("正在执行 TestCaseDemo.test_1_dbcheck")         # 记录日志，级别为info [依据实际需求编写]


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()