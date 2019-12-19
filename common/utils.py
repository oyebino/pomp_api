# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: 叶永彬
# @Date  : 2018/10/15
# @Desc  :

import os
import re
import yaml
import json
from Config.Config import Config

class YmlUtils(object):

    def __init__(self,yamlPath):
        self.C = Config()
        self.all_data = self.load_yaml(yamlPath)

    def load_yaml(self,yamlPath):

        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = root_path+yamlPath

        f = open(full_path, 'r', encoding='UTF-8')
        cfg = f.read()
        cfg = YmlCommon().getsubString2(cfg)
        self.all_data = yaml.load(cfg)  # 用load方法转字典
        return self.all_data

    @property
    def format_data(self):
        d = self.all_data
        item = []
        for i in range(0,len(d)):
            for value in d[i].values():
                child = []
                child.append(value['name'])
                child.append(value['send_data'])
                child.append(value['except'])
                item.append(tuple(child))
        return item


    @property
    def getData(self):

        d = self.all_data
        array=[]  # 每条案例对应的测试数据信息
        desc=[]   # 每条案例对应的描述信息
        for i in range(0,len(d)):
            for value in d[i].values():
                childarray = []
                childarray.append(value['send_data'])
                childarray.append(value['except'])
                desc.append(value['desc'])
                array.append(tuple(childarray))
        return array,desc

    def single_data(self):
        pass
    #TODO 先占个位置


    def data_flow(self):
        """业务流数据"""
        pass
from common.superAction import SuperAction
from common.XmlHander import XmlHander
class YmlCommon(object):
    def __init__(self):
        self.C = Config()

    def getsubString2(self,template):
        """
        对yaml文本的引用参数进行解析
        :param template:
        :return:
        """
        template = self.formatYmlFun(template)
        return template

    def formatYmlFun(self,template):
        """
        对函数进行解析
        :param template:
        :return:
        """
        rule = r'%(.*)%'
        textList = re.findall(rule, str(template))
        text_dic = {}
        for key in textList:
            c = getattr(SuperAction(),key)
            value = c()
            text_dic[key] = value
        for key in text_dic:
            strKey = "%" + key + "%"
            template = template.replace(strKey, text_dic[key])
        return self.formatYmlStr(template)

    def formatYmlStr(self,template):
        """
        对全局变量进行解析
        :param template:
        :return:
        """
        rule = r'{(.*)}'
        textList = re.findall(rule, template)
        text_dic = {}
        for key in textList:
            value = XmlHander().getValueByName(key)
            text_dic[key] = value
        for key in text_dic:
            strKey = "{" + key + "}"
            template = template.replace(strKey, text_dic[key])
        return template


if __name__ == "__main__":
    # test_data, case_desc =YmlUtils("/test_data/information_service/presentCar.yml").all_data
    # print(test_data)
    # c = YmlUtils("/test_data/information_service/presentCar.yml").all_data
    # print(c)
    x = XmlHander()
    print(x._XmlHander__filename)


