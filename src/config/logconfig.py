# coding=utf-8

"""
作者：张正
文件名：logconfig.py
文档描述：
最近修改：2018年6月24日
修改记录：
    1、2018年6月24日 1) 将confing.ini log相关配置获取移动至logconfig.py文件中
                    2) 对配置读取时做异常保护，并输出至日志
    2、2019年8月23日 1) 优化日志模块记录逻辑

"""

import configparser
from configparser import NoOptionError, NoSectionError
import os
import logging
import codecs

from src.public.public import Public
from src.exception.seleniumexecption import SeleniumTypeError

G_projectdir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)


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
    def loggingLevel(self):
        try:
            level = self.returnConfig().get(section="LOG", option="loggingLevel")
        except (NoOptionError, NoSectionError):
            level = "INFO"
        if str.upper(level) == "DEBUG":
            return logging.DEBUG
        elif str.upper(level) == "INFO":
            return logging.INFO
        elif str.upper(level) == "WARN" or str.upper(level) == "WARNING":
            return logging.WARNING
        elif str.upper(level) == "CRITICAL" or str.upper(level) == "FATAL":
            return logging.CRITICAL
        elif str.upper(level) == "ERROR":
            return logging.ERROR
        else:
            raise SeleniumTypeError(
                '配置文件中定义的日志级别loggingLevel为"%s",请填写以下几种级别“INFO、DEBUG、WARNING、ERROR、CRITICAL”'
                % level
            )


class Config(object):
    # 项目路径
    projectDir = GetConfig().projectDir
    # 配置输出日志级别
    loggingLevel = GetConfig().loggingLevel
