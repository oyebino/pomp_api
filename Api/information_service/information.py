#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 16:00
# @Author  : 叶永彬
# @File    : information.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from common.XmlHander import XmlHander as xmlUtil
import time
from urllib.parse import urlencode

class Information(Req):
    """
    信息查询
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    data = SA().get_today_data()

    def getPresentCar(self,parkId,carNum):
        """
        获取在场车场
        :param parkId:
        :return:
        """
        data = {
            "page":1,
            "rp":1,
            "approchTimeFrom":self.data +" 00:00:00",
            "approchTimeTo":self.data +" 23:59:59",
            "parkIds":parkId,
            "parkSysType":1,
            "plate":carNum
        }
        self.url = "/mgr/park/presentCar/getPresentCar.do?" + urlencode(data)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getCarLeaveHistory(self,parkId,carNum):
        """
        获取进出场记录
        :param parkId:
        :return:
        """
        data = {
            "page":1,
            "rp":1,
            "fromLeaveTime":self.data + " 00:00:00",
            "toLeaveTime":self.data +" 23:59:59",
            "query_carNo":carNum,
            "parkIds":parkId,
            "parkSysType":1
        }
        self.url = "/mgr/park/carLeaveHistory/pageListParkingRecord.do?" + urlencode(data)
        time.sleep(5)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getParkingBillDetail(self,parkId,carNum):
        """
        获取收费记录
        :param parkId:
        :return:
        """
        time.sleep(5)
        data = {
            "page":1,
            "rp":1,
            "query_payTimeFrom":self.data + " 00:00:00",
            "query_payTimeTo":self.data + " 23:59:59",
            "query_carCode":carNum,
            "parkIds":parkId
        }
        self.url = "/mgr/park/parkingBillDetail/list.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def centralGetCharge(self,carNum):
        """
        中央查费
        :return:
        """
        time.sleep(5)
        areaParkingRecordIdSql = "select id from area_parking_record where car_code='"+carNum+"' ORDER BY enter_time desc limit 1"
        areaParkingRecordId = db().select(areaParkingRecordIdSql)
        self.url = "https://zbcloud.k8s.yidianting.com.cn/charge-pay-service/charge/central-get-charge"
        json_data ={
          "areaParkingRecordId": areaParkingRecordId,
          "carNo": carNum,
          "carType": 1,
          "chargeTime": "{}".format(SA().get_utcTime()),
          "parkingCode": xmlUtil().getValueByName("lightRule_parkCode")
        }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re


    def centralPay(self,carNum):
        """
        中央缴费
        :return:
        """
        payVal = self.centralGetCharge(carNum).json()["payVal"]
        topBillCodeSql = "SELECT TOP_BILL_CODE from parking_bill where CAR_CODE = '"+ carNum +"'ORDER BY check_in_time desc limit 1"
        topBillCode = db().select(topBillCodeSql)
        self.url = "https://zbcloud.k8s.yidianting.com.cn/charge-pay-service/pay/central-pay"
        json_data = {
          "billCode": SA().get_uuid(),
          "carCode": carNum,
          "parkId": xmlUtil().getValueByName("lightRule_parkUUID"),
          "payTime": SA().cal_get_utcTime(),
          "realValue": payVal,
          "releaseType": 0,
          "reliefValue": 0,
          "shouldValue": payVal,
          "tollCollectorName": "zuto-zbyun",
          "topBillCode": topBillCode,
          "traderCouponList": None
        }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re

    def getAdjustCarWaterNum(self,newCarCode,parkIds):
        """
        获取校正流水
        :return:
        """
        data = {
            "page":1,
            "rp":20,
            "newCarCode":newCarCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkIds
        }
        self.url = "/mgr/park/adjustCarRecord/getAdjustCarRecord.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re


    def getAbnormalInCar(self, parkIds, carCode):
        """
        获取异常进场记录
        :return:
        """
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkIds,
            "parkSysType": 1
        }
        self.url = "mgr/park/abnormalInCar/getAbnormalInCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def getAbnormalPicCar(self, parkIds, carCode):
        """
        获取异常拍照记录
        :return:
        """
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkIds,
            "parkSysType": 1
        }
        self.url = "mgr/park/parkAbnormalPicCar/getParkAbnormalPicCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re



if __name__ == '__main__':
    # central("https://zbcloud.k8s.yidianting.com.cn").centralGetCharge()
    # re =Information_controller().centralPay("粤Q12347")
    re = Information().centralGetCharge("粤Q12349")
    print(re.json())


