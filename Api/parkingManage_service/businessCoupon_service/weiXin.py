#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 16:39
# @Author  : 叶永彬
# @File    : weiXin.py

from common.Req import Req
from common.db import Db as db

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class WeiXin(Req):
    """商家劵"""
    def send_Business_coupon(self,coupon_name,carNum):
        """下发商家劵"""
        sql = "SELECT ID FROM park_trader_coupon_sell_bill psb WHERE psb.COUPON_TMP_ID in(SELECT ID FROM park_trader_coupon_template WHERE `NAME`='{}') ORDER BY ID DESC LIMIT 1 ".format(coupon_name)
        sellId = db().select(sql)
        self.url = "/mgr-weixin/coupon/grant/grantCouponToCar.do"
        data = {
            "sellBillId": "{}".format(sellId),
            "carCode": "{}".format(carNum),
            "checkExisted": ""
        }
        re = self.post(self.weiXin_api, data = data, headers = form_headers)
        return re

    def buyTraderCoupon(self):
        """购买优惠劵"""
        pass

    def checkTraderCouponPay(self):
        """判断是否支持线上购买优惠劵"""
        self.url = "/mgr-weixin/home/checkTraderCouponPay.do?"
        re = self.post(self.weiXin_api, headers = json_headers)
        return re

    def findCouponList(self):
        """查询发放优惠劵列表"""
        self.url = "/mgr-weixin/coupon/grant/findCoupon.do?"
        re = self.post(self.weiXin_api, )