# coding=utf-8

"""
作者：张正
文件名：config.py
文档描述：
最近修改：2018年11月20日
修改记录：
    1、2018年6月24日  1) 将confing.ini log相关配置获取移动至logconfig.py文件中
                     2) 对配置读取时做异常保护，并输出至日志
    2、2018年11月20日 1) 增加config.ini文件DATABASE.dbType配置项
    3、2019年8月23日 1) 优化日志模块记录逻辑

"""

import configparser
from configparser import NoOptionError, NoSectionError
import os
import codecs

from src.public.public import Public
from src.log.log import Log

G_projectdir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)

logger = Log()


class GetConfig(object):
    def returnConfig(self):
        config = configparser.ConfigParser()
        config_path = G_projectdir + r"\Config\config.ini"

        with open(
            file=config_path, mode="rb"
        ) as f:  # 2018-6-10 BEGIN 判断文件的编码类型 如果是UTF-8 BOM格式，则将其转化为无BOM格式
            s = f.read()
        if s.startswith(codecs.BOM_UTF8):  # 带BOM的文件是以 b'\xef\xbb\xbf' 开头
            s = s[len(codecs.BOM_UTF8) :]  # 截取 b'\xef\xbb\xbf' 到文件结尾
            with open(file=config_path, mode="wb") as f:  # 保存为无BOM格式
                f.write(s)
        coding = Public().getFileCoding(filepath=config_path).get("encoding")
        config.read(
            filenames=config_path, encoding=coding
        )  # 2018-6-10 END 判断文件的编码类型 如果是UTF-8 BOM格式，则将其转化为无BOM格式
        return config

    @property
    def projectDir(self):
        # return self.returnConfig().get(section="PROJECT", option="projectDir")
        # 不在需要配置项目路径，项目迁移更加灵活。
        return G_projectdir

    @property
    def browserType(self):
        try:
            browsertype = self.returnConfig().get(
                section="PROJECT", option="browserType"
            )
        except (NoOptionError, NoSectionError):
            browsertype = "Chrome"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 PROJECT.browserType 选项，将采用默认值"%s"' %
                browsertype
            )
        return browsertype

    @property
    def browserPath360(self):
        try:
            browser_path_360 = self.returnConfig().get(
                section="PROJECT", option="360BrowserPath"
            )
        except (NoOptionError, NoSectionError):
            browser_path_360 = None
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 PROJECT.browserPath360 选项，将采用默认值"%s"' %
                browser_path_360
            )
        return browser_path_360


    @property
    def timeOut(self):
        try:
            timeout = self.returnConfig().getint(section="TEST", option="timeOut")
        except (NoOptionError, NoSectionError):
            timeout = 10
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 TEST.timeOut 选项，将采用默认值"%s"' % timeout
            )
        return timeout

    @property
    def headLess(self):
        try:
            headless = self.returnConfig().getboolean(section="TEST", option="headLess")
        except (NoOptionError, NoSectionError):
            headless = False
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 TEST.headLess 选项，将采用默认值"%s"' %
                headless
            )
        return headless

    @property
    def sendEmail(self):
        try:
            sendemail = self.returnConfig().getboolean(
                section="EMAIL", option="sendEmail"
            )
        except (NoOptionError, NoSectionError):
            sendemail = False
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 EMAIL.sendEmail 选项，将采用默认值"%s"' %
                sendemail
            )
        return sendemail

    @property
    def genReport(self):
        try:
            genreport = self.returnConfig().getboolean(
                section="EMAIL", option="genReport"
            )
        except (NoOptionError, NoSectionError):
            genreport = True
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 EMAIL.genReport 选项，将采用默认值"%s"' %
                genreport
            )
        return genreport

    @property
    def SMTPLoginName(self):
        return self.returnConfig().get(section="EMAIL", option="SMTPLoginName")

    @property
    def SMTPLoginPasswd(self):
        return self.returnConfig().get(section="EMAIL", option="SMTPLoginPasswd")

    @property
    def senderAddress(self):
        return self.returnConfig().get(section="EMAIL", option="senderAddress")

    @property
    def receiversAddress(self):
        address = self.returnConfig().items(section="receiversAddress")  # [(,), (,)...]
        address_list = list(dict(address).values())
        ret = []
        for _address in address_list:
            for _address_splited in _address.split(";"):
                if _address_splited:
                    ret.append(_address_splited)
        return ret

    @property
    def SMTPServerAddress(self):
        return self.returnConfig().get(section="EMAIL", option="SMTPServerAddress")

    @property
    def SMTPPort(self):
        return self.returnConfig().getint(section="EMAIL", option="SMTPPort")

    @property
    def emailTitle(self):
        try:
            emailtitle = self.returnConfig().get(section="EMAIL", option="emailTitle")
        except (NoOptionError, NoSectionError):
            emailtitle = "Web自动化测试报告邮件"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 EMAIL.emailTitle 选项，将采用默认值"%s"' %
                emailtitle
            )
        return emailtitle

    @property
    def emailText(self):
        try:
            emailtext = self.returnConfig().get(section="EMAIL", option="emailText")
        except (NoOptionError, NoSectionError):
            emailtext = "详细测试报告请查看附件..."
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 EMAIL.emailText 选项，将采用默认值"%s"' %
                emailtext
            )
        return emailtext

    @property
    def title(self):
        try:
            title = self.returnConfig().get(section="REPORT", option="title")
        except (NoOptionError, NoSectionError):
            title = "Web自动化测试报告"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 REPORT.title 选项，将采用默认值"%s"' % title
            )
        return title

    @property
    def description(self):
        try:
            description = self.returnConfig().get(
                section="REPORT", option="description"
            )
        except (NoOptionError, NoSectionError):
            description = "报告描述"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 REPORT.description 选项，将采用默认值"%s"' %
                description
            )
        return description

    @property
    def dbtype(self):
        try:
            dbtype = self.returnConfig().get(
                section="DATABASE", option="dbType"
            )
        except (NoOptionError, NoSectionError):
            dbtype = "MySQL"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 DATABASE.dbType 选项，将采用默认值"%s"' %
                dbtype
            )
        return dbtype

    @property
    def DSN(self):
        section = "ORACLE"
        option = "DSN"
        try:
            DSN = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            DSN = "DSN_Oracle"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, DSN)
            )
        return DSN

    @property
    def userName(self):
        section = "ORACLE"
        option = "userName"
        try:
            userName = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            userName = "sys"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, userName)
            )
        return userName

    @property
    def passWord(self):
        section = "ORACLE"
        option = "passWord"
        try:
            passWord = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            passWord = "1"
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, passWord)
            )
        return passWord

    @property
    def host(self):
        section = "MYSQL"
        option = "host"
        default = "localhost"
        try:
            value = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            value = default
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, value)
            )
        return value

    @property
    def user(self):
        section = "MYSQL"
        option = "user"
        default = "root"
        try:
            value = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            value = default
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, value)
            )
        return value

    @property
    def passwd(self):
        section = "MYSQL"
        option = "passwd"
        default = "root"
        try:
            value = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            value = default
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, value)
            )
        return value

    @property
    def port(self):
        section = "MYSQL"
        option = "port"
        default = 3306
        try:
            value = self.returnConfig().getint(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            value = default
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, value)
            )
        return value

    @property
    def charset(self):
        section = "MYSQL"
        option = "charset"
        default = 'utf8'
        try:
            value = self.returnConfig().get(
                section=section, option=option
            )
        except (NoOptionError, NoSectionError):
            value = default
            logger.warning(
                '...\\项目目录\\Config\\config.ini文件未配置 %s.%s 选项，将采用默认值"%s"' %
                (section, option, value)
            )
        return value


class Config(object):
    # 项目路径
    projectDir = GetConfig().projectDir
    # 配置隐形等待时间
    timeOut = GetConfig().timeOut
    # 无头模式运行
    headLess = GetConfig().headLess

    # 案例运行浏览器类型
    browserType = GetConfig().browserType  # Firefox\Chrome\360
    browserPath360 = GetConfig().browserPath360

    # Email
    # 是否发送邮件
    sendEmail = GetConfig().sendEmail
    # 是否生成报告
    genReport = GetConfig().genReport
    # SMTP服务器登录名
    SMTPLoginName = GetConfig().SMTPLoginName
    # SMTP服务器登录密码
    SMTPLoginPasswd = GetConfig().SMTPLoginPasswd
    # 发件地址
    senderAddress = GetConfig().senderAddress
    # 收件地址
    receiversAddress = GetConfig().receiversAddress
    # SMTP服务器地址
    SMTPServerAddress = GetConfig().SMTPServerAddress
    # SMTP服务器地址端口
    SMTPPort = GetConfig().SMTPPort
    # 邮件主题
    emailTitle = GetConfig().emailTitle
    # 正文内容
    emailText = GetConfig().emailText

    # 报告的标题
    title = GetConfig().title
    # 报告的描述
    description = GetConfig().description

    # 数据库类型
    dbtype = GetConfig().dbtype
    # Oracle DSN配置
    DSN = GetConfig().DSN
    userName = GetConfig().userName
    passWord = GetConfig().passWord
    # MySQL 配置
    host = GetConfig().host
    user = GetConfig().user
    passwd = GetConfig().passwd
    port = GetConfig().port
    charset = GetConfig().charset


# if __name__ == "__main__":
#     print(",".join(Config.receiversAddress))