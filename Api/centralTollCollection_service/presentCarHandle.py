#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 16:30
# @Author  : 叶永彬
# @File    : presentCarHandle.py

from common.Req import Req
from urllib.parse import urlencode
import datetime
form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class PresentCarHandle(Req):
    """中央收费处-在场车辆处理"""
    carTypeDict = {
        "蓝牌车": 1,
        "黄牌车": 2,
        "新能源小车": 4,
        "新能源大车": 3
    }

    def centerRecords(self, carCode = ""):
        """查询在场车辆"""
        data = {
            "pageNumber": 1,
            "pageSize": 40,
            "car_code": carCode
        }
        self.url = "/ydtp-backend-service/api/center_records?" + urlencode(data)
        re = self.get(self.zby_api)
        return re.json()['rows']

    def additionalRecording(self, parkName, carCode, enterTime, carSizeType = '蓝牌车'):
        """车辆补录"""
        parkList = {"parkList": self.__sentryUserParking().json()}
        operatorName = parkList['parkList'][0]['channels'][0]['wechat_nick_name']
        parkDict = self.getDictBykey(parkList, 'park_name', parkName)
        carSizeList = {"carSizeList": self.__getCarSize(parkDict['park_id']).json()}
        carSizeDict = self.getDictBykey(carSizeList, 'name', carSizeType)
        matchCarDict = self.__getMatchCarIn(carCode, parkDict['park_id']).json()
        enterTime = datetime.datetime.strftime(enterTime,'%Y-%m-%d %H:%M:%S')
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
            return re.json()
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

    def checkChargeDetail(self, carNum):
        """选择车牌查询费用"""
        carDict = self.getDictBykey(self.centerRecords(carNum), 'carCode' , carNum)
        data = {
            "id": carDict['id'],
            "carType": carDict['carType'],
            "topBillCode": carDict['topBillCode'],
            "carNo": carNum,
            "parkId": carDict['parkId']
        }
        self.url = "/ydtp-backend-service/api/central/charge_detail?" + urlencode(data)
        re = self.get(self.zby_api, headers = form_headers)
        return re.json()

    def centraPay(self, carNum):
        """中央-收费"""
        carDict = self.getDictBykey(self.centerRecords(carNum), 'carCode', carNum)
        carDetailDict = self.checkChargeDetail(carNum)

        data = {
            'billCode': carDetailDict['billCode'],
            'carNo': carNum,
            'carType': carDict['carType'],
            'extend6': carDict['extend6'],
            'id': carDict['id'],
            'realValue': carDetailDict['payVal'],
            'reliefValue': carDetailDict['favorVal'],
            'shouldValue': carDetailDict['parkFee'],
            'time': carDetailDict['checkTime'],
            'topBillCode': carDetailDict["billCode"],
            'traderCouponList': carDetailDict['selectedCoupon']
        }
        self.url = "/ydtp-backend-service/api/central/pay"
        re = self.post(self.zby_api, json = data, headers = json_headers)
        return re.json()

    def centralChargeRecord(self, carNum = ""):
        """中央 收费明细"""
        data = {
            "pageNumber": 1,
            "pageSize": 1,
            "car_no": carNum
        }
        self.url = "/ydtp-backend-service/api/central/charge_records?" + urlencode(data)
        re = self.get(self.zby_api, headers = form_headers)
        return re.json()['list']

    def centralTicket(self, carNum):
        """中央 开纸质票"""
        carRecordDict = self.getDictBykey(self.centralChargeRecord(carNum), 'carNo', carNum)
        self.url = "/ydtp-backend-service/api/central/ticket"
        data = {
            "recordId": carRecordDict['recordId']
        }
        re = self.post(self.zby_api, data =data, headers = form_headers)
        return re.text

    def centralRecordsPath(self, carNum, pathCarNum = None, carType = None):
        """中央 在场校正车牌或车类型"""
        if pathCarNum == None:
            pathCarNum = carNum
        if not carType == None:
            carType = self.carTypeDict[carType]
        carDict = self.getDictBykey(self.centerRecords(carNum), 'carCode', carNum)
        data = {
            "car_code": pathCarNum,
            "topBillCode": carDict['topBillCode'],
            "modifyType": 12,
            "carType": carType
        }
        self.url = "/ydtp-backend-service/api/records/patch"
        re = self.post(self.zby_api, data = data, headers = form_headers)
        return re.text




    