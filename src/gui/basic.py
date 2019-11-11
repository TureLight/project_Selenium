# encoding = utf-8

import os
import subprocess

from src.exception.seleniumexecption import CMDRunError
from src.public.public import monitor_run_timeout


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
AUTOIT_DIR = os.path.join(PROJECT_DIR, "AutoIt")
AUTOIT_EXE = "AutoIt3_x64.exe"


def _create_script(file_name: str, content: str):
    file_path = os.path.join(AUTOIT_DIR, file_name)
    if os.path.exists(file_path):
        raise FileExistsError("目录%s下存在相同的脚本文件%s，请先删除再创建。" % (AUTOIT_DIR, file_name))
    with open(file=os.path.join(AUTOIT_DIR, file_name), mode="w", encoding='utf-8') as file:
        file.write(content)


def run_autoit(file_name: str, cmdline: str = "", timeout: int = 10):
    """
    执行\AutoIt下的autoit脚本
    :param file_name: 脚本名
    :param cmdline: 参数
    :param timeout: 执行超时时间
    :return: subprocess.run的执行结果
    """
    cmd_str = os.path.join(AUTOIT_DIR, AUTOIT_EXE) + " " + os.path.join(AUTOIT_DIR, file_name) + " " + cmdline

    def run():
        _result = subprocess.run(args=cmd_str,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True,
                                 timeout=timeout)
        return _result
    # def run 构造了一个闭包环境供下面多线程调用传入fn=run
    # 这里使用monitor_run_timeout方法监控run方法的运行时间，当运行超时时，raise TimeoutError
    result = monitor_run_timeout(fn=run,
                                 timeout=timeout,
                                 timeout_message="执行CMD命令“%s”超时。\n设置的超时时间为%ss。" % (cmd_str, timeout))

    if result.returncode != 0:
        raise CMDRunError("执行CMD命令“%s”出现异常\n错误信息：\n%s" % (result.args, result.stderr))
