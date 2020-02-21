#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 10:51
# @Author  : 叶永彬
# @File    : XmlHander.py

import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))
from common.XmlDao import XmlDao

class XmlHander():

    def __init__(self,filename=None):
        if filename is None:
            self.__filename = root_path +'/test_data/commonData.xml'
        else:
            self.__filename = filename
            if os.path.exists(self.__filename):
                pass
            else:
                XmlDao.createXml(self.__filename)

    #获取节点属性
    def getValueByName(self,name,nodeName='caseData'):
        tree = XmlDao.openXml(self.__filename)
        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, nodeName)
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            return nodes[0].attrib['value']
        return None

    #设置节点
    def setValueByName(self,name,value):
        if os.path.exists(self.__filename):
            pass
        else:
            XmlDao.createXml(self.__filename,)
        tree = XmlDao.openXml(self.__filename)
        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, 'caseData')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            nodes[0].attrib['value'] = value
            XmlDao.saveAs(tree, self.__filename)

    #添加节点,已存在相同名称的则会覆盖
    def addTag(self,name,value):
        tree = XmlDao.openXml(self.__filename)
        nodes = XmlDao.find_nodes(tree, 'caseData')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name': name})
        if not nodes is None:
            XmlDao.del_node_by_tagkeyvalue([tree.getroot()], 'caseData', {'name': name})
        XmlDao.add_child_node([tree.getroot()],XmlDao.create_node('caseData', {'name':name,'value':str(value)}))
        XmlDao.saveAs(tree, self.__filename)
    #删除节点
    def deleteTagByName(self,name):
        tree = XmlDao.openXml(self.__filename)
        XmlDao.del_node_by_tagkeyvalue([tree.getroot()], 'caseData', {'name':name})
        XmlDao.saveAs(tree, self.__filename)

if __name__ == "__main__":
    path ='E:\POMP_API/temporaryDataLog/information/carInOutDetail.xml'
    XmlHander(path).getValueByName('age')
    # print(XmlHander('E:/POMP_API/test_data/333.xml').getValueByName("age","caseData"))