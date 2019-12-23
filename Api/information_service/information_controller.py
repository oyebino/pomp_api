#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 16:00
# @Author  : 叶永彬
# @File    : information_controller.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from common.XmlHander import XmlHander as xmlUtil
from Api.cloudparking_service import cloudparking_service
import time

class Information_controller(Req):
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
        self.url = "/mgr/park/presentCar/getPresentCar.do?page=1&rp=1&approchTimeFrom="+self.data+"+00:00:00&approchTimeTo="+self.data+"+23:59:59&parkIds="+str(parkId)+"&parkSysType=1&plate="+str(carNum)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getCarLeaveHistory(self,parkId,carNum):
        """
        获取进出场记录
        :param parkId:
        :return:
        """
        self.url = "/mgr/park/carLeaveHistory/pageListParkingRecord.do?page=1&rp=1&fromLeaveTime="+self.data+"+00:00:00&toLeaveTime="+self.data+"+23:59:59&query_carNo="+str(carNum)+"&parkIds="+str(parkId)+"&parkSysType=1"
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
        self.url = "/mgr/park/parkingBillDetail/list.do?page=1&rp=1&query_payTimeFrom="+self.data+"+00:00:00&query_payTimeTo="+self.data+"+23:59:59&query_carCode="+str(carNum)+"&parkIds="+str(parkId)+""
        re = self.get(self.api, headers=self.api_headers)
        return re

    def centralGetCharge(self,carNum):
        """
        中央查费
        :return:
        """
        time.sleep(5)
        areaParkingRecordIdSql = "select id from area_parking_record where car_code='"+carNum+"'"
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
        topBillCodeSql = "SELECT TOP_BILL_CODE from parking_bill where CAR_CODE = '"+ carNum +"'"
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

if __name__ == '__main__':
    # central("https://zbcloud.k8s.yidianting.com.cn").centralGetCharge()
    re =Information_controller().centralPay("测K85914")
    print(re.json())


