# coding=utf-8

"""
Author: zhangzheng
Description: Provide Decorator To Function And Class
Version: 0.0.1
LastUpdateDate: 2019-8-22
UpadteURL: 
LOG: 2019-8-22 提供单例装饰器
"""


class Singleton(object):
    """
        单例模式（装饰类的类装饰器）
    """

    instances = {}

    def __init__(self, cls: type):
        self.cls = cls
        self.cls_name = cls.__name__

    def __call__(self, *args, **kwargs):
        if self.cls_name not in __class__.instances:
            __class__.instances[self.cls_name] = self.cls(*args, **kwargs)
        return __class__.instances[self.cls_name]
