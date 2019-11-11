# coding=utf-8

import unittest
import time

from Elements.火车票 import 主页, 购票页
from src.log.log import Log  # 日志记录功能
from src.testcasemore.testcasemore import TestCaseMore  # 继承一些公共方法
from src.newselenium.driver import Driver  # 可使用经过二次处理的Dirver
from src.newselenium.keys import Keys
from src.database.db import test_dbcheck

logger = Log()


class 购票(TestCaseMore, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://www.12306.cn/"
        cls.driver = Driver(cls.base_url, "firefox")
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_1_购票查询(self):
        logger.info("正在执行购票.test_1_购票查询")
        self.driver.getelement(*主页.购票).click()
        time.sleep(5)
        self.driver.switch_to_window(self.driver.window_handles[1])
        # 通过js实现元素操作
        # self.driver.execute_script("document.getElementById('fromStationText').value = '杭州';")
        # self.driver.execute_script("document.getElementById('toStationText').value = '郑州';")
        self.driver.getelement(*购票页.出发地).click()
        self.driver.getelement(*购票页.出发地).send_keys("杭州")
        self.driver.getelement(*购票页.出发地).keyboard(key=Keys.ENTER)
        self.driver.getelement(*购票页.目的地).click()
        self.driver.getelement(*购票页.目的地).send_keys("郑州")
        self.driver.getelement(*购票页.目的地).keyboard(key=Keys.ENTER)
        # 使用js方法输入
        self.driver.getelement(*购票页.出发日).js_send_keys("2018-06-20")
        self.driver.getelement(*购票页.返程日).js_send_keys("2018-06-21")
        self.driver.getelement(*购票页.学生).click()
        self.driver.getelement(*购票页.查询).click()

    def test_2_购票信息修改(self):
        res = self.dbcheck(sql="select * from hs_user.sysarg;")
        print("数据库比对结果：", res)
