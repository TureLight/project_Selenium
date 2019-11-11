# coding=utf-8

"""
Author: zhangzheng
Description: Get Windows "regedit" information
Version: 0.0.1
LastUpdateDate: 2019-7-31
UpadteURL:
LOG:
    2019-7-31 Create an AbstractBaseClass
"""

import winreg


class Regedit(object):

    @classmethod
    def get_value(cls, path, name=""):
        """
            根据路径与名称来获取值
             “(默认)”的名称的数据通过传入name="(默认)"来获取
        :param path: 路径，可以通过右键“复制项名称”获得
        :param name: “名称”
        :return:
        """
        hkey, sub_path = path.split("\\", 1)
        if hkey == "HKEY_CLASSES_ROOT": key = winreg.HKEY_CLASSES_ROOT
        if hkey == "HKEY_CURRENT_CONFIG": key = winreg.HKEY_CURRENT_CONFIG
        if hkey == "HKEY_CURRENT_USER": key = winreg.HKEY_CURRENT_USER
        if hkey == "HKEY_DYN_DATA": key = winreg.HKEY_DYN_DATA
        if hkey == "HKEY_LOCAL_MACHINE": key = winreg.HKEY_LOCAL_MACHINE
        if hkey == "HKEY_PERFORMANCE_DATA": key = winreg.HKEY_PERFORMANCE_DATA
        if hkey == "HKEY_USERS": key = winreg.HKEY_USERS
        open_key = winreg.OpenKey(key, sub_path)
        if name == "(默认)": name = ""
        return winreg.QueryValueEx(open_key, name)[0]

    @classmethod
    def get_uninstall_apps(cls):
        """
            返回注册表中所有的程序列表
            问题：
                1. 和控制面板中的程序列表不一致
        """
        ret = []
        bit64_app_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        bit32_app_path = r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        app_paths = [bit64_app_path, bit32_app_path]
        open_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bit64_app_path)
        count = 0
        for app_path in app_paths:
            while True:
                try:
                    count += 1
                    sub_key_name = winreg.EnumKey(open_key, count)
                    sub_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, app_path + "\\" + sub_key_name)
                    displayname = winreg.QueryValueEx(sub_key, r"DisplayName")
                    ret.append(displayname)
                except OSError as e:
                    if e.winerror == 259:  # <class 'tuple'>: (22, '没有可用的数据了。', None, 259, None)
                        break
                    elif e.winerror == 2:  # <class 'tuple'>: (2, '系统找不到指定的文件。', None, 2, None)
                        # print(sub_key_name + " 的 DisplayName 不存在")
                        pass
                    else:
                        raise
        return ret


if __name__ == '__main__':
    print(Regedit.get_uninstall_apps())
    print(Regedit.get_value(r"HKEY_CURRENT_CONFIG\Software\Fonts", name="LogPixels"))
