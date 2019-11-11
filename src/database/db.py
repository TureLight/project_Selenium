# coding:utf-8

"""
作者：azheng
文件名：db.py
最近修改：2018年12月26日
文档描述：
    编写一个方便访问数据库的类，支持访问Oracle和MySQL
修改记录：
    2019年1月25日：
        1. 新增支持mysql数据库

"""

__author__ = "zhangzheng"

import os
import inspect
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Iterable, Union, List, Generator
import pyodbc
import pymysql
from pymysql.cursors import DictCursor, SSCursor
import pandas
from pandas import DataFrame, ExcelWriter

from src.config.config import Config
from src.exception.seleniumexecption import SeleniumTypeError
from src.database.compare import Compare


class DataType(object):
    DictCursor = 1  # 元祖包含字典
    SSCursor = 2    # 列表包含元祖


class AbstracDBClass(ABC):
    @abstractmethod
    def __init__(self):
        """
        数据库初始化
        需要读取对应数据的配置项
        """

    @abstractmethod
    def _read_config(self):
        """
        数据库初始化前需要先读取配置
        """

    @abstractmethod
    def _connect(self):
        """
        创建数据库连接
        """

    @abstractmethod
    def _data_convert_dataframe(self,
                                data: Iterable[OrderedDict],
                                data_type=DataType.DictCursor) -> DataFrame:
        """
        支持将查询数据转换为pandas.DataFrame类型
        """
        if data_type == DataType.DictCursor:
            df = pandas.DataFrame(data)
        else:
            df = None
        return df

    @abstractmethod
    def _table_name(self, sql: str) -> str:
        """
        说明：
            返回当前sql的表名，如果出现连表查询涉及多个表，则默认返回第一个from后面的表名
        :param sql: sql
        :return: 表名

        注意：
            暂不支持句式如下的sql语句
                SELECT *
                FROM (SELECT A.*,
                      NVL((SELECT B.FULL_NAME
                             FROM CLIENT B
                            WHERE B.CLIENT_ID = A.CLIENT_ID),
                           ' ') AS FULL_NAME
                      FROM MONITORACCT A) A
                WHERE 1 = 1
                    AND TRIM(A.FUND_ACCOUNT) IS NOT NULL
                    AND A.VALID_FLAG = '1'
                    AND A.IS_LIST_ACCT = '1'
                    AND A.BEGIN_DATE < SYSDATE
                    AND END_DATE > SYSDATE
                    AND A.EXCHANGE_TYPE IN ('1', '2', 'D', 'H');

        """
        _sql_split_list = str.upper(sql).split()
        _table_name_index = _sql_split_list.index("FROM") + 1
        table_name = _sql_split_list[_table_name_index]
        return table_name.split(".")[-1].replace(";", "")  # hs_user.sysarg;  SYSARG

    @abstractmethod
    def select(self,
               sql: str,
               data_type=DataType.DictCursor) -> Union[Iterable[OrderedDict], List[list], None]:
        """
        说明：
            支持查询并返回指定数据类型的数据

        :param sql: sql
        :param data_type: 指定数据类型

        :return: 返回指定数据类型的数据
        """
        # TODO: 需要支持多种数据返回类型
        if "SELECT" in str.upper(sql):  # select查询
            cursor = self.connect.cursor()
            cursor.execute(sql)
            result_columns_gen = [str.upper(column[0]) for column in cursor.description]  # 返回查询结果的列名
            result_rows_list = cursor.fetchall()  # 返回查询数据
            # 处理不同种数据类型
            if data_type == DataType.DictCursor:
                result = (OrderedDict(zip(result_columns_gen, rows)) for rows in result_rows_list)
            elif data_type == DataType.SSCursor:
                result = result_rows_list
            else:
                result = []
            return result
        else:
            return None

    @abstractmethod
    def to_excel(self,
                 dataframes: Iterable[DataFrame],
                 excel_name: str,
                 sheet_names=None,
                 index=False) -> None:
        """
        说明：
            支持将查询数据写入文件
            将dataframes存入Excel中

        :param dataframes: 由dataframe组成的可迭代对象
        :param excel_name: Excel文件路径名
        :param sheet_names: sheet页名
        :param index: 是否写入行号

        :return: Excel文件
        """
        with ExcelWriter(excel_name) as writer:
            for i, df in enumerate(dataframes):
                if sheet_names:
                    df.to_excel(writer, sheet_name=sheet_names[i], index=index)
                else:
                    df.to_excel(writer, sheet_name="sheet"+str(i), index=index)

    @abstractmethod
    def expectation(self,
                    sql: Union[str, Iterable[str]],
                    data_type=DataType.DictCursor,
                    excel_path=None) -> None:
        """
        说明：
            通过传入sql语句将数据落地为Excel文件，数据库中的一个表存到Excel为一个sheet页
        示例：
            ==========================================
            (1):一次查询一个表并落地到Excel中t
            DB().expectation(sql="select * from hs_user.excharg;")

            (2):一次查询多个表并落地到Excel中
            DB().expectation(
                sql=[
                    "select * from hs_user.excharg;",
                    "select * from hs_user.sysarg;"
                    "select * from hs_user.exchargtime;"
                ]
            )
            ==========================================
        """
        df_list = []
        table_name_list = []
        if isinstance(sql, str):
            _sql = sql
            table_name = self._table_name(sql=_sql)
            result = self.select(sql=_sql, data_type=data_type)
            df = self._data_convert_dataframe(data=result, data_type=data_type)
            df_list.append(df)
            table_name_list.append(table_name)
        elif isinstance(sql, Iterable):
            for _sql in sql:
                table_name = self._table_name(sql=_sql)
                result = self.select(sql=_sql, data_type=data_type)
                df = self._data_convert_dataframe(data=result, data_type=data_type)
                df_list.append(df)
                table_name_list.append(table_name)
        self.to_excel(dataframes=df_list,
                      excel_name=excel_path,
                      sheet_names=table_name_list)


class OracleDB(AbstracDBClass):
    """
    Oracle数据库实例
    """
    def __init__(self):
        self._read_config()
        self._connect()

    def _read_config(self):
        self.dsn = Config.DSN
        self.username = Config.userName
        self.password = Config.passWord

    def _connect(self):
        self.connect = pyodbc.connect("DSN=%s;UID=%s;PWD=%s;" % (self.dsn, self.username, self.password))

    def _data_convert_dataframe(self,
                                data: Iterable[OrderedDict],
                                data_type=DataType.DictCursor) -> DataFrame:
        """
        支持将查询数据转换为pandas.DataFrame类型
        """
        return super()._data_convert_dataframe(data=data, data_type=data_type)

    def _columns(self,
                 table=None,
                 schema=None,
                 column=None) -> Generator:
        """
        说明：
            返回表字段相关信息
        :param table: 表名
        :param schema: 用户名
        :param column: 字段名
        :return: 表字段相关信息
          0) table_cat
          1) table_schem
          2) table_name
          3) column_name
          4) data_type
          5) type_name
          6) column_size
          7) buffer_length
          8) decimal_digits
          9) num_prec_radix
         10) nullable
         11) remarks
         12) column_def
         13) sql_data_type
         14) sql_datetime_sub
         15) char_octet_length
         16) ordinal_position
         17) is_nullable
        """
        if table: table = str.upper(table)
        if schema: schema = str.upper(schema)
        if column: column = str.upper(column)
        cursor = self.connect.cursor()
        _columns_l = cursor.columns(table=table, schema=schema, column=column).fetchall()
        return ((row[3], row[5]) for row in _columns_l)

    def _table_name(self,
                    sql: str) -> str:
        """
        说明：
            返回当前sql的表名，如果出现连表查询涉及多个表，则默认返回第一个from后面的表名
        """
        return super()._table_name(sql=sql)

    def select(self,
               sql: str,
               data_type=DataType.DictCursor) -> Union[Iterable[OrderedDict], List[list], None]:
        """
        支持查询并返回指定数据类型的数据
        """
        return super().select(sql=sql,
                              data_type=data_type)

    def to_excel(self,
                 dataframes: Iterable[DataFrame],
                 excel_name: str,
                 sheet_names=None,
                 index=False) -> None:
        """
        支持将查询数据写入文件
        """
        return super().to_excel(dataframes=dataframes,
                                excel_name=excel_name,
                                sheet_names=sheet_names,
                                index=index)

    def expectation(self,
                    sql: Union[str, Iterable[str]],
                    data_type=DataType.DictCursor,
                    excel_path=None) -> None:
        """
        支持客户使用该方法将期望查询sql落地成Excel文件
        """
        return super().expectation(sql=sql,
                                   data_type=data_type,
                                   excel_path=excel_path)


class MySQLDB(AbstracDBClass):
    """
    MySQL数据库实例
    """
    def __init__(self):
        self._read_config()
        self._connect()

    def _read_config(self):
        self.host = Config.host
        self.user = Config.user
        self.passwd = Config.passwd
        self.port = Config.port
        self.charset = Config.charset

    def _connect(self):
        self.connect = pymysql.connect(host=self.host,
                                       user=self.user,
                                       password=self.passwd,
                                       port=self.port,
                                       charset=self.charset)

    def _table_name(self,
                    sql: str) -> str:
        """
        说明：
            返回当前sql的表名，如果出现连表查询涉及多个表，则默认返回第一个from后面的表名
        """
        return super()._table_name(sql=sql)

    def select(self,
               sql: str,
               data_type=DataType.DictCursor) -> Union[Iterable[OrderedDict], List[list], None]:
        return super().select(sql=sql, data_type=data_type)

    def _data_convert_dataframe(self,
                                data: Iterable[OrderedDict],
                                data_type=DataType.DictCursor) -> DataFrame:
        """
        支持将查询数据转换为pandas.DataFrame类型
        """
        return super()._data_convert_dataframe(data=data,
                                               data_type=data_type)

    def to_excel(self,
                 dataframes: Iterable[DataFrame],
                 excel_name: str,
                 sheet_names=None,
                 index=False) -> None:
        """
        支持将查询数据写入文件
        """
        return super().to_excel(dataframes=dataframes,
                                excel_name=excel_name,
                                sheet_names=sheet_names,
                                index=index)

    def expectation(self,
                    sql: Union[str, Iterable[str]],
                    data_type=DataType.DictCursor,
                    excel_path=None) -> None:
        """
        支持客户使用该方法将期望查询sql落地成Excel文件
        """
        return super().expectation(sql=sql,
                                   data_type=data_type,
                                   excel_path=excel_path)


class DB(object):
    def __init__(self, dbtype=""):
        self.db = self._read_config(dbtype=dbtype)

    def _read_config(self, dbtype: str):
        """
        先读取config目录下的配置文件，决定实例化哪种数据库类型，例如 Oracle or MySQL。
        :param args:
        :param kwargs:
            1) dbtype: 数据库类型，当指定类型时优先根据指定类型实例化，否则读取config.ini配置
                       如果config.ini未配置默认为MySQL
        """
        supported_dbtypes = {"ORACLE", "MYSQL"}
        _dbtype = str.upper(dbtype)
        _dbtype_config = str.upper(Config.dbtype)

        if _dbtype in supported_dbtypes:
            if _dbtype == "ORACLE":
                return OracleDB()
            elif _dbtype == "MYSQL":
                return MySQLDB()
        elif _dbtype and (_dbtype not in supported_dbtypes):  # 指定dbtype但不在支持数据库范围内
                raise SeleniumTypeError("指定数据库不在当前支持范围内，当前支持如下数据库%s" % supported_dbtypes)
        elif _dbtype_config in supported_dbtypes:
            if _dbtype_config == "ORACLE":
                return OracleDB()
            elif _dbtype_config == "MYSQL":
                return MySQLDB()
        else:  # 未指定dbtype且配置文件不在支持数据库范围内
            raise SeleniumTypeError("未指定数据库或指定数据库不在当前支持范围内，当前支持如下数据库%s" % supported_dbtypes)

    # def __new__(cls, *args, **kwargs):
    #     """
    #     先读取config目录下的配置文件，决定实例化哪种数据库类型，例如 Oracle or MySQL。
    #     :param args:
    #     :param kwargs:
    #         1) dbtype: 数据库类型，当指定类型时优先根据指定类型实例化，否则读取config.ini配置
    #                    如果config.ini未配置默认为MySQL
    #     """
    #     supported_dbtypes = {"ORACLE", "MYSQL"}
    #     _dbtype = str.upper(kwargs.get('dbtype', ""))
    #     _dbtype_config = str.upper(Config.dbtype)
    #
    #     if _dbtype in supported_dbtypes:
    #         if _dbtype == "ORACLE":
    #             return OracleDB()
    #         elif _dbtype == "MYSQL":
    #             return MySQLDB()
    #     elif _dbtype and (_dbtype not in supported_dbtypes):  # 指定dbtype但不在支持数据库范围内
    #             raise SeleniumTypeError("指定数据库不在当前支持范围内，当前支持如下数据库%s" % supported_dbtypes)
    #     elif _dbtype_config in supported_dbtypes:
    #         if _dbtype_config == "ORACLE":
    #             return OracleDB()
    #         elif _dbtype_config == "MYSQL":
    #             return MySQLDB()
    #     else:  # 未指定dbtype且配置文件不在支持数据库范围内
    #         raise SeleniumTypeError("未指定数据库或指定数据库不在当前支持范围内，当前支持如下数据库%s" % supported_dbtypes)

    def expectation(self,
                    sql: Union[str, Iterable[str]],
                    data_type=DataType.DictCursor,
                    excel_path=None):
        """
        说明：
            通过传入sql语句将数据落地为Excel文件，数据库中的一个表存到Excel为一个sheet页
        """
        if excel_path is None:
            excel_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "【Test】_【实际结果】.xlsx")
        self.db.expectation(sql=sql,
                            data_type=data_type,
                            excel_path=excel_path)


def test_dbcheck(sql: Union[str, Iterable[str]]):
    def decorator(func):
        co_varnames = tuple(inspect.signature(func).parameters)  # 获取func函数的形参
        def warpper(*arg, **kwargs):
            func(*arg, **kwargs)
            _check_result = False
            try:
                IS_TEST_FUNC = ("test" in str(arg[0].__class__)) and (co_varnames[0] == "self")
            except IndexError:
                raise SeleniumTypeError("装饰器@test_dbcheck请使用在测试案例方法上 'def test_*(self, ): '。")
            if IS_TEST_FUNC:  # 表示第一个参数是对象测试用例方法“test_*”
                self = arg[0]
                _check_result = dbcheck(self=self, sql=sql)
            else:
                raise SeleniumTypeError("装饰器@test_dbcheck请使用在测试案例方法上 'def test_*(self, ): '。")
            if not _check_result:
                self.assertEqual("", sql, msg="数据比对失败，请查看比对结果文件")
        return warpper
    return decorator


def dbcheck(self, sql: Union[str, Iterable[str]]) -> bool:
    """
    说明：
        执行数据比对

    :param sql: 需要比对的sql语句

    :return: True or False <class 'bool'>
    """
    except_path, actual_path = _get_compare_filename(self=self)
    except_exist = os.path.exists(except_path)
    if not except_exist:
        DB().expectation(sql=sql,
                         excel_path=actual_path,)
        return False
    else:  # 存在期望结果则开始比较
        DB().expectation(sql=sql,
                         excel_path=actual_path,)
        return Compare(expected=except_path, actual=actual_path).compare()


def _get_compare_filename(self):
    _module = self.__module__
    _module = _module.replace(".", "\\")
    case_filename = os.path.realpath(_module + ".py")
    _dir = os.path.dirname(case_filename)  # case案例所在目录
    _name = ( "["
            + self.__module__
            + "."
            + self.__class__.__name__
            + "."
            + self._testMethodName
            + "]")
    except_path = os.path.join(_dir, _name) + "_[期望结果].xlsx"
    actual_path = os.path.join(_dir, _name) + "_[执行结果].xlsx"
    return except_path, actual_path


if __name__ == "__main__":
    df = DB().expectation(
        sql=[
            "select * from hs_user.excharg;",
            "select * from hs_user.exchangetime;",
            "select * from hs_user.sysarg;"
        ]
    )
    # DB().expectation(sql="select * from hs_user.exchangetime;")
