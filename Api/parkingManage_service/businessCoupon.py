#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 15:23
# @Author  : 叶永彬
# @File    : businessCoupon.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from common.XmlHander import XmlHander as xmlUtil
from common.logger import logger
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class Businessman(Req):
    """商户管理"""

    def addTrader(self,name):
        """
        新增商家
        :return:
        """
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
        if self.__isUniqueName(json_data['name']) and self.__isExistOtherTrader(json_data['tel']):
            self.url = "/mgr/trader/addTrader.do"
            re = self.post(self.api,data=json_data,headers=form_headers)
            return re
        else:
            logger.error('商家名或电话已被注册')

    def editTrader(self,id,name,tel):
        """编辑商家"""
        traderIdSql = "select TRADER_ID from park_trader_user where name='{}'".format(name)
        traderId = db().select(traderIdSql)
        form_data = {
            "id":traderId,
            "name": name,
            "parkName": xmlUtil().getValueByName("parkName"),
            "parkId": xmlUtil().getValueByName("lightRule_parkUUID"),
            "type": "美食",
            "defaultType": "美食",
            "contact": "auto-zbyun",
            "tel": tel,
            "password": "123456",
            "confirmPassword": "123456",
            "isLimitBuy": 0,
            "userCount": 2,
            "couponIdListStr": "4392",
            "telIsEdit": "true"
        }
        if self.__isUniqueName(form_data['name'],id=form_data['id']) and self.__isExistOtherTrader(form_data['tel'],id=form_data['id']):
            self.url = "/mgr/trader/editTrader.do"
            re = self.post(self.api,data=form_data,headers=form_headers)
            return re
        else:
            logger.error('商家名或电话已被注册')

    def getTraderListData(self,parkId,name=''):
        """获取商户列表"""
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkId,
            "parkSysType":1,
            "name":name
        }
        self.url = '/mgr/trader/getTraderListData.do?' + urlencode(data)
        re = self.get(self.api,headers=form_headers)
        return re

    def add(self,traderId):
        """
        销售商家劵
        :return:
        """
        self.url = "/mgr/coupon/sell/add.do"
        re = self.__getCoupon2BugByTraderId(traderId)

        json_data = {
            "coupon":couponIndex,
            "realPrice":1,
            "originalPrice":1,
            "traderName":11,
            "traderId":1,
            "totalAvilableToBuy":1,
            "maxBuyNum":1,
            "sellNum":1,
            "totalMoney":1,
            "sellMoney":1,
            "sellRemark":1,
            "couponTmpId":1
        }

    def __findRowData(self,dataList,findKey,findValue):
        for index,row_data in enumerate(dataList):
            if row_data[findKey] == findValue:
                return index,row_data

    def __getCoupon2BugByTraderId(self,traderId):
        """按商户ID查看所有优惠劵信息"""
        form_data = {
            "traderId":traderId
        }
        self.url = '/mgr/trader/getCoupon2BuyByTraderId.do?' + urlencode(form_data)
        re = self.get(self.api,headers=form_headers)
        return re

    def __isUniqueName(self,name,id=None):
        """判断是否存在已有相同商户名"""
        self.url = "/mgr/trader/isUniqueName.do"
        form_data = {
            "name":name,
            "traderId":id
        }
        re = self.post(self.api,data=form_data,headers=form_headers)
        return re.json()['valid']

    def __isExistOtherTrader(self,tel,id=None):
        """判断是否存在已注册号码"""
        self.url = "/mgr/trader/isExistOtherTrader.do"
        form_data = {
            "tel":tel,
            "id":id
        }
        re = self.post(self.api,data=form_data,headers=form_headers)
        return re.json()['valid']

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

class Coupon(Req):
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
class WeiXin(object):
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

    def buyTraderCoupon(self):
        """购买优惠劵"""
        pass
