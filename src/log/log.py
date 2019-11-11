# coding:utf-8

import logging
import sys
import os
from datetime import datetime
from typing import Tuple, Union

from src.public.decorators import Singleton
from src.public.console import Color
from src.config.logconfig import Config


if hasattr(sys, '_getframe'):
    # 0-当前frame, 1-self._get_callerframe_info, 2-self._message_format, 3.self.debug/info/warning/error, 4. caller
    callerframe = lambda: sys._getframe(4)
else: #pragma: no cover
    def callerframe():
        """Return the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back.f_back.f_back.f_back


@Singleton
class Log(object):

    def __init__(self):
        self.logger = logging.getLogger()
        today = datetime.now().strftime("%Y%m%d")
        ch = logging.StreamHandler()  # 控制台输出
        fh = logging.FileHandler(
            filename=(Config.projectDir + "\\Log\\log_" + today + ".log"),
            encoding="utf-8",
        )  # 文件输出
        # 添加Handler
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        self.logger.setLevel(Config.loggingLevel)

    def _get_callerframe_info(self) -> Tuple[str, str, int]:
        """
        :return: 代码文件路径, 函数名, 行号
        """
        f = callerframe()
        co = f.f_code
        return co.co_filename, co.co_name, f.f_lineno

    def _message_format(self, level: str, msg: str) -> str:
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        file, func, lineno = self._get_callerframe_info()
        lineno = str(lineno)
        file = os.path.basename(file)
        file_func_lineno = file + "-" + func + "-" + lineno
        # 格式化输出
        return "{time:<29}{level:<10}{file_func_lineno:<40}{msg}".format(time="["+time+"]",
                                                                         level="["+level+"]",
                                                                         file_func_lineno="["+file_func_lineno+"]",
                                                                         msg="[信息:"+msg+"]")

    def debug(self, msg: str, *args, **kwargs) -> Union[None]:
        msg = self._message_format(level="DEBUG", msg=msg)
        Color.white_bright_foreground_black_background()
        self.logger.debug(msg, *args, **kwargs)
        Color.white_foreground_black_background()

    def info(self, msg: str, *args, **kwargs) -> Union[None]:
        msg = self._message_format(level="INFO", msg=msg)
        Color.white_foreground_black_background()
        self.logger.info(msg, *args, **kwargs)
        Color.white_foreground_black_background()

    def warning(self, msg: str, *args, **kwargs) -> Union[None]:
        msg = self._message_format(level="WARNING", msg=msg)
        Color.yellow_foreground_black_background()
        self.logger.warning(msg, *args, **kwargs)
        Color.white_foreground_black_background()

    def error(self, msg: str, *args, **kwargs) -> Union[None]:
        msg = self._message_format(level="ERROR", msg=msg)
        Color.red_foreground_black_background()
        self.logger.error(msg, *args, **kwargs)
        Color.white_foreground_black_background()

    def critical(self, msg: str, *args, **kwargs) -> Union[None]:
        msg = self._message_format(level="CRITICAL", msg=msg)
        Color.red_bright_foreground_black_background()
        self.logger.critical(msg, *args, **kwargs)
        Color.white_foreground_black_background()