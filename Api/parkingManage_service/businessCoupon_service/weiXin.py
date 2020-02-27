#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 16:39
# @Author  : 叶永彬
# @File    : weiXin.py

from common.Req import Req

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}
import time
class WeiXin(Req):
    """商家劵"""
    def grantCouponToCar(self,couponName,carNum):
        """下发商家劵"""

        couponDict = self.getDictBykey(self.__findCouponList().json(),'tmpName',couponName)
        self.url = "/mgr-weixin/coupon/grant/grantCouponToCar.do?t=12" + str(int(time.time()))
        data = {
            "sellBillId": couponDict['id'],
            "carCode": carNum,
            "checkExisted": ""
        }
        re = self.post(self.weiXin_api, data = data, headers = form_headers)
        return re

    def checkTraderCouponPay(self):
        """判断是否支持线上购买优惠劵"""
        self.url = "/mgr-weixin/home/checkTraderCouponPay.do?"
        re = self.post(self.weiXin_api, headers = json_headers)
        return re

    def __findCouponList(self):
        """查询发放优惠劵列表"""
        self.url = "/mgr-weixin/coupon/grant/findCoupon.do?t=12" + str(int(time.time()))
        re = self.post(self.weiXin_api, headers = json_headers)
        return re

    def findCouponList(self):
        """查询发放优惠劵列表"""
        self.url = "/mgr-weixin/coupon/grant/findCoupon.do?t=12" + str(int(time.time()))
        re = self.post(self.weiXin_api, headers = json_headers)
        return re

    def getMyCoupons(self):
        """获取我的优惠劵"""
        self.url = '/mgr-weixin/coupon/report/getMyCoupons.do?t=12' + str(int(time.time()))
        data = {
            "page":1,
            "pageSize":20
        }
        re = self.post(self.weiXin_api,json = data, headers = json_headers)
        return re