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
        cloudparking_service().mock_car_in_out(carNum,0,xmlUtil().getValueByName("lightRule_inClientID"))
        self.url = "/mgr/park/presentCar/getPresentCar.do?page=1&rp=20&approchTimeFrom="+self.data+"+00:00:00&approchTimeTo="+self.data+"+23:59:59&parkIds="+str(parkId)+"&parkSysType=1"
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getCarLeaveHistory(self,parkId,carNum):
        """
        获取进出场记录
        :param parkId:
        :return:
        """
        cloudparking_service().mock_car_in_out(carNum, 0, xmlUtil().getValueByName("lightRule_inClientID"))
        self.centralPay(carNum)
        cloudparking_service().mock_car_in_out(carNum, 1, xmlUtil().getValueByName("lightRule_outClientID"))
        self.url = "/mgr/park/carLeaveHistory/pageListParkingRecord.do?page=1&rp=5&fromLeaveTime="+self.data+"+00:00:00&toLeaveTime="+self.data+"+23:59:59&parkIds="+str(parkId)+"&parkSysType=1"
        time.sleep(5)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getParkingBillDetail(self,parkId,carNum):
        """
        获取收费记录
        :param parkId:
        :return:
        """
        cloudparking_service().mock_car_in_out(carNum, 0, xmlUtil().getValueByName("lightRule_inClientID"))
        self.centralPay(carNum)
        cloudparking_service().mock_car_in_out(carNum, 1, xmlUtil().getValueByName("lightRule_outClientID"))
        time.sleep(5)
        self.url = "/mgr/park/parkingBillDetail/list.do?page=1&rp=20&query_payTimeFrom="+self.data+"+00:00:00&query_payTimeTo="+self.data+"+23:59:59&parkIds="+str(parkId)+""
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
        parkFee = self.centralGetCharge(carNum).json()["parkFee"]
        topBillCodeSql = "SELECT TOP_BILL_CODE from parking_bill where CAR_CODE = '"+ carNum +"'"
        topBillCode = db().select(topBillCodeSql)
        self.url = "https://zbcloud.k8s.yidianting.com.cn/charge-pay-service/pay/central-pay"
        json_data = {
          "billCode": SA().get_uuid(),
          "carCode": carNum,
          "parkId": xmlUtil().getValueByName("lightRule_parkUUID"),
          "payTime": SA().cal_get_utcTime(),
          "realValue": parkFee,
          "releaseType": 0,
          "reliefValue": 0,
          "shouldValue": parkFee,
          "tollCollectorName": "zuto-zbyun",
          "topBillCode": topBillCode,
          "traderCouponList": None
        }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re

    # def carOutGetCharge(self,carNum,channel_in,channel_out):
    #     topBillCodeSql = "SELECT top_bill_code from realtime_car_in_out where car_no = '"+ carNum +"' ORDER BY id desc LIMIT 1;"
    #     topBillCode = db().select(topBillCodeSql)
    #     self.url = "https://zbcloud.k8s.yidianting.com.cn/charge-pay-service/charge/car-out-get-charge"
    #     json_data = {
    #         "carNo": carNum,
    #         "carSizeType": 1,
    #         "enterChannelId": channel_in,
    #         "enterTime": "{}".format(SA().get_time(strType="%Y-%m-%dT%H:%M:%S.001Z")),
    #         "leaveChannelId": channel_out,
    #         "leaveTime": "{}".format(SA().cal_get_time(strType="%Y-%m-%dT%H:%M:%S.001Z")),
    #         "parkCode": "{}".format(xmlUtil().getValueByName("lightRule_parkCode")),
    #         "parkUUID": "{}".format(xmlUtil().getValueByName("lightRule_parkUUID")),
    #         "topBillCode": topBillCode
    #     }
    #     re = self.post(self.url, json=json_data, headers=self.api_headers)
    #     return re


# import requests
# from urllib.parse import urlencode
# class central():
#     """中央值守"""
#
#     def __init__(self,host):
#         self.url = host + "/ydtp-backend-service/api/open/central_duty"
#         self.headers = {
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
#         }
#         self.S = requests.Session()
#         data = {
#             "user_id": "apitest",
#             "password": "123456"
#         }
#         result = self.S.post(self.url, data, headers=self.headers)
#         self.token = result.json()['token']
#         print(self.token)
#         # self.son_headers = {
#         #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","user":token
#         # }
#
#     def centralGetCharge(self):
#         """中央查费"""
#         self.url = "https://zbcloud.k8s.yidianting.com.cn/ydtp-backend-service/api/central/charge_detail?"
#         args = {
#             "id": "2004751",
#             "carType": "1",
#             "topBillCode": "190803154651605940964746",
#             "carNo": "京Y19746",
#             "parkId": "55a2151e-1bc6-4fd9-8c6d-8f8a912bf0fe"
#         }
#         encode_args = urlencode(args)
#         re = self.S.get(self.url+encode_args,headers={'user':self.token})
#         print(re.json())


if __name__ == '__main__':
    # central("https://zbcloud.k8s.yidianting.com.cn").centralGetCharge()
    pass


