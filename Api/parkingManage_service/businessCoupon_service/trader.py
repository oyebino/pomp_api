#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 16:37
# @Author  : 叶永彬
# @File    : trader.py


from common.Req import Req
from common.db import Db as db
from Api.index_service.index import Index
from common.logger import logger
from urllib.parse import urlencode
from common.superAction import SuperAction as SA

form_headers = {"content-type": "application/x-www-form-urlencoded;akeparking_grey_zone_name=grey"}
json_headers = {"content-type": "application/json;charset=UTF-8;akeparking_grey_zone_name=grey"}

class Trader(Req):
    """商户管理"""

    def addTrader(self,name,parkName,account,couponName,pwd = '123456'):
        """
        新增商家
        :return:
        """
        parkNameDict = self.getDictBykey(self.__queryAllPark().json(),'name',parkName)
        couponDict = self.getDictBykey(self.__getCoupon2Buy(parkNameDict['id']).json(),'name',couponName)
        json_data ={
            "name":name,
            "parkName":parkNameDict['name'],
            "parkId": parkNameDict['pkGlobalid'],
            "type":"美食",
            "defaultType":"美食",
            "contact":"auto-zbyun",
            "account": account,
            "tel":"135{}".format(SA().create_randomNum(val= 8)),
            "password":pwd,
            "confirmPassword":pwd,
            "isLimitBuy":0,
            "userCount":2,
            "couponIdListStr":couponDict['id'],
            "telIsEdit":"true"
        }
        if self.__isUniqueName(json_data['name']) and self.__isExistOtherTrader(json_data['account']):
            self.url = "/mgr/trader/addTrader.do"
            re = self.post(self.api,data=json_data,headers=form_headers)
            return re
        else:
            logger.error('商家名或电话已被注册')

    def __queryAllPark(self):
        self.url = "/mgr/trader/queryAllPark.do"
        re = self.get(self.api,headers = json_headers)
        return re


    def __getCoupon2Buy(self,parkId):
        data = {
            "parkId":parkId,
            "sort": True
        }
        self.url = "/mgr/trader/getCoupon2Buy.do?" + urlencode(data)
        re = self.get(self.api, headers=json_headers)
        return re


    def editTrader(self,name,editName,parkName,pwd = ""):
        """编辑商家"""
        traderDict = self.getDictBykey(self.getTraderListData(parkName).json(), 'name', name)
        parkNameDict = self.getDictBykey(self.__queryAllPark().json(), 'name', parkName)

        form_data = {
            "id": traderDict['id'],
            "name": editName,
            "parkName": parkNameDict['name'],
            "parkId": parkNameDict['pkGlobalid'],
            "type": "美食",
            "defaultType": "美食",
            "contact": "auto-zbyun",
            "account": traderDict['account'],
            "tel": traderDict['tel'],
            "password": pwd,
            "confirmPassword": pwd,
            "isLimitBuy": 0,
            "userCount": 2,
            "telIsEdit": "true"
        }
        if self.__isUniqueName(form_data['name'],id=form_data['id']) and self.__isExistOtherTrader(form_data['account'],id=form_data['id']):
            self.url = "/mgr/trader/editTrader.do"
            re = self.post(self.api,data=form_data,headers=form_headers)
            return re
        else:
            logger.error('商家名或电话已被注册')

    def getTraderListData(self,parkName,name=''):
        """获取商户列表"""
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkDict['value'],
            "parkSysType":1,
            "name":name
        }
        self.url = '/mgr/trader/getTraderListData.do?' + urlencode(data)
        re = self.get(self.api,headers=form_headers)
        return re

    def addSell(self,parkName, traderName,couponName,sellNum='1',sellMoney='9'):
        """
        销售商家劵
        :param name: 商家劵名称
        :param sellNum: 购买数量
        :param sellMoney: 商家折扣价
        :return:
        """
        # traderIdSql = "select TRADER_ID from park_trader_user where name='{}'".format(traderName)
        # traderId = db().select(traderIdSql)
        traderDict = self.getDictBykey(self.getTraderListData(parkName).json(), 'name', traderName)

        re = self.__getCoupon2BugByTraderId(traderDict['id'])
        couponIndex,couponDict = self.__findRowData(re.json()['data'],'name',couponName)
        form_data = {
            "coupon":couponIndex,
            "realPrice":couponDict['realPrice'],
            "originalPrice":couponDict['originalPrice'],
            "traderName":couponDict['name'],
            "traderId":traderDict['id'],
            "totalAvilableToBuy":couponDict['totalAvilableToBuy'],
            "maxBuyNum":couponDict['totalAvilableToBuy'],
            "sellNum":sellNum,
            "totalMoney":'{}'.format(int(sellNum) * couponDict['realPrice']),
            "sellMoney":sellMoney,
            "sellRemark":'',
            "couponTmpId":couponDict['couponTmpId']
        }
        self.url = "/mgr/coupon/sell/add.do"
        re = self.post(self.api,data=form_data,headers = form_headers)
        return re


    def __findRowData(self,dataList,findKey,expectedValue):
        """返回json的序号及，当前的子json"""
        for index,row_data in enumerate(dataList):
            if row_data[findKey] == expectedValue:
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

    def __isExistOtherTrader(self,account,id=None):
        """判断是否存在已注册号码"""
        self.url = "/mgr/trader/isExistOtherTrader.do"
        form_data = {
            "account":account,
            "id":id
        }
        re = self.post(self.api,data=form_data,headers=form_headers)
        return re.json()['valid']

    def enableTrader(self,parkName,name):
        """启用商家"""
        # traderIdSql = "SELECT TRADER_ID from park_trader_user where name='" + name + "'"
        # traderId = db().select(traderIdSql)
        traderDict = self.getDictBykey(self.getTraderListData(parkName).json(), 'name', name)
        form_data = {
            "traderIds":traderDict['id']
        }
        self.url = "/mgr/trader/enableTraderList.do?" + urlencode(form_data)
        re = self.get(self.api,headers=json_headers)
        return re

    def disAbleTrader(self,parkName,name):
        """冻结商家"""
        # traderIdSql = "SELECT TRADER_ID from park_trader_user where name='" + name + "'"
        # traderId = db().select(traderIdSql)
        traderDict = self.getDictBykey(self.getTraderListData(parkName).json(), 'name', name)
        form_data = {
            "traderIds": traderDict['id']
        }
        self.url = "/mgr/trader/disableTraderList.do?" + urlencode(form_data)
        re = self.get(self.api, headers=json_headers)
        return re


    def deleteTrader(self,parkName,name):
        """删除商户"""
        traderDict = self.getDictBykey(self.getTraderListData(parkName).json(),'name',name)
        self.url = "/mgr/trader/deleteTrader.do"
        json_data = {
            "id": traderDict['id']
        }
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re
