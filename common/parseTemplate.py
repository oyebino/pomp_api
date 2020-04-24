#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 11:58
# @Author  : 叶永彬
# @File    : parseTemplate.py

import os
from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))

class ParseTemplate():
    """解析模板"""
    def formatExpected(self,template):
        """
        解析期望值传进的值
        :return:
        """
        import re
        rule = r'\${(.*)}'
        # if not isinstance(template, str):
        #     return template
        textList = re.findall(rule, str(template))
        text_dic = {}
        for key in textList:
            caseName = str(key).split('.')[0]
            keyProperty = str(key).split('.')[1]
            value = self.__get_caseData(keyProperty, caseName)
            text_dic[key] = value
        for key in list(text_dic.keys()):
            strKey = "${" + key + "}"
            template = template.replace(strKey, text_dic[key])
        return template

    def __get_caseData(self,nodeName,caseName = None):
        """
        提取运行案例值
        :return:
        """
        if caseName.lower() == "mytest":
            caseName = str(tempDataPath.runingCaseName).lower() + ".xml"
        else:
            caseName = str(caseName).lower() + ".xml"
        fileList = FloderUtil().getListFloder(root_path + "/temporaryDataLog")
        for file in fileList:
            if self.__getLastFloatName(file).lower() == caseName:
                run_data = XmlHander(file).getValueByName(nodeName)
                return run_data
            else:
                pass

    def __getLastFloatName(self,path):
        """获取最后的文件名"""
        path = str(path).replace("\\","/")
        return path.split('/')[-1]