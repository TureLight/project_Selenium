# coding=utf-8

from selenium.common.exceptions import NoSuchElementException
import unittest
import time, os

from Elements.jira import JIRA
from src.log.log import Log
from src.testcasemore.testcasemore import TestCaseMore
from src.newselenium.driver import Driver
from src.newselenium.keys import Keys
from src.config.config import Config

logger = Log()


class 案例3_JIRA(TestCaseMore, unittest.TestCase):
    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def setUpClass(cls):
        cls.driver = Driver(
            "https://se.hundsun.com/dm/secure/Dashboard.jspa"
        )  # 根据配置文件获取相应版本的浏览器Driver
        cls.base_url = "https://se.hundsun.com/dm/secure/Dashboard.jspa"

    @classmethod  # 执行整个TestCase中只调用一次setUp和tearDown
    def tearDownClass(cls):
        # cls.driver.quit()
        pass

    def test_1_JIRA_登录测试(self):
        logger.info("正在执行 案例3_JIRA.test_1_JIRA_登录测试")
        self.driver.get(url=self.base_url)
        self.driver.getelement(*JIRA.登录用户名输入框).send_keys("zhangzheng17239")
        self.driver.getelement(*JIRA.登录密码输入框).send_keys("********")
        self.driver.getelement(*JIRA.登录确定按钮).click()
        self.get_screenshot()
        time.sleep(2)
        # 断言
        self.checkElement(*JIRA.a_zhangzheng_loc)

    def test_2_JIRA_新增缺陷(self):
        logger.info("正在执行 案例3_JIRA.test_2_JIRA_新增缺陷")
        self.driver.getelement(*JIRA.新建按钮).click()
        self.driver.getelement(*JIRA.概要输入框).send_keys("输入概要")
        self.driver.getelement(*JIRA.优先级输入框).send_keys("致命")
        self.driver.getelement(*JIRA.缺陷来源下拉框).select("代码活动")
        self.driver.getelement(*JIRA.缺陷来源第二个下拉框).select("逻辑问题（函数引用、返回、顺序、易读性）")
        self.driver.getelement(*JIRA.模块多行输入框).send_keys("UFTDB")
        self.driver.getelement(*JIRA.单元测试发现).select("是")
        self.driver.getelement(*JIRA.经办人输入框).send_keys("张正")
        self.driver.getelement(*JIRA.经办人输入框).keyboard(Keys.ENTER)
        self.driver.getelement(*JIRA.环境多行输入框).send_keys("输入环境")
        self.driver.getelement(*JIRA.描述多行输入框).send_keys("输入描述")
        self.driver.getelement(*JIRA.上传文件).send_keys(
            os.path.join(Config.projectDir, "runtest.py")
        )
        self.driver.getelement(*JIRA.上传文件).send_keys(
            os.path.join(Config.projectDir, "demo.py")
        )
        self.driver.getelement(*JIRA.报告人输入框).send_keys("张正")
        self.driver.getelement(*JIRA.报告日期输入框).clear()
        self.driver.getelement(*JIRA.报告日期输入框).send_keys("1/四月/18")
        self.driver.getelement(*JIRA.修改单号输入框).send_keys("123123")
        self.driver.getelement(*JIRA.缺陷发现阶段选择框).select("编码（单元测试）")
        self.driver.getelement(*JIRA.类别选择框).select("A.功  能")
        self.driver.getelement(*JIRA.打回次数输入框).send_keys("1")
        self.driver.getelement(*JIRA.测试方法选择框).select("自动化测试")


# 案例也可单独调试
if __name__ == "__main__":
    unittest.main()
