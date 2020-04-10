#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 17:58
# @Author  : 叶永彬
# @File    : index.py

from common.Req import Req
from urllib.parse import urlencode
form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class Index(Req):
    """首页接口"""
    def getNewMeun(self):
        self.url = "/mgr/main/newmenu.do"
        re = self.get(self.api, headers = json_headers)
        return re

    def getParkingBaseDataTree(self):
        """获取当前用户停车场权限列表树"""
        self.url = "/mgr/parkingBaseData/getParkingBaseDataTree.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def getUnsignedParkList(self):
        self.url = "/mgr/valueAdded/getUnsignedParkList.do"
        re = self.get(self.api, headers = json_headers)
        return re

    def getOperatorParkConfigListView(self, parkName):
        """查看车场配置列表"""
        operatorId = self.getNewMeun().json()['user']['operatorID']
        data = {
            "operatorId": operatorId,
            "parkName": parkName
        }
        json_data = {
            "pageNumber": 1,
            "pageSize": 6,
            "sortType": "ASC"
        }
        self.url = "/mgr/operatorPark/getOperatorParkConfigListView?" + urlencode(data)
        re = self.post(self.api, json= json_data,headers= json_headers)
        return re.json()['data']['list']

    def downloadExcelTmp(self,fileName,downPath):
        """下载excel模板"""
        data = {
            "fileName": fileName
        }
        self.url = "/mgr/common/templateDownload.do?" + urlencode(data)
        re = self.get(self.api)
        with open(downPath, 'wb') as code:
            code.write(re.content)