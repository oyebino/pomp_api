# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: 叶永彬
# @Date  : 2018/10/15
# @Desc  :

import os
import re
import yaml
from Config.parameter import tempDataPath
from Config.Config import Config
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))

class YmlUtils(object):

    def __init__(self,yamlPath):
        self.C = Config()
        self.all_data = self.load_yaml(yamlPath)
        tempPath = root_path + yamlPath.replace("test_data", "temporaryDataLog").split('.')[0]
        tempDataPath.temporaryDataPath = tempPath
        # FloderUtil().delFloder(tempPath)

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
        name = [] # 每条案例的名称
        for i in range(0,len(d)):
            for value in d[i].values():
                childarray = []
                childarray.append(value['send_data'])
                childarray.append(value['except'])
                desc.append(value['desc'])
                name.append(value['name'])
                array.append(tuple(childarray))
        tempDataPath.runingCaseName = str(name[0])
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
        self.commonData = root_path + "/test_data/commonData.xml"

    def getsubString2(self,template):
        """
        对yaml文本的引用参数进行解析
        :param template:
        :return:
        """
        template = self.formatYmlFun(template)
        return template

    def getFunData(self,template):
        rule = r'\${__(.*?)}'
        if re.search(rule,template) != None:
            re.search(rule, template).group(0)
        template = re.sub(rule,)
        pass

    def formatYmlFun(self,template):
        """
        对函数进行解析
        :param template:
        :return:
        """
        rule = r'\${__(.*?)}'
        textList = re.findall(rule, str(template))
        text_dic = {}
        for key in textList:
            funName,argsList,kwargsList=self.getFunNameAndParm(key)
            c = getattr(SuperAction(),funName)
            if len(argsList)==0 and len(kwargsList)==0:
                value = c()
            elif not len(argsList)==0 and len(kwargsList)==0:
                argsList = tuple(argsList)
                value = c(*argsList)
            elif len(argsList)==0 and not len(kwargsList)==0:
                kwargsdict = self.listToDict(kwargsList)
                value = c(**kwargsdict)
            else:
                argsList = tuple(argsList)
                kwargsdict = self.listToDict(kwargsList)
                value = c(*argsList,**kwargsdict)

            text_dic[key] = value
        for key in text_dic:
            strKey = "${__" + key + "}"
            template = template.replace(strKey, str(text_dic[key]))
        return self.formatYmlStr(template)

    def listToDict(self,parmList):
        s = ",".join(parmList).replace("'",'"').replace('"','')
        kwargsdict = dict((l.split('=') for l in s.split(',')))
        return kwargsdict

    def __index_str(self,s1,s2):
        """
        返回字符第一次出现的地方
        :return:
        """
        n1 = len(s1)
        n2 = len(s2)
        for i in range(n1 - n2 + 1):
            if s1[i:i + n2] == s2:
                return i
        else:
            return -1

    def getFunNameAndParm(self,yamlFun):
        """切割分开函数名和参数体"""
        num = self.__index_str(yamlFun,'(')
        if num == -1:
            pass
        else:

            funName = yamlFun[0:num]
            parm = yamlFun[num+1:-1]
            kwargsList = list()
            argsList = list()
            if parm == "":
                return funName, argsList, kwargsList
            elif parm==1:
                pass
            else:
                parmList = parm.split(',')
                if len(parmList) ==0:
                    pass
                else:
                    for key in parmList:
                        if key.rfind('=') >= 0:
                            kwargsList.append(key)
                        else:
                            argsList.append(key)
                    return funName,argsList,kwargsList


    def formatYmlStr(self,template):
        """
        对全局变量进行解析
        :param template:
        :return:
        """
        rule = r'\${(.*)}'
        textList = re.findall(rule, template)
        text_dic = {}
        for key in textList:
            value = XmlHander(self.commonData).getValueByName(key)
            text_dic[key] = value
        for key in list(text_dic.keys()):
            if text_dic[key]==None:
                text_dic.pop(key)
            else:
                strKey = "${" + key + "}"
                template = template.replace(strKey, text_dic[key])
            if not text_dic:
                return template
        return template

class FloderUtil(object):

    def getListFloder(self,path):
        """
        文件夹递归,返回全部文件list
        :param path:
        :return:
        """
        os.chdir(path)
        all_files =list()
        isExists = os.path.exists(path)
        if not isExists:
            return False
        else:
            file_list = os.listdir(path)
            for file in file_list:
                filePath = path +'\\'+file
                if os.path.isdir(file):
                    all_files.extend(self.getListFloder(path+'\\'+file))
                    os.chdir(path)
                else:
                    all_files.append(filePath)

        return all_files

    def createFloder(self,path):
        """创建文件夹"""
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def delFloder(self,path):
        """删除文件夹及文件"""
        isExists = os.path.exists(path)
        if not isExists:
            return False
        else:
            if not os.path.isdir(path):
                os.remove(path)
            else:
                import shutil
                shutil.rmtree(path)
            return True



if __name__ == "__main__":
    test_data, case_desc =YmlUtils("/test_data/parkingManage/monthTicket/editTicketConfigStatus.yml").getData
    # print(test_data)
    print(test_data)





