# coding=utf-8

# TODO: 1. 多台环境分布式执行
# TODO: 2. 继续封装PyAutoIt方法

from datetime import datetime
import traceback
from multiprocessing import Pool, current_process
import os
import shutil
from typing import Tuple

from src.report.HTMLTestRunner import HTMLTestRunner
from src.config.config import Config
from src.report.sendemail import sendEmail
from src.runthroughcase.runthroughcase import testPlan
from src.log.log import Log
from src.public.public import Public, ParseXml

logger = Log()  # 创建日志记录对象 logger


# 报告相关信息
class ReportInfo:
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    reportname = "ResultReport_%s" % time  # 报告名
    reportfullname = reportname + ".html"  # 报告文件名 格式为.html
    reportparentdir = os.path.join(Config.projectDir, "Report", reportname)  # 报告文件所在的报告目录，目录名与报告名一致
    reportpath = os.path.join(reportparentdir, reportfullname)  # 同名目录下创建同名报告


# 重制后报告信息
class ReMakeReport:
    startTime = " "
    stopTime = " "
    success_count = 0
    failure_count = 0
    error_count = 0
    title = " "
    description = " "
    test_method_results = []  # 元素为每个测试方法的执行结果
    test_plan_results = []  # 元素为每个测试计划的执行结果


# 重制报告内容
def remake_report(results: list):
    startime = datetime.strptime("2999-12-31 23:59:59", r"%Y-%m-%d %H:%M:%S")
    stopime = datetime.strptime("2000-01-01 00:00:01", r"%Y-%m-%d %H:%M:%S")
    total_success_count = 0
    total_failure_count = 0
    total_error_count = 0
    total_results = []
    total_testplan_count = len(results)  # 测试计划配置中启用的案例个数
    test_plan_results = results
    for i, _results in enumerate(results):
        total_testsuit_count = len(_results)  # 测试案例中配置的并发案例个数(即Excel中sheet个数)
        for j, result in enumerate(_results):
            dt_startime = result.startTime
            dt_stoptime = result.stopTime
            startime = dt_startime if dt_startime < startime else startime  # 获取更小的时间
            stopime = dt_stoptime if dt_stoptime > stopime else stopime  # 获取更大的时间
            total_success_count += result.success_count
            total_failure_count += result.failure_count
            total_error_count += result.error_count
            total_results.extend(result.result)
    ReMakeReport.startTime = startime
    ReMakeReport.stopTime = stopime
    ReMakeReport.success_count = total_success_count
    ReMakeReport.failure_count = total_failure_count
    ReMakeReport.error_count = total_error_count
    ReMakeReport.title = Config.title
    ReMakeReport.description = Config.description
    ReMakeReport.test_method_results = total_results
    ReMakeReport.test_plan_results = test_plan_results


# 写报告
def write_report() -> str:
    # 如果配置不生成报告则直接返回None
    if not Config.genReport:
        return
    # 报告相关信息
    reportparentdir = ReportInfo.reportparentdir
    reportpath = ReportInfo.reportpath
    os.mkdir(reportparentdir)
    with open(reportpath, "wb") as fp:
        htmlTestRunner = HTMLTestRunner(stream=fp, title=Config.title, description=Config.description)
        htmlTestRunner.startTime = ReMakeReport.startTime
        htmlTestRunner.stopTime = ReMakeReport.stopTime
        htmlTestRunner.title = ReMakeReport.title
        htmlTestRunner.description = ReMakeReport.description
        htmlTestRunner.generateReport(test=None, result=ReMakeReport)
    # 2018年10月10日 zz：将projectDir/src/css&js/下资源文件copy到报告html相同目录下
    src_css = os.path.join(Config.projectDir, "src", "css&js", "bootstrap.min.css")
    src_js = os.path.join(Config.projectDir, "src", "css&js", "echarts.common.min.js")
    shutil.copy2(src=src_css, dst=reportparentdir)
    shutil.copy2(src=src_js, dst=reportparentdir)
    archivefilename = Public().make_archive(
        base_name=reportparentdir,
        format="zip",
        root_dir=reportparentdir
    )  # 压缩报告
    return archivefilename


# 构造测试集
def make_test_case() -> Tuple[Tuple]:
    try:
        logger.info("构建测试用例开始")
        # 按照Excel配置运行
        allsuites = testPlan()
        logger.info("构建测试用例完毕")
        return allsuites
    except Exception:
        logger.error("测试用例构建失败。报错信息:\n" + traceback.format_exc())


# 每个进程运行方法
def run(suite):
    # 2018年9月6日 zz：加上进程号
    # pid = current_process().pid  # 当前进程号
    # 不生成测试报告运行
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    # 生成测试报告运行
    # 2018年9月9日 zz: 增加案例执行失败异常保护
    # 2018年9月17日 zz: 调整为多进程生成一份测试报告
    try:
        runner = HTMLTestRunner(
            # stream=fp,
            # title=Config.title,
            # description=Config.description,
            report=False  # 默认不输出报告，测试计划执行完后再重制报告并输出报告
        )
        result = runner.run(suite)
    except Exception:
        logger.error("案例执行失败。报错信息:\n" + traceback.format_exc())
    return result


# 运行前的初始化工作
def init():
    try:
        logger.info("执行前初始化执行开始")
        # 1. 检查目录
        tempimgpath = os.path.join(Config.projectDir, "Report", "tempimg")  # 截图的临时目录
        if os.path.exists(tempimgpath):
            shutil.rmtree(tempimgpath)
            os.mkdir(tempimgpath)
        else:
            os.mkdir(tempimgpath)
        logdir = os.path.join(Config.projectDir, "Log")  # 日志目录
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        # 2. 重置数据
        xml = ParseXml(filepath=os.path.join(Config.projectDir, "automation.data"))
        build_num = xml.get_value_from_xpath(xpath="./BuildData/BuildCount", attribute="count")
        build_num = int(build_num) + 1
        xml.set_value_from_xpath(xpath="./BuildData/BuildCount", attribute="count", value=str(build_num))
        date, time = ReportInfo.time.split("_")
        xml.set_value_from_xpath(xpath="./BuildData/LastBuildDate", attribute="date", value=date)
        xml.set_value_from_xpath(xpath="./BuildData/LastBuildDate", attribute="time", value=time)
        logger.info("执行前初始化执行完毕")
    except Exception:
        logger.error("测试用例构建失败。报错信息:\n" + traceback.format_exc())


# 发送报告
# 2018年9月16日 zz: 邮件发送单独拿到一个函数中
def send_report(attchpath: str, info: ReMakeReport):
    """
    :param filepath: 附件路径
    :param info: 报告信息，用于邮件正文展示关键信息
    """
    # 邮件发送
    try:
        if Config.sendEmail:
            logger.info("邮件发送开始")
            sendEmail(attchpath, info)  # 发送邮件
            logger.info("邮件发送结束")
    except Exception:
        logger.error("邮件发送失败。报错信息:\n" + traceback.format_exc())


def main():
    # 运行前的初始化工作
    init()
    # 构造并返回测试集
    allsuites = make_test_case()  # type: Tuple[Tuple("suite")]
    # 多进程执行开始
    logger.info("测试执行开始")
    # 2018年9月6日 zz: 修改使用pool进程池，使得每个独立的进程可以返回执行结果。
    results = []  # 结果集
    # 遍历测试套件, 并使用多进程执行(for 循环为串行，suites为并行)
    for suites in allsuites:  # allsuites <类型 tuple of tuple>
        pool = Pool(len(suites) + 1)
        logger.info("执行测试套件：" + "".join([suite.__repr__() for suite in suites]))
        rl = pool.map(func=run, iterable=suites)  # 返回run方法的返回值 # suites内的测试案例在多进程执行时，logger记录日志会记录在一个文件。（可能是每次pool.map会公用一个logger句柄）
        pool.close()  # 关闭进程池，不再接受新的进程
        pool.join()   # 主进程阻塞等待子进程的退出
        results.append(rl)
    # 重制报告内容
    remake_report(results=results)
    # 写报告
    archivefilename = write_report()
    logger.info("测试执行结束")
    # 发送报告
    send_report(attchpath=archivefilename, info=ReMakeReport)


# 执行测试集
if __name__ == "__main__":
    main()