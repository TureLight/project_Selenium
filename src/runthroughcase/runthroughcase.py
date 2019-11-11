# coding=utf-8

import pandas as pd
import unittest

from src.config.config import Config
from typing import Tuple


def getConfigWay(value: str) -> int:
    if value == "1-按方法运行":
        return 1
    elif value == "2-按类名运行":
        return 2
    elif value == "3-按模块运行":
        return 3
    elif value == "4-按路径运行":
        return 4


def getPath(value: str) -> str:
    # 去掉路径前后的"\"
    value = value.replace("\\", ".")
    if value[0] == ".":
        value = value[1:]
    if value[-1] == ".":
        value = value[:-1]
    return value


def getFileName(value: str) -> str:
    if "." not in value:
        return value
    return ".".join(value.split(".")[0:-1])


def getClassName(value: str) -> str:
    return value


def getFunctionName(value: str) -> str:
    return value


def whetherRun(value: str) -> bool:
    """
    说明：
        判断是否运行该用例
    :param value: type = <class str> 
    :return: type = <class boolean>
    """
    if ("N" in value) or ("n" in value) or ("否" in value) or ("不" in value):
        return False
    else:
        return True


def getFileFullName(value: str) -> str:
    """
    说明：
        获取文件的名称，包含后缀
    :param value:
    :return:
    """
    if "." not in value:
        raise TypeError("请在“测试计划.xlsx”中写明文件名包含文件格式。”")
    elif value.split(".")[-1] not in ["xlsx", "xls"]:
        raise TypeError(
            "“测试计划.xlsx”不支持配置%s格式文件名，请转化为.xlsx或.xls。" % value.split(".")[-1]
        )
    else:
        return value


# 读取测试案例配置.xlsx，返回一个或多个suite(取决于配置了多少个sheet页，sheet页之间是多进程并行执行)
def addTestCaseByExcel(filename: str) -> tuple:
    """
    说明：
        传入测试案例配置的文件名，返回解析该文件后生成的suite
    :param filename: 文件名
    :return: (suite1, suite2) <class tuple>
    """
    # 构造测试集 方法1 添加测试用例类中的方法(函数)
    # suite.addTest(Test_1('test_baidu_1_search'))
    # suite.addTest(Test_2('test_baidu_2_search'))
    # suite.addTest(Test_2('test_baidu_3_search'))
    # suite.addTest(Test_zhaopin_1('test_search_1'))
    # suite.addTest(Test_3('test_1_jira'))
    # suite.addTest(Test_5('test_1_createIssure'))
    # 构造测试集 方法2 添加测试用例类中的所有方法(函数)
    # suite = unittest.TestSuite(unittest.makeSuite(Test_2))
    # 构造测试集 方法3 添加目录中所有的测试用例类的方法(函数)
    # suite = unittest.TestLoader().discover("test")
    # 构造测试集 方法4 按照Excel案例配置运行
    # addTestCaseByExcel(suite)
    suites = []
    od = pd.read_excel(
        io=Config.projectDir + "\\Config\\" + filename, sheet_name=None
    )  # 读取所有sheet 返回OrderedDict
    sheets = list(od.keys())  # 获取Execl所有sheet名
    for sheet in sheets:  # 分别处理每个sheet中的案例配置
        suite = unittest.TestSuite()  # 每个sheet构造一个suite
        suite.sheet_name = sheet
        suite.file_name = filename
        df = od[sheet]
        max_row = df.shape[0]  # 案例个数
        for i in range(max_row):
            if whetherRun(df.at[i, "是否执行"]):
                path = getPath(df.at[i, "路径"])
                pyfilename = getFileName(df.at[i, "文件名"])
                classname = getClassName(df.at[i, "类名"])
                funname = getFunctionName(df.at[i, "方法名"])
                if getConfigWay(df.at[i, "配置方式"]) == 1:  # 按方法运行
                    import_str = (
                        "from " + path + "." + pyfilename + " import " + classname
                    )
                    addtest_str = "suite.addTest(" + classname + "('" + funname + "'))"
                    exec(import_str)
                    eval(addtest_str)
                elif getConfigWay(df.at[i, "配置方式"]) == 2:  # 按类名运行
                    import_str = (
                        "from " + path + "." + pyfilename + " import " + classname
                    )
                    addtest_str = "suite.addTest(unittest.TestLoader().loadTestsFromTestCase(" + classname + "))"
                    exec(import_str)
                    eval(addtest_str)
                elif getConfigWay(df.at[i, "配置方式"]) == 3:  # 按模块运行
                    import_str = (
                        "from " + path + " import " + pyfilename
                    )
                    addtest_str = "suite.addTest(unittest.TestLoader().loadTestsFromModule(" + pyfilename + "))"
                    exec(import_str)
                    eval(addtest_str)
                elif getConfigWay(df.at[i, "配置方式"]) == 4:  # 按路径运行
                    addtest_str = (
                        'suite.addTest(unittest.TestLoader().discover("' + path + '"' + "))"
                    )  # such as suite.addTest(unittest.TestLoader().discover("test"))
                    eval(addtest_str)
        suites.append(suite)
    return tuple(suites)


# 读取测试计划配置.xlsx
def readTestPlanExcel() -> tuple:
    """
    说明：
        读取测试计划.xlsx，获取配置串行运行案例的文件名。
    :return:
        文件名 <class tuple>
    """
    df = pd.read_excel(
        io=Config.projectDir + r"\Config\测试计划.xlsx", sheet_name=0
    )  # 只读取第一个sheet页
    max_row = df.shape[0]  # 配置个数
    filenames = []
    for i in range(max_row):
        if whetherRun(df.at[i, "是否执行"]):
            filename = getFileFullName(df.at[i, "文件名"])
            filenames.append(filename)
    return tuple(filenames)


# 构造多进程执行计划
def testPlan() -> Tuple[Tuple]:
    """
    说明：
        构造多进程的执行计划
    :return:
            返回不同Excel中sheet页案例所构造的suite
            <类型 tuple of tuple>
            ((suite1,), (suite2, suite3), (suite4,)))
                ^               ^
            Excel有1个sheet Excel有2个sheet
            (suite1,) 与  (suite2, suite3) 与 (suite4,) 串行执行， suite2, suite3 并行执行。
    """
    filenames = readTestPlanExcel()
    allsuites = []
    for filename in filenames:
        suites = addTestCaseByExcel(filename)
        allsuites.append(suites)
    return tuple(allsuites)
