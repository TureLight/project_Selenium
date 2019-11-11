# coding=utf-8

import traceback
import os
import random
from typing import Union, Iterable, Tuple
from selenium.common.exceptions import NoSuchElementException

from src.newselenium.driver import Driver
from src.newselenium.by import By
from src.public.public import Public
from src.public import g
from src.exception.seleniumexecption import SeleniumTypeError
from src.config.config import Config
from src.database.db import DB
from src.database.compare import Compare


class TestCaseMore(Public, object):
    def checkElement(self, by=By.ID, value=None):
        """
        说明：
            检查元素是否存在，如果存在则返回该元素对象，如果不存在则校验失败并在报告中体现
        :param by:
        :param value:
        :return: 存在则返回元素对象
        """
        if isinstance(self.driver, Driver):
            try:
                return self.driver.getelement(by=by, value=value)
                # self.driver.driver.find_element(by=by, value=value)
            except NoSuchElementException:
                self.assertTrue(
                    False, "未找到该元素，%s" % ("方式：" + str(by) + " 值：" + str(value))
                )
                return False
                # self.verificationErrors.append("未找到该元素，%s" % ("方式：" + str(by) + " 值：" + str(value)))
        else:
            raise SeleniumTypeError("self.driver 对象类型不对，应为Driver类，请检查...")

    def get_screenshot(self):
        """
        说明：
            截图并会在测试报告中体现
            单独调试TestCase时，可以在“\Report\tempimg\”目录下查看截图
        """
        s = traceback.extract_stack()
        projectdir = Config.projectDir
        random_int = random.randint(10000000, 99999999)  # 随机数
        # 图片名称 需要拼上测试案例相关信息
        screenshot_name = (self.__module__
            + "."
            + self.__class__.__name__
            + "."
            + s[-2][2]
            + "_"
            + str(random_int)
            + ".png")
        path = os.path.join(
            projectdir,
            "report",
            "tempimg",
            screenshot_name,
        )
        # 截图保存
        self.driver.get_screenshot(path=path)
        g.SCREENSHOTS_NAME.append(screenshot_name)

    def dbcheck(self, sql: Union[str, Iterable[str]]) -> bool:
        """
        说明：
            执行数据比对

        :param sql: 需要比对的sql语句

        :return: True or False <class 'bool'>
        """
        except_path, actual_path = self._get_compare_filename()
        except_exist = os.path.exists(except_path)
        if not except_exist:
            DB().expectation(sql=sql,
                             excel_path=actual_path,)
            return False
        else:  # 存在期望结果则开始比较
            DB().expectation(sql=sql,
                             excel_path=actual_path, )
            return Compare(expected=except_path, actual=actual_path).compare()

    def _get_compare_filename(self):
        _module = self.__module__
        _module = _module.replace(".", "\\")
        case_filename = os.path.realpath(_module + ".py")
        _dir = os.path.dirname(case_filename)  # case案例所在目录
        _name = ( "["
                + self.__module__
                + "."
                + self.__class__.__name__
                + "."
                + self._testMethodName
                + "]")
        except_path = os.path.join(_dir, _name) + "_[期望结果].xlsx"
        actual_path = os.path.join(_dir, _name) + "_[执行结果].xlsx"
        return except_path, actual_path
