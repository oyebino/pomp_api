#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 16:38
# @Author  : 叶永彬
# @File    : couponSetting.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CouponSetting(Req):
    """优惠配置"""
    today = SA().get_today_data()

    def addCoupon(self,name,parkName,traderName,couponType=0,chargeGroupName=None,isCover=0):
        """
        创建优惠劵
        :param name:创建优惠名
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(),'name',parkName)
        traderDict = self.getDictBykey(self.__getTrader2Sell(parkDict['value']).json(),'name',traderName)
        if chargeGroupName == None:
            chargeGroupDict = dict(chargeTypeSeq = 0)
        else:
            chargeGroupDict = self.getDictBykey(self.__selectChargeGroupList(parkDict['parkId']),'typeName',chargeGroupName)
        json_data = {
            "name":name,
            "parkList[0]":parkDict['value'],
            "inputParks[0]":parkDict['name'],
            "balanceType":"0",
            "validDay":"1440",
            "couponType":couponType,    # 优惠劵类型
            "faceValue":chargeGroupDict['chargeTypeSeq'],      # 计费规则类型typeSeq
            "originalPrice":"11",       #券原价
            "realPrice":"11",       # 折扣价
            "useRuleMin":"0",
            "useRuleMax":"9999",
            "totalNum":"0",
            "isLimitTotal":"1",
            "couponRule":"0",
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

    def addSell(self,traderName,parkName,couponName,sellNum,sellMoney):
        """
        售卖商家劵
        :param traderName: 商家名
        :param couponName: 优惠劵名
        :return:
        """
        parkIdSql = "select id from tbl_device_parking where `NAME`='{}'".format(parkName)
        parkId = db().select(parkIdSql)

        couponDict = self.getDictBykey(self.getListByPage(parkId).json(),'name',couponName)
        couponParkDict = self.getDictBykey(self.__getCouponParkList(couponDict['tmpId']).json(), 'name', parkName)
        traderDict = self.getDictBykey(self.__getTraderList(couponParkDict['id']).json(),'name',traderName)

        json_data = {
            "coupon": "0",
            "realPrice": couponDict['originalPrice'],
            "originalPrice":couponDict['originalPrice'],
            "traderName":traderName,
            "traderId": traderDict['id'],
            "totalAvilableToBuy":0,
            "maxBuyNum":0,
            "sellNum":sellNum,
            "totalMoney":"{}".format(couponDict['originalPrice'] * sellNum),
            "sellMoney":sellMoney,
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

    def getListByPage(self,parkId):
        """优惠配置-获取优惠劵列表"""
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkId,
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


    def getCouponGrantList(self,parkId):
        """
        优惠劵发放记录
        :return:
        """
        self.url = "/mgr/coupon/getCouponGrantList.do?page=1&rp=1&query_parkId="+str(parkId)+"&parkSysType=1&beginTime="+self.today+"+00:00:00&endTime="+self.today+"+23:59:59"
        re = self.get(self.api, headers=json_headers)
        return re

    def getCouponSerialList(self,parkId):
        """
        优惠劵使用记录
        :return:
        """
        self.url = "/mgr/coupon/getCouponSerialList.do?page=1&rp=1&query_parkId="+str(parkId)+"&beginTime="+self.today+"+00:00:00&endTime="+self.today+"+23:59:59"
        re = self.get(self.api, headers=json_headers)
        return re
