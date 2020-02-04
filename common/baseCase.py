#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 11:50
# @Author  : 叶永彬
# @File    : baseCase.py

from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))

class BaseCase(object):
    """案例的基础测试类"""

    def save_data(self,name,value):
        """
        保存案例的运行时的数值
        :return:
        """
        filePath = tempDataPath.temporaryDataPath
        floderPath = (filePath.rsplit("/",1))[0]
        FloderUtil().createFloder(floderPath)
        XmlHander(filePath).addTag(name,value)


if __name__ == "__main__":
    print(BaseCase().save_data("age","12"))