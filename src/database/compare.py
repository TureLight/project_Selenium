# coding:utf-8

"""
作者：azheng
文件名：compare.py
创建日期：2018年12月5日
文档描述：
    编写一个比对Excel文件数据的类。
    比对结果会写入到一个新的Excel文件中，不会修改比对文件数据。
    结果文件.Excel的第一个sheet页将会对比对结果进行描述。
    新文件名为(Compare_Resutlt_*.xlsx)
修改记录：
    2019年1月13日：新增内容：
        1. 支持期望数据多于实际数据条数时，在比对结果文件中能将期望数据中多出的数据以灰色斜体标识出
        2. 支持实际数据多于期望数据条数时，在比对结果文件中能将实际数据中多出的数据以红色颜色标识出
    2019年1月22日：新增内容：
        1. 在结果文件中第一页展示所有表的比对结果
    2019年1月23日：
        1. 修复Excel数据为空时，期望与实际结果一致但被标出为不一致的bug
        2. 支持表相同时，表字段不同时以颜色标识出，实际结果中缺少的字段以灰色斜体标识出，实际结果中多出的字段以红色标识出
    2019年2月24日：
        1. 支持.xls格式数据比对
        2. 支持.csv格式数据比对
"""
# TODO: 支持csv格式文件比对

import os
from collections import OrderedDict
from typing import List, Dict, Iterable
import pandas
from pandas import DataFrame, Series

DIFF_DATA_ATTR = 'background-color: yellow'
EXTRA_DATA_ATTR = 'background-color: red'
LACK_DATA_ATTR = 'background-color: gray; font-style:oblique'


class Compare(object):
    def __init__(self, expected: str, actual: str, sep: str = ","):
        """
        :param expected: 期望结果数据文件
        :param actual: 实际结果数据文件
        """
        self.file_type = None
        self.compare_result_filename = self._init_return_compare_result_filename(path=actual)
        self.expected_dataframes = self._init_dataframes(path=expected, sep=sep)
        self.actual_dataframes = self._init_dataframes(path=actual, sep=sep)
        self.expected_sheet_name = self.expected_dataframes.keys()
        self.actual_sheet_name = self.actual_dataframes.keys()

    def _init_return_compare_result_filename(self, path: str) -> str:
        """
        说明：
            生成比对结果文件的路径，固定为.xlsx格式文件。
        :param path: 实际结果文件路径
        :return: 比对结果文件路径
        """
        _path = os.path.join(os.path.dirname(path),
                             "Compare_Result_" + os.path.basename(path))
        _path_list = _path.split(".")
        _path_list[-1] = "xlsx"
        return ".".join(_path_list)

    def _init_dataframes(self, path: str, sep: str = ",") -> DataFrame:
        """
        说明：
            根据不同文件类型转换为DataFrame对象
        :param path:
        :param sep:
        :return:
        """
        ext = os.path.splitext(path)[-1]
        if str.lower(ext) == '.csv':
            self.file_type = "csv"
            df = pandas.read_csv(filepath_or_buffer=path, sep=sep, engine="python")
            return OrderedDict([('csv', df)])
        elif str.lower(ext) in ['.xlsx', '.xls']:
            self.file_type = "excel"
            return pandas.read_excel(io=path, sheet_name=None)
        else:
            raise TypeError("不支持%s格式文件数据比对" % ext)

    def compare(self) -> bool:
        """
        说明:
            比对Excel差异

        :return: 是否比对成功
        """
        # 1、检查sheet页名称是否一致（即表名） # 目前没有作用
        self.check_sheet_name()
        # 2、比对每个sheet页的数据
        err_loc_od = OrderedDict()
        for sheet_name in (set(self.expected_sheet_name) | set(self.actual_sheet_name)):
            _err_loc_d = self.check_sheet_data(sheet_name=sheet_name)
            err_loc_od[sheet_name] = _err_loc_d
        # 3、写入结果Excel中
        self.writein(err_location=err_loc_od)
        # 4、返回是否比对成功
        _compare_res_list = []
        for key in err_loc_od.keys():
            _compare_res = err_loc_od[key].get('compare_res', False)
            _compare_res_list.append(_compare_res)
        return all(_compare_res_list)


    def _add_style(self, data: DataFrame, err_sheet_loc: Dict):
        """
        说明：
            为比对结果文件中的数据增加样式
        :param data: 比对结果文件中的数据，其实就是实际结果的数据
        :param err_sheet_loc: 比对结果信息
        :return:
        """
        err_sheet_loc.update(loc=[(i, list(data.columns).index(j)) for i, j in err_sheet_loc['loc']])  # 转换loc坐标，列名转换为列号
        lack_column_num = [list(data.columns).index(_col_data.name) for _col_data in err_sheet_loc['lack_column_data']]
        extra_column_num = [list(data.columns).index(_col_name) for _col_name in err_sheet_loc['extra_column_name']]
        deal_count = err_sheet_loc.get('deal_count', 0)
        df_data_style = []
        data_row_count, data_col_count = data.shape
        for row in range(data_row_count):
            _series_data_style = []
            for col in range(data_col_count):
                if col in lack_column_num:
                    _series_data_style.append(LACK_DATA_ATTR)  # 实际比期望缺少的列，灰色标识
                elif col in extra_column_num:
                    _series_data_style.append(EXTRA_DATA_ATTR)  # 实际比期望多出的列，红色标识
                elif (row, col) in err_sheet_loc.get('loc', []):
                    _series_data_style.append(DIFF_DATA_ATTR)  # 比对结果不同以黄色标识
                elif ((data_row_count-1 - row) < deal_count) and (deal_count > 0):  # 实际sheet数据条数>期望条数，红色标识
                    _series_data_style.append(EXTRA_DATA_ATTR)
                elif ((data_row_count-1 - row) < -deal_count) and (deal_count < 0):  # 实际sheet数据条数<期望条数，灰色标识
                    _series_data_style.append(LACK_DATA_ATTR)
                else:
                    _series_data_style.append("")
            df_data_style.append(_series_data_style)
        return pandas.DataFrame(data=df_data_style,
                                index=data.index,
                                columns=data.columns)

    def writein(self, err_location: OrderedDict, index=False):
        """
        说明：
            将比对结果写入文件
        """
        # print(err_location)
        with pandas.ExcelWriter(path=self.compare_result_filename) as writer:
            self.first_sheet_df(err_location=err_location).to_excel(excel_writer=writer,
                                                                    sheet_name='比对结果',
                                                                    index=index)
            for sheet_name, df in self.actual_dataframes.items():
                err_sheet_loc = err_location[sheet_name]  # type: dict
                deal_count = err_sheet_loc.get('deal_count', 0)
                if deal_count < 0:
                    # pandas.concat 新产生的DataFrame列会重新排序
                    df = pandas.concat(objs=[df, err_sheet_loc.get("lack_row_data", DataFrame())], ignore_index=True)  # 如果实际数据缺少，则在结果中拼接上缺少的数据
                lack_column_data = err_sheet_loc.get('lack_column_data', [])  # type: Iterable[Series]
                if lack_column_data:
                    for _col_data in lack_column_data:
                        df = df.assign(**{_col_data.name: _col_data})  # 为df增加列数据，df.assign(列名1=数据1, 列名2=数据2)
                new_df = df.style.apply(func=self._add_style, axis=None, err_sheet_loc=err_sheet_loc)
                new_df.to_excel(excel_writer=writer,
                                sheet_name=sheet_name,
                                index=index)

    def first_sheet_df(self, err_location: OrderedDict) -> DataFrame:
        columns = ('表名', '比对结果')
        data_list = []
        for key in err_location.keys():
            _data_key_list = []
            _sheet_name = err_location[key].get('sheet_name', "无")
            _data_key_list.append(_sheet_name)  # 表名
            _act_exist_flag = err_location[key].get('act_exist_flag', False)
            _exp_exist_flag = err_location[key].get('exp_exist_flag', False)
            _compare_res = err_location[key].get('compare_res', False)
            if not _compare_res:  # 是否比对成功，compare_res=true表示比对成功
                if _act_exist_flag is False:
                    _compare_res = '未比对，实际数据未找到'
                elif _exp_exist_flag is False:
                    _compare_res = '未比对，期望数据未找到'
                else:
                    _compare_res = '失败'
            else:
                _compare_res = '成功'
            _data_key_list.append(_compare_res)
            data_list.append(_data_key_list)
        return pandas.DataFrame(data=data_list, columns=columns)

    def check_sheet_name(self):
        """
        说明
            检查两个Excel中的sheet页名称是否相同
        :return: 比对是否成功 <class 'bool'>
        """
        if self.actual_sheet_name == self.expected_sheet_name:
            # print("check_sheet_name比对成功")
            return True
        else:
            # print("check_sheet_name比对失败")
            return False

    def check_column(self, expected_df: DataFrame, actual_df: DataFrame):
        expected_df_columns = expected_df.keys().sort_values()  # 获取sheet页的列名(按照升序排序)
        actual_df_columns = actual_df.keys().sort_values()
        if (len(expected_df_columns) == len(actual_df_columns)) and all(expected_df_columns == actual_df_columns):
            # print("check_column比对成功")
            return True
        else:
            # print("check_column比对失败")
            return False

    def check_sheet_data(self, sheet_name: str):
        """
        说明：
            比对2个Excel同一个sheet页的数据
        :param sheet_name: 比对的表名
        :return: 当前表(sheet)比对结果
        """
        err_loc_d = dict(
            sheet_name=sheet_name,
            loc=[],
            act_exist_flag=False,  # False表示实际结果中不存在该表
            exp_exist_flag=False,  # False表示期望结果中不存在该表
            compare_res=False,  # true表示比对成功，false表示比对失败
            deal_count=0,       # deal_count>0表示 实际条数>期望条数。需要特殊处理这些数据的样式
            lack_row_data=[],   # deal_count<0时，实际条数<期望条数，需要将实际缺失的数据保存在这里 type: DataFrame
            lack_column_data=[],   # 实际结果中缺失列的数据 type: Iterable[Series]
            extra_column_name=[],  # 实际结果中比期望多出列的列名 type: Iterable[str]
        )
        if sheet_name in self.actual_sheet_name:
            err_loc_d.update(act_exist_flag=True)
        if sheet_name in self.expected_sheet_name:
            err_loc_d.update(exp_exist_flag=True)
        if err_loc_d.get('act_exist_flag') and err_loc_d.get('exp_exist_flag'):  # 实际与期望都存在的表开始进行比对
            expected_df = self.expected_dataframes[sheet_name]
            actual_df = self.actual_dataframes[sheet_name]
            # 1、比对sheet页中，数据列名是否相同，如果列名不同则不比对。
            # self.check_column(expected_df=expected_df, actual_df=actual_df)
            # 2、遍历df每行数据逐个比对
            actual_df_row_count, actual_df_column_count = actual_df.shape
            expected_df_row_count, expected_df_column_count = expected_df.shape
            deal_count = actual_df_row_count - expected_df_row_count  # >0 实际条数>期望条数； <0 实际条数<期望条数
            traversal_count = expected_df_row_count if actual_df_row_count > expected_df_row_count else actual_df_row_count
            act_column_name_list = list(actual_df.keys())
            exp_column_name_list = list(expected_df.keys())
            loc = []  # 记录比对失败的位置
            for i in range(traversal_count):  # 这里只比对实际与期望的最小行数，多出的行数据会在后面特殊处理
                for act_column_name in act_column_name_list:
                    actual_cell_value = actual_df.iloc[i].get(act_column_name)
                    expected_cell_value = expected_df.iloc[i].get(act_column_name)
                    # 2019年1月23日 当Excel单元格数据为空时，取出的值为nan type为float，
                    # 此时两个nan 进行==比较时为False，但id一致，所以增加此判断，修复为空时实际与期望一致但被标出不一致的问题
                    if (actual_cell_value != expected_cell_value) and not (actual_cell_value is expected_cell_value):
                        loc.append((i, act_column_name))
            err_loc_d.update(loc=loc)
            if not loc: err_loc_d.update(compare_res=True)
            err_loc_d.update(deal_count=deal_count)
            # 3、如果实际值比期望值缺少行，则记录在err_loc_d中
            if deal_count < 0:
                err_loc_d.update(lack_row_data=expected_df.iloc[deal_count:])
                err_loc_d.update(compare_res=False)
            if deal_count > 0:
                err_loc_d.update(compare_res=False)
            # 4、如果实际值比期望值缺少列，则记录在err_loc_d中
            lack_column_name = set(exp_column_name_list) - set(act_column_name_list)
            extra_column_name = set(act_column_name_list) - set(exp_column_name_list)
            if lack_column_name:
                err_loc_d.update(compare_res=False)
                lack_column_data = [expected_df[col] for col in lack_column_name]
                err_loc_d.update(lack_column_data=lack_column_data)
            if extra_column_name:
                err_loc_d.update(extra_column_name=list(extra_column_name))
        print("比对失败位置:", err_loc_d)
        return err_loc_d


if __name__ == "__main__":
    # c = Compare(expected=r"C:\Users\zhangzheng17239\Desktop\test1.xlsx",
    #             actual=r"C:\Users\zhangzheng17239\Desktop\test2.xlsx")
    # c = Compare(expected=r"C:\Users\zhangzheng17239\Desktop\test1.xls",
    #             actual=r"C:\Users\zhangzheng17239\Desktop\test2.xls")
    c = Compare(expected=r"D:\test1\债券基本资料表-HTIS.ADB_DJ_ZQ-体内.xlsx",
                actual=r"D:\test2\债券基本资料表-HTIS.ADB_DJ_ZQ-体内.xlsx")  # , sep=r'\t'

    c.compare()
