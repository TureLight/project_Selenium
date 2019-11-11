# coding=utf-8

import smtplib
from email.mime.text import MIMEText  # 正文文本
from email.mime.multipart import MIMEMultipart
from email.header import Header
import traceback
import sys
import os

from src.log.log import Log
from src.config.config import Config
from src.report.reporthtml import ReportHtml
from src.public.public import ParseXml

logger = Log()

USER = Config.SMTPLoginName  # SMTP服务器登录名
PASSWORD = Config.SMTPLoginPasswd  # SMTP服务器登录密码
SENDER_ADDRESS = Config.senderAddress  # 发件地址
RECEIVERS = Config.receiversAddress  # 收件地址
SMTP_SERVER = Config.SMTPServerAddress  # SMTP服务器地址
SMTP_PORT = Config.SMTPPort  # SMTP服务器地址端口


HTML = ""
HTML_HEAD_TITLE = ""
HTML_BODY_TABLE = ""
HTML_BODY_TABLE_TBODY_TR = ""


def exit(errmsg):
    logger.error(errmsg)
    os.system("pause")
    sys.exit(0)


def get_html_text(attch_name, info):
    """
    说明：将报告信息已html文本返回
    :param attch_name: 附件名
    :param info: 报告信息，用于邮件正文展示关键信息
    :return: html文本
    :rtype: str
    """
    global HTML, HTML_HEAD_TITLE, HTML_BODY_TABLE, HTML_BODY_TABLE_TBODY_TR
    xml = ParseXml(filepath=os.path.join(Config.projectDir, "automation.data"))
    BUILD_NUMBER = xml.get_value_from_xpath(xpath="./BuildData/BuildCount", attribute="count")
    test_plan_results = info.test_plan_results
    total_success_count = 0
    total_failure_count = 0
    total_error_count = 0
    for _results in test_plan_results:
        test_plan_name = _results[0].file_name
        success_count = 0
        failure_count = 0
        error_count = 0
        for _res in _results:
            success_count += _res.success_count
            failure_count += _res.failure_count
            error_count += _res.error_count
        HTML_BODY_TABLE_TBODY_TR += ReportHtml.HTML_BODY_TABLE_TBODY_TR % {
            'TEST_PLAN_NAME': test_plan_name,
            'TEST_PLAN_CASE_COUNT': success_count + failure_count + error_count,
            'TEST_PLAN_SUCCESS_COUNT': success_count,
            'TEST_PLAN_FAILURE_COUNT': failure_count + error_count,
            'TEST_PLAN_SUCCESS_RATE': success_count / (success_count + failure_count + error_count),
            'TEST_PLAN_FAILURE_RATE': (failure_count + error_count) / (success_count + failure_count + error_count),
        }
        total_success_count += success_count
        total_failure_count += failure_count
        total_error_count += error_count

    HTML_HEAD_TITLE = ReportHtml.HTML_HEAD_TITLE % {
        'BUILD_NUMBER': BUILD_NUMBER,
    }

    HTML_BODY_TABLE = ReportHtml.HTML_BODY_TABLE % {
        'BUILD_STATUS': '构建成功',
        'PROJECT_NAME': 'Web自动化项目',
        'BUILD_NUMBER': BUILD_NUMBER,
        'CAUSE': '手工触发',
        'HTML_BODY_TABLE_TBODY_TR': HTML_BODY_TABLE_TBODY_TR,
        'CASE_COUNT': total_success_count + total_failure_count + total_error_count,
        'SUCCESS_COUNT': total_success_count,
        'FAILURE_COUNT': total_failure_count + total_error_count,
        'SUCCESS_RATE': total_success_count / (total_success_count + total_failure_count + total_error_count),
        'FAILURE_RATE': (total_failure_count + total_error_count) / (total_success_count + total_failure_count + total_error_count),
        'ATTACHED_FILE': attch_name,
    }

    HTML = ReportHtml.HTML % {
        'HTML_HEAD_TITLE': HTML_HEAD_TITLE,
        'HTML_BODY_TABLE': HTML_BODY_TABLE,
    }
    return HTML


def sendEmail(attchpath, info):
    """
    说明：
        发送邮件
    :param attchpath: 附件文件路径
    :param info: 报告信息，用于邮件正文展示关键信息
    """
    if attchpath:
        attch_name = os.path.basename(attchpath)
        attch_file = [
            {"path": attchpath, "name": attch_name}
        ]  # 添加多个附件
    else:
        attch_file = False
        attch_name = "无附件"

    message = MIMEMultipart()  # 创建一个带附件的实例
    # 下面三个为邮件发送时显示的发件人、收件人和邮件主题
    message["From"] = SENDER_ADDRESS  # 发件地址
    message["To"] = ",".join(RECEIVERS)  # 收件地址 字符串 多个地址用逗号隔开
    message["Subject"] = Header(Config.emailTitle, "utf-8")  # 邮件主题
    # 三个参数：第一个为文本内容，第二个 plain or html 设置文本格式，第三个 utf-8 设置编码
    html_text = get_html_text(attch_name, info)
    message.attach(MIMEText(html_text, 'html', 'utf-8'))  # 正文内容 Html格式
    # message.attach(MIMEText("test", 'plain', 'utf-8'))  # 正文内容 plain 文本格式

    # 构造附件
    if attch_file:
        for item in attch_file:
            att = MIMEText(open(item["path"], "rb").read(), "base64", "utf-8")  # 创建二进制流
            att["Content-Type"] = ("application/octet-stream")
            # Content-Type，内容类型，一般是指网页中存在的Content-Type，
            # 用于定义网络文件的类型和网页的编码，决定浏览器将以什么形式、什么编码读取这个文件，
            # 这就是经常看到一些Asp网页点击的结果却是下载到的一个文件或一张图片的原因。
            # (引用:http://www.runoob.com/http/http-content-type.html)
            att.add_header(
                "Content-Disposition",
                "attachment",
                filename=("utf-8", "", item["name"]),
            )
            message.attach(att)  # 添加附件

    # 连接SMTP服务器
    try:
        logger.info("开始连接SMTP服务器...")
        smtpObj = smtplib.SMTP(
            SMTP_SERVER, SMTP_PORT
        )  # 这里填写发送邮件的SMTP服务器地址 返回<class 'smtplib.STMP'>
        info_msg = smtpObj.ehlo()  # 查看是否连接服务器成功 返回一个元祖，第一个元素为应答号 250表示链接SMTP服务器成功
        if info_msg[0] == 250:
            logger.info("连接SMTP服务器成功...")
        else:
            exit("连接SMTP服务器失败...\n" + "详细信息:\n" + str(info_msg))
    except Exception:
        exit("连接SMTP服务器失败...\n" + "详细信息:\n" + traceback.format_exc())

    # 开始TLS加密 (587端口)
    smtpObj.starttls()  # 使用TLS加密传输必须使用此方法，否则无法登陆

    # 登录SMTP服务器
    try:
        logger.info(USER + "开始登录SMTP服务器...")
        # 注意： 一般情况下登录地址为邮箱，但不排除非邮箱地址登录的情况。
        login_msg = smtpObj.login(user=USER, password=PASSWORD)  # 返回元祖 一个元素应答 235表示成功
        if login_msg[0] == 235:
            logger.info(USER + "登录SMTP服务器成功...")
        else:
            exit("登录SMTP服务器失败...\n" + "详细信息:\n" + login_msg)
    except Exception:
        exit("登录SMTP服务器失败...\n" + "详细信息:\n" + traceback.format_exc())

    # 发送邮件
    try:
        logger.info("开始发送邮件...")
        smtpObj.sendmail(
            from_addr=SENDER_ADDRESS, to_addrs=RECEIVERS, msg=message.as_string()
        )
        smtpObj.quit()
        logger.info("邮件发送成功...")
    except Exception:
        exit("邮件发送失败，详细信息:\n" + "详细信息:\n" + traceback.format_exc())


# if __name__ == "__main__":
#     sendEmail(attchpath=None, info=None)