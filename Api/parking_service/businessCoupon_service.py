#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 15:23
# @Author  : 叶永彬
# @File    : businessCoupon_service.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from common.XmlHander import XmlHander as xmlUtil

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class Businessman_controller(Req):
    """商户管理"""

    def addTrader(self,name):
        """
        新增商家
        :return:
        """
        self.url = "/mgr/trader/addTrader.do"
        json_data ={
            "name":name,
            "parkName":xmlUtil().getValueByName("parkName"),
            "parkId": xmlUtil().getValueByName("lightRule_parkUUID"),
            "type":"美食",
            "defaultType":"美食",
            "contact":"auto-zbyun",
            "tel":'135' + SA().create_randomNum(val=8),
            "password":"123456",
            "confirmPassword":"123456",
            "isLimitBuy":0,
            "userCount":2,
            "couponIdListStr":"4392",
            "telIsEdit":"true"
        }
        re = self.post(self.api,data=json_data,headers=form_headers)
        return re

    def enableTrader(self,name):
        """启用商家"""
        traderIdSql = "SELECT TRADER_ID from park_trader_user where name='" + name + "'"
        traderId = db().select(traderIdSql)

        self.url = "/mgr/trader/enableTraderList.do?traderIds=" + str(traderId)
        re = self.get(self.api,headers=json_headers)
        return re

    def deleteTrader(self,name):
        """删除商户"""
        traderIdSql = "SELECT TRADER_ID from park_trader_user where name='"+ name +"'"
        traderId = db().select(traderIdSql)
        self.url = "/mgr/trader/deleteTrader.do"
        json_data = {
            "id": traderId
        }
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re

class Coupon_controller(Req):
    """优惠配置"""
    today = SA().get_today_data()

    def addCoupon(self,name,couponType=0,faceValue=0,isCover=0):
        """
        创建优惠劵
        :param name:创建优惠名
        :return:
        """
        self.url = "/mgr/coupon/add.do"
        json_data = {
            "name":name,
            "parkList[0]":xmlUtil().getValueByName("lightRule_parkID"),
            "inputParks[0]":xmlUtil().getValueByName("parkName"),
            "balanceType":"0",
            "validDay":"1440",
            "couponType":couponType,    # 优惠劵类型
            "faceValue":faceValue,      # 优惠
            "originalPrice":"11",
            "realPrice":"11",
            "useRuleMin":"0",
            "useRuleMax":"9999",
            "totalNum":"0",
            "isLimitTotal":"1",
            "couponRule":"0",
            "useParkingFee":"0",
            "maxCoverNum":"2",
            "expireRefund":"0",
            "financialParkId":xmlUtil().getValueByName("lightRule_parkID"),
            "isCover":isCover,      # 是否叠加
            "useRule":"0~9999",
            "sellFrom":SA().get_today_data()+" 00:00:00",
            "sellTo":SA().cal_get_day(strType = "%Y-%m-%d",days = 365)+" 23:59:59",
            "validFrom":SA().get_today_data()+" 00:00:00",
            "validTo":SA().cal_get_day(strType = "%Y-%m-%d",days = 365)+" 23:59:59"
        }
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re

    def addSell(self,traderName,couponName):
        """
        售卖商家劵
        :param traderName: 商家名
        :param couponName: 优惠劵名
        :return:
        """
        traderIdSql = "select ID from park_trader where name='"+ traderName +"'"
        traderId = db().select(traderIdSql)
        couponTmpIdSql = "select ID from park_trader_coupon_template where name = '"+couponName+"'"
        couponTmpId = db().select(couponTmpIdSql)
        sellMoneySql = "select real_price from park_trader_coupon_template where NAME='"+ couponName +"'"
        sellMoney = int(db().select(sellMoneySql))
        self.url = "/mgr/coupon/sell/add.do"
        json_data = {
            "coupon": "0",
            "realPrice": sellMoney,
            "originalPrice":sellMoney,
            "traderName":traderName,
            "traderId": traderId,
            "totalAvilableToBuy":0,
            "maxBuyNum":0,
            "sellNum":1,
            "totalMoney":sellMoney,
            "sellMoney":sellMoney,
            "couponTmpId":couponTmpId
        }
        re = self.post(self.api, data=json_data, headers=form_headers)
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



import requests
class werXin(object):
    """商家劵"""
    def __init__(self, host= "https://ydtw.k8s.yidianting.com.cn"):
        self.host = host
        loginUrl = self.host + "/mgr-weixin/passport/signin.do"
        self.S = requests.session()
        data = {
            "username": "13531412589",
            "password": "123456"
        }
        self.S.post(loginUrl, data)

    def send_Business_coupon(self,coupon_name,carNum):
        """下发商家劵"""
        sql = "SELECT ID FROM park_trader_coupon_sell_bill psb WHERE psb.COUPON_TMP_ID in(SELECT ID FROM park_trader_coupon_template WHERE `NAME`='{}') ORDER BY ID DESC LIMIT 1 ".format(coupon_name)
        sellId = db().select(sql)
        path = self.host + "/mgr-weixin/coupon/grant/grantCouponToCar.do"
        data = {
            "sellBillId": "{}".format(sellId),
            "carCode": "{}".format(carNum),
            "checkExisted": ""
        }
        re = self.S.post(path,data)
        return re

