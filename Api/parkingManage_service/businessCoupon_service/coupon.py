#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 16:38
# @Author  : 叶永彬
# @File    : coupon.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from urllib.parse import urlencode
from Api.index_service.index import Index

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}
couponTypeDict = {
    "免费劵":0,
    "金额扣减券":1,
    "金额折扣券":2,
    "金额固定值券":3,
    "时间券":4,
    "不同计价券":5
}


class Coupon(Req):
    """优惠配置"""
    today = SA().get_today_data()

    def addCoupon(self,couponName,parkName,traderName,couponType = '免费劵',couponRule = 0,faceValue = 0,chargeGroupName=None,isCover=0):
        """
        创建优惠劵
        :param couponName:
        :param parkName:
        :param traderName:
        :param couponType:优惠劵类型
        :param faceValue: 各个优惠劵的优惠值(‘免费劵’和‘不同计价劵’不用填写)
        :param chargeGroupName: 不同计价劵填写收费组名
        :param couponRule:扣减类型,时间劵才要填写
        :param isCover: 是否叠加(‘金额扣减劵’‘时间劵’才可填写)
        :return:
        """
        # parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(),'name',parkName)
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(),'name',parkName)
        traderDict = self.getDictBykey(self.__getTrader2Sell(parkDict['value']).json(),'name',traderName)
        if str(couponType) == '不同计价券':
            chargeGroupDict = self.getDictBykey(self.__selectChargeGroupList(parkDict['parkId']).json(), 'typeName',chargeGroupName)
            faceValue = chargeGroupDict['chargeTypeSeq']
        if str(couponType) == '金额折扣券':
            faceValue = int(faceValue)/10
        json_data = {
            "name":couponName,
            "parkList[0]":parkDict['value'],
            "inputParks[0]":parkDict['name'],
            "balanceType":"0",
            "validDay":"1440",
            "couponType":couponTypeDict[couponType],    # 优惠劵类型
            "faceValue":faceValue,      # 各个优惠劵的优惠值(‘免费劵’默认0，不同计价劵会自动获取计费组的typeSeq)
            "originalPrice":"11",       #券原价
            "realPrice":"11",       # 折扣价
            "useRuleMin":"0",
            "useRuleMax":"9999",
            "totalNum":"0",
            "isLimitTotal":"1",
            "couponRule":couponRule,
            "useParkingFee":"0",
            "maxCoverNum":"2",
            "expireRefund":"0",
            "financialParkId":parkDict['value'],
            "isCover":isCover,      # 是否叠加
            "useRule":"0~9999",
            "sellFrom":SA().get_today_data()+" 00:00:00",
            "sellTo":SA().cal_get_day(strType = "%Y-%m-%d",days = 365)+" 23:59:59",
            "validFrom":SA().get_today_data()+" 00:00:00",
            "validTo":SA().cal_get_day(strType = "%Y-%m-%d",days = 365)+" 23:59:59",
            "traderIdListStr": traderDict['id']
        }
        self.url = "/mgr/coupon/add.do"
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re

    def __getParkingBaseDataTree(self):
        """获取当前用户停车场权限列表树"""
        self.url = "/mgr/coupon/getParkingBaseDataTree.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def __selectChargeGroupList(self,parkUUid):
        """列取车场计费组"""
        data = {
            "parkIdList": parkUUid
        }
        self.url = "/mgr/coupon/selectChargeGroupList2?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def __getTrader2Sell(self,parkId):
        """获取商家列表"""
        form_data = {
            "parkIds":parkId,
            "sort": True    # 是否排序
        }
        self.url = "/mgr/coupon/getTrader2Sell.do?" + urlencode(form_data)
        re = self.get(self.api, headers=form_headers)
        return re

    def addSell(self,couponName,parkName,traderName,sellNum = 1,sellMoney = None):
        """
        售卖商家劵
        :param traderName: 商家名
        :param parkName: 停车场名
        :param couponName: 优惠劵名
        :param sellNum: 数量(默认1张)
        :param sellMoney:商家折扣价 (不填自动取总数)
        :return:
        """
        couponDict = self.getDictBykey(self.getCouponListByPage(parkName).json(),'name',couponName)
        couponParkDict = self.getDictBykey(self.__getCouponParkList(couponDict['tmpId']).json(), 'name', parkName)
        traderDict = self.getDictBykey(self.__getTraderList(couponParkDict['id']).json(),'name',traderName)
        totalMoney = int(couponDict['originalPrice']) * int(sellNum)
        if sellMoney == None:
            sellMoney = totalMoney
        json_data = {
            "coupon": "0",
            "realPrice": couponDict['originalPrice'],
            "originalPrice":couponDict['originalPrice'],
            "traderName":traderName,
            "traderId": traderDict['id'],
            "totalAvilableToBuy":0,
            "maxBuyNum":0,
            "sellNum":sellNum,
            "totalMoney": totalMoney,
            "sellMoney": sellMoney,
            "couponTmpId":couponDict['tmpId']
        }
        self.url = "/mgr/coupon/sell/add.do"
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re

    def __getCouponParkList(self,couponTmpId):
        """查看当前劵的使用停车场列表"""

        data = {
            "couponTmpId":couponTmpId
        }
        self.url = "/mgr/coupon/couponParkList.do?" + urlencode(data)
        re = self.get(self.api,headers = form_headers)
        return re

    def getCouponListByPage(self,parkName):
        """优惠配置-获取优惠劵列表"""
        parkDict = self.getDictBykey(Index(self.Session).getUnsignedParkList().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkDict['id'],
            "parkSysType":1
        }
        self.url = "/mgr/coupon/getListByPage.do?" + urlencode(data)
        re = self.get(self.api,headers = form_headers)
        return re

    def __getTraderList(self,parkId):
        """
        在优惠配置，销售劵，获取商家信息列表
        :return:
        """
        form_data = {
            "query_parkId":parkId,
            "page":1,
            "rp":10
        }
        self.url = '/mgr/coupon/sell/getTraderListByPage.do?' + urlencode(form_data)
        re = self.get(self.api , headers = json_headers)
        return re


    def getCouponGrantList(self,parkName,carNum):
        """
        优惠劵发放记录
        :param parkName:
        :param carNum: 发放车牌
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(), 'name', parkName)
        self.url = "/mgr/coupon/getCouponGrantList.do?page=1&rp=1&query_parkId="+str(parkDict['value'])+"&parkSysType=1&beginTime="+self.today+"+00:00:00&endTime="+self.today+"+23:59:59&carCode="+carNum
        re = self.get(self.api, headers=json_headers)
        return re

    def getCouponSerialList(self,parkName,carNum):
        """
        优惠劵使用记录
        :param parkName:
        :param carNum: 使用车牌
        :return:
        """
        from time import sleep
        sleep(5)
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(), 'name', parkName)
        self.url = "/mgr/coupon/getCouponSerialList.do?page=1&rp=1&query_parkId="+str(parkDict['value'])+"&beginTime="+self.today+"+00:00:00&endTime="+self.today+"+23:59:59&carCode="+carNum
        re = self.get(self.api, headers=json_headers)
        return re

    def getCityCouponUseRecord(self,parkName,carNum):
        """查看城市劵使用记录"""
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(),"name",parkName)
        data = {
            "page":1,
            "rp":20,
            "query_useTimeFrom": self.today + " 00:00:00",
            "query_useTimeTo": self.today + " 23:59:59",
            "query_carCode":carNum,
            "parkIds": parkDict['value'],
            "parkSysType":1
        }
        self.url = "/mgr/cityCoupon/useRecord/list.do?" + urlencode(data)
        re = self.get(self.api, headers = json_headers)
        return re

class CityCoupon(Req):
    """城市劵"""
    def createCityCoupon(self, parkName, cityCouponName):
        """创建城市劵"""
        parkCodeSql = "select parkCode from tbl_device_parking where name ='"+ parkName +"'"
        parkCode = db().select(parkCodeSql)
        self.url = "/openydt/api/v2/createCityOperationCouponTemplate"
        json_data = {
            "parkCodeList": [
                parkCode
            ],
            "couponTemplate": {
                "wxAppid": "wxbc0f049b70707054",
                "name": cityCouponName,
                "totalNum": 10,
                "couponType": 1,
                "faceValue": 1.00,
                "useRuleFrom": 0,
                "useRuleTo": 1000,
                "couponRule": "",
                "useParkingFee": "",
                "isCover": 1,
                "maxCoverNum": 3,
                "validFrom": SA().get_today_data() +" 00:00:00",
                "validTo": SA().cal_get_day(strType = "%Y-%m-%d",days = 365)+" 23:59:59",
                "validTime": 360,
                "billUseType": 0,
                "remark": "创建城市运营模板劵--金额扣减券_正常"
            }
        }
        re = self.post(self.openYDT_api, json = json_data)
        return re

    def grantCityOperationCoupon(self,couponTemplateCode,carNum):
        """发放城市劵"""
        self.url = "/openydt/api/v2/grantCityOperationCoupon"
        json_data = {
            "couponTemplateCode" : couponTemplateCode,
            "carNo" : carNum
        }
        re = self.post(self.openYDT_api, json = json_data)
        return re


