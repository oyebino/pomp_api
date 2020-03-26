#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 10:50
# @Author  : 叶永彬
# @File    : excelUnitl.py

import xlrd
from xlutils.copy import copy

class ExcelUnitl():
    """excel 基础操作"""
    def __init__(self, file):
        self.file = file

    def editCell(self, col, row, editValue):
        """
        修改excel文件cell值
        :param file:
        :param col: 行
        :param row: 列
        :param editValue:
        :return:
        """
        old_excel = xlrd.open_workbook(self.file, formatting_info=True)
        new_excel = copy(old_excel)
        ws = new_excel.get_sheet(0)
        ws.write(col, row, editValue)
        new_excel.save(self.file)

if __name__ == "__main__":
    ExcelUnitl().editCell('E:/POMP_API/upload/批量退费月票.xls', 1, 0, '123')