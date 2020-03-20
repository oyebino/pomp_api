#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 16:30
# @Author  : 叶永彬
# @File    : presentCarHandle.py

from common.Req import Req
from urllib.parse import urlencode
form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class PresentCarHandle(Req):
    """中央收费处-在场车辆处理"""
    def centerRecords(self, carCode = ""):
        """查询在场车辆"""
        data = {
            "pageNumber": 1,
            "pageSize": 40,
            "car_code": carCode
        }
        self.url = "/ydtp-backend-service/api/center_records?" + urlencode(data)
        re = self.get(self.zby_api)
        return re

    def additionalRecording(self, parkName, carCode, enterTime, carSizeType = '蓝牌车'):
        """车辆补录"""
        parkList = {"parkList": self.__sentryUserParking().json()}
        operatorName = parkList['parkList'][0]['channels'][0]['wechat_nick_name']
        parkDict = self.getDictBykey(parkList, 'park_name', parkName)
        carSizeList = {"carSizeList": self.__getCarSize(parkDict['park_id']).json()}
        carSizeDict = self.getDictBykey(carSizeList, 'name', carSizeType)
        matchCarDict = self.__getMatchCarIn(carCode, parkDict['park_id']).json()
        if matchCarDict['carNo'] == None:
            self.url = "/car-record-service/carRecord/additionalRecording"
            data = {
                "carCodeType": carSizeDict['id'],
                "carNo": carCode,
                "enterTime": enterTime,
                "operatorName": operatorName,
                "parkId": parkDict['park_id'],
            }
            re = self.post(self.zby_api, json = data, headers = json_headers)
            return re
        else:
            print("已存在改车牌")

    def __sentryUserParking(self):
        """用户上班停车场"""
        self.url = "/ydtp-backend-service/api/sentry_user_parking"
        re = self.get(self.zby_api)
        return re

    def __getCarSize(self, parkId):
        """获取车辆类型"""
        data = {
          "parkId": parkId
        }
        self.url = "/ydtp-backend-service/api/open/get-car-size?" + urlencode(data)
        re = self.get(self.zby_api)
        return re

    def __getMatchCarIn(self, carNum, parkUUID):
        """匹配是否已有在场记录"""
        self.url = "/car-record-service/carRecord/getMatchCarIn"
        data = {
            "carNo": carNum,
            "parkUUID": parkUUID
        }
        re = self.post(self.zby_api, json = data, headers = json_headers)
        return re