#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/20 15:48
# @Author  : 叶永彬
# @File    : openYDTReq.py
from common.superAction import SuperAction as SA
from common.Req import Req
import time
form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json"}

class OpenYDTReq(Req):
    """vems车场业务"""

    def carInOut(self,parkCode, carNum, mockType):
        """开放平台模拟vems车进出"""
        self.url = "/openydt/api/v2/mockInOut"
        data = {
            "carCard": "",
            "carNo": carNum,
            "mockType": mockType,
            "operateTime": "2017-09-11 14:04:04",
            "operator": "operator",
            "parkCode": parkCode
        }
        time.sleep(5)
        re = self.post(self.openYDT_api, json = data, headers = json_headers)
        return re.json()

    def getParkFee(self,parkCode ,carNum):
        """查费"""
        self.url = "/openydt/api/v2/getParkFee"
        data = {
            "carCode": carNum,
            "parkCode": parkCode
        }
        re = self.post(self.openYDT_api, json=data,headers = json_headers)
        return re.json()['data']

    def payParkFee(self ,parkCode, carNum):
        """缴费"""
        parkFeeDict = self.getParkFee(parkCode, carNum)
        # couponList = parkFeeDict.get('otherAttr').get('traderCouponList') if parkFeeDict.get('otherAttr').get('traderCouponList') else []
        data = {
            "parkingCode": parkFeeDict.get("parkingCode"),
            "chargeDate": parkFeeDict.get("chargeDate"),
            "payDate": SA().get_time(),
            "actPayCharge": parkFeeDict.get("shouldPayValue"),
            "reliefCharge": "1.2",
            "payOrigin": "3",
            "payOriginRemark": "微信",
            "paymentMode": "0",
            "paymentModeRemark": "00",
            "billCode": SA.getTimeStamp(),
            "couponList": []
        }
        self.url = "/openydt/api/v2/payParkFee"
        re = self.post(self.openYDT_api, json=data, headers = json_headers)
        return re.json()

    def getVipType(self,parkCode,customVipName):
        """通过开放平台-查询vems月票类型信息"""
        self.url = "/openydt/api/v2/getVipType"
        data = {
            "parkCode": parkCode,
            "customVipName":customVipName,
            "operateTime": SA().get_time(strType='%Y-%m-%d %H:%M:%S')
        }
        re = self.post(self.openYDT_api,json=data, headers = json_headers)
        return re.json()['data']['vipTypeList']

    def getMonthCard(self,parkCode ,carNum):
        """通过开放平台-查询vems月卡信息"""
        self.url = "/openydt/api/v2/getMonthCard"
        data = {
            "parkCode": parkCode,
            "carNO": carNum
        }
        re = self.post(self.openYDT_api, json= data, headers = json_headers)
        return re.json()['data']['monthCardList']