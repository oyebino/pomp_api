#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 15:59
# @Author  : 叶永彬
# @File    : alarmSetting.py

from common.Req import Req
from Api.index_service.index import Index
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json"}

class AlarmSetting(Req):
    """告警配置"""
    def setAlarm(self, parkName, enterConfidence):
        """配置告警信息"""
        parkDict = self.getDictBykey(self.__getOperatorParkConfigListView().json(), 'parkName', parkName)
        parkAlrmDict = self.__getAlarm(parkDict['parkId']).json()['data']
        data = {
            "addMaintainer": parkAlrmDict['addMaintainer'],
            "deleteMaintainer": parkAlrmDict['deleteMaintainer'],
            "enterConfidence": enterConfidence,
            "offlineDuration": parkAlrmDict['offlineDuration'],
            "offlineRemindTotal": parkAlrmDict['offlineRemindTotal'],
            "oldMaintainer": parkAlrmDict['oldMaintainer'],
            "parkUUId": parkDict['parkId'],
            "reconnectMinsAfter": parkAlrmDict['reconnectMinsAfter'],
            "remindInterval": parkAlrmDict['remindInterval']
        }
        self.url = "/mgr/operatorPark/setAlarm"
        re = self.post(self.api, json=data, headers = json_headers)
        return re.json()

    def __getAlarm(self, parkId):
        """获取告警配置信息"""
        data = {
            "parkId": parkId
        }
        self.url = "/mgr/operatorPark/getAlarm?" + urlencode(data)
        re = self.get(self.api)
        return re

    def __getOperatorParkConfigListView(self):
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
