#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 17:00
# @Author  : 叶永彬
# @File    : parkingSetting.py

from common.Req import Req
from Api.index_service.index import Index
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class ParkingSetting(Req):
    """车场配置"""


    def updataOperatorParkCofigInfo(self):
        pass

    def getOperatorParkConfigInfo(self,parkingName):
        """获取车场配置信息"""
        data = {
            # "parkID":parkid
        }

    def getOperatorParkConfigListView(self):
        """获取当前用户车场列表"""
        re = Index(self.Session).getNewMeun()
        operatorID = re.json()["user"]["operatorID"]
        json_data = {
            "pageNumber":1,
            "pageSize":6,
            "sortType":"ASC"
        }
        data = {
            "operatorId": operatorID,
            "parkName":""
        }
        self.url = '/mgr/operatorPark/getOperatorParkConfigListView?' + urlencode(data)
        re = self.post(self.api,json = json_data, headers = json_headers)
        return re

