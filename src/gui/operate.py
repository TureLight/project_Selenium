# coding=utf-8

import autoit  # https://github.com/jacexh/pyautoit/blob/master/autoit
from autoit.autoit import Properties
from typing import Union

INTDEFAULT = -2147483647


class Operate(object):
    @classmethod
    def run(cls, filename: str, work_dir: str ="", show_flag: str =Properties.SW_SHOWNORMAL):
        """
        说明：运行外部程序.
        :param filename: 运行程序的完整路径(文件类型: EXE, BAT, COM, 或 PIF.).
        :param work_dir: [可选参数] 工作目录. 不是程序的路径.
        :param show_flag: [可选参数] 程序执行时的显示状态:
        :return:
            success: 返回运行程序的 PID(进程标识符).
            fail:    返回 0.
        """
        return autoit.run(filename=filename,
                          work_dir=work_dir,
                          show_flag=show_flag)

    @classmethod
    def run_wait(cls, filename: str, work_dir: str ="", show_flag: int =Properties.SW_SHOWNORMAL):
        """
        说明：运行外部程序并暂停脚本执行，直到程序结束.
        :param filename: 运行程序的完整路径(文件类型: EXE, BAT, COM, 或 PIF
        :param work_dir: [可选参数] 工作目录, 不是程序的路径.
        :param show_flag: [可选参数] 程序执行时的显示状态:
        :return:
            success: 返回程序的退出代码.
            fail:    返回 0.
        """
        return autoit.run_wait(filename=filename,
                               work_dir=work_dir,
                               show_flag=show_flag)


    @classmethod
    def mouse_click(cls,
                    button: str = "left",
                    x: int = INTDEFAULT,
                    y: int = INTDEFAULT,
                    clicks: int = 1,
                    speed: int = -1):
        """
        说明：执行鼠标点击操作
        :param button:
            用于点击操作的按钮:
            "left" = 左键
            "right" = 右键
            "middle" = 中键
            "main" = 主要
            "menu" = 菜单
            "primary" = 主键
            "secondary" = 次键
        :param x: [可选参数] 点击目标的 X/Y 坐标值. 若两者都留空, 则使用当前位置(默认).
        :param y: [可选参数] 点击目标的 X/Y 坐标值. 若两者都留空, 则使用当前位置(默认).
        :param clicks: [可选参数] 鼠标按钮点击的次数. Default(默认) = 1.
        :param speed: [可选参数] 鼠标移动速度. 可设数值范围在 1(最快)和 100(最慢)之间.
                      若设置速度为 0, 则立即移动鼠标到指定位置. Default(默认) = 10.
        :return:
            success: 返回 1.
            fail:    返回 0, 按钮不在列表中, 或者使用了无效的参数.
        """
        return autoit.mouse_click(button=button, x=x, y=y, clicks=clicks, speed=speed)

    @classmethod
    def mouse_click_drag(cls,
                         x1: int,
                         y1: int,
                         x2: int,
                         y2: int,
                         button: str = "left",
                         speed: int = -1):
        """
        说明：执行鼠标单击并拖动操作.
        :param x1: 拖动操作开始的 X/Y 坐标值.
        :param y1: 拖动操作开始的 X/Y 坐标值.
        :param x2: 拖动操作结束的 X/Y 坐标值.
        :param y2: 拖动操作结束的 X/Y 坐标值.
        :param button:
            用于点击操作的按钮:
            "left" = 左键
            "right" = 右键
            "middle" = 中键
            "main" = 主要
            "menu" = 菜单
            "primary" = 主键
            "secondary" = 次键
        :param speed: [可选参数] 鼠标移动速度. 可设数值范围在 1(最快)和 100(最慢)之间.
                    若设置速度为 0, 则立即移动鼠标到指定位置. Default(默认) = 10.
        :return:
            success: 返回 1.
            fail:    返回 0, 鼠标按钮不在列表内.
        """
        return autoit.mouse_click_drag(x1=x1,
                                       y1=y1,
                                       x2=x2,
                                       y2=y2,
                                       button=button,
                                       speed=speed)

    @classmethod
    def mouse_down(cls, button: str ="left"):
        """
        说明：执行鼠标当前位置的按下事件(不松开按键).
        :param button:
            用于点击操作的按钮:
            "left" = 左键
            "right" = 右键
            "middle" = 中键
            "main" = 主要
            "menu" = 菜单
            "primary" = 主键
            "secondary" = 次键
        :return:
            success: 返回 1.
            fail:    返回 0, 按钮不在列表里面.
        """
        return autoit.mouse_down(button=button)

    @classmethod
    def mouse_move(cls, x: int, y: int, speed: int =-1):
        """
        说明：移动鼠标.
        :param x: 移动到屏幕的 X 坐标.
        :param y: 移动到屏幕的 Y 坐标.
        :param speed: [可选参数] 鼠标移动速度. 可设数值范围在 1(最快)和 100(最慢)之间.
                    若设置速度为 0, 则立即移动鼠标到指定位置. Default(默认) = 10
        :return: None
        """
        return autoit.mouse_move(x=x, y=y, speed=speed)

    @classmethod
    def mouse_up(cls, button: str ="left"):
        """
        说明：移动鼠标.
        :param button:
            用于点击操作的按钮:
            "left" = 左键
            "right" = 右键
            "middle" = 中键
            "main" = 主要
            "menu" = 菜单
            "primary" = 主键
            "secondary" = 次键
        :return:
            success: 返回 1.
            fail:    返回 0, 按钮不在列表里面.
        """
        return autoit.mouse_up(button=button)

    @classmethod
    def mouse_wheel(cls, direction: str, clicks: int =1):
        """

        :param direction: "up" or "down"
        :param clicks: [可选参数] 滚轮的滚动次数. Default(默认) = 1.
        :return:
            success: 返回 1.
            fail:    返回 0, "方向"参数值不正确.
        """
        return autoit.mouse_wheel(direction=direction, clicks=clicks)

    @classmethod
    def mouse_get_pos(cls):
        """
        说明：获取鼠标的当前坐标位置.
        :return: (x, y)
        :rtype: tuple
        """
        return autoit.mouse_get_pos()

    @classmethod
    def control_set_text(cls, title: str, control: str, control_text: str, **kwargs):
        """
        说明：设置控件文本.
        :param title: 目标窗口标题.
        :param control: 控件ID 控件标识符.
        :param control_text: 更新到控件的新文本.
        :param kwargs:
            text:目标窗口文本.
        :return:
        """
        return autoit.control_set_text(title=title,
                                       control=control,
                                       control_text=control_text,
                                       **kwargs)

    @classmethod
    def control_click(cls, title: str, control: str, **kwargs):
        """
        说明：发送鼠标点击命令到指定控件.
        :param title: 目标窗口标题.
        :param control: 控件标识符.
        :param text: 目标窗口文本.
        :param button: [可选参数] 点击使用的按钮,
            "left" = 左键
            "right" = 右键
            "middle" = 中键
            "main" = 主要
            "menu" = 菜单
            "primary" = 主键
            "secondary" = 次键
            默认使用 left(左键).
        :param clicks: [可选参数] 鼠标点击的次数. 默认为 1 次.
        :param x: [可选参数] 点击控件的 X 坐标位置. 默认为控件中心.
        :param y: [可选参数] 点击控件的 Y 坐标位置. 默认为控件中心.
        :return:
        """
        return autoit.control_click(title=title, control=control, **kwargs)

    @classmethod
    def win_activate(cls, title: str, **kwargs):
        """
        说明：激活指定窗口.
        :param title: 目标窗口标题
        :param kwargs:
            text: [可选参数] 目标窗口文本.
        :return:
            success: 返回 1.
            fail:    返回 0. 窗口没有找到或不能被激活.
        """
        return autoit.win_activate(title=title, **kwargs)

    @classmethod
    def win_active(cls, title: str, **kwargs):
        """
        说明：检查窗口是否被激活
        :param title: 目标窗口标题.
        :param kwargs:
            text: [可选参数] 目标窗口文本.
        :return:
            success: 如果窗口为激活状态, 则返回窗口句柄.
            fail:    返回 0, 未激活 或 其它(错误).
        """
        return autoit.win_active(title=title, **kwargs)

    @classmethod
    def win_wait_active(cls, title: str, timeout: int = 0, **kwargs):
        """
        说明：暂停脚本执行,直到请求的窗口激活.
        :param title: 目标窗口标题.
        :param timeout: [可选参数] 暂停时间(秒)
        :param kwargs:
        :return:
            success: 返回 1.
            fail:    返回 0, 已超时.
        """
        return autoit.win_wait_active(title=title, timeout=timeout, **kwargs)

    @classmethod
    def win_exists(cls, title: str, **kwargs):
        """
        说明：检查指定窗口是否存在.
        :param title: 目标窗口标题.
        :param text: [可选参数] 目标窗口文本.
        :return:
            success: 返回 1, 窗口存在.
            fail:    返回 0, 其它(错误).
            　———————————————————————————————
            ｜ 提示         　                 ｜
            ｜                                ｜
            ｜　    未找此到内容，是否关闭       ｜
            ｜                                ｜
            ｜                    是     否    ｜
            　————————————————————————————————
        示例：
            Operate.win_exists(title="提示", text="未找此到内容，是否关闭")
        """
        return autoit.win_exists(title=title, **kwargs)

    @classmethod
    def win_close(cls, title: str, **kwargs):
        """
        说明：关闭指定窗口.
        :param title: 目标窗口标题.
        :param kwargs:
            text: [可选参数] 目标窗口文本.
        :return:
            success: 返回 1.
            fail:    返回 0, 窗口不存在.
        """
        return autoit.win_close(title=title, **kwargs)

    @classmethod
    def win_get_handle(cls, title: str, **kwargs) -> Union[int, str]:
        """
        说明：获取窗口句柄.
        :param title: 目标窗口标题.
        :param kwargs:
            text: [可选参数] 目标窗口文本.
        :return:
            success: 返回目标窗口句柄.
            fail:    返回空字符串""
        """
        return autoit.win_get_handle(title=title, **kwargs)

    @classmethod
    def win_get_pos(cls, title, **kwargs):
        """
        说明：获取窗口的坐标位置和大小.
        :param title: 目标窗口标题.
        :param kwargs:
            text: [可选参数] 目标窗口文本.
        :return:
            success: (X坐标, Y坐标, 宽度, 高度)
            fail:   返回 0
        """
        return autoit.win_get_pos(title=title, **kwargs)


if __name__ == "__main__":
    # print(Operate.win_close("AutoIt 帮助 By 131738 汉化"))
    # print(autoit.win_get_pos("AutoIt 帮助 By 131738 汉化"))
    # print(autoit.win_get_handle("AutoIt 帮助 By 131738 汉化"))
    print(Operate.win_get_handle.__annotations__)