#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 11:50
# @Author  : 叶永彬
# @File    : BaseCase.py

from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath

class BaseCase(object):
    """案例的基础测试类"""

    def save_data(self,name,value):
        """
        保存案例的运行时的数值
        :return:
        """
        floderPath = tempDataPath.temporaryDataPath
        FloderUtil().createFloder(floderPath)
        filePath = floderPath + "/" + tempDataPath.runingCaseName + ".xml"
        XmlHander(filePath).addTag(name,value)



if __name__ == "__main__":
    a = []
    if len(a)>0:
        print(len(a))
