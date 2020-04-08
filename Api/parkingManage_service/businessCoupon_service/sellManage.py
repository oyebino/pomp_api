#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 16:14
# @Author  : 叶永彬
# @File    : sellManage.py

from common.Req import Req
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class SellManage(Req):
    """售卖管理"""
    def couponRefund(self, parkName, refundCouponName):
        """优惠劵退款"""
        couponInfoDict = self.getDictBykey(self.getSellListByPage(parkName),'tmpName',refundCouponName)
        self.url = "/mgr/coupon/sell/refund.do"
        data = {
            "id": couponInfoDict['id'],
            "sellMoney": couponInfoDict['sellMoney'],
            "payMoney": couponInfoDict['sellMoney'],
            "actPayMoney": couponInfoDict['sellMoney'],
            "refundMoney": 1,
            "refundRemark": ""
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re.json()

    def __getParkingBaseDataTree(self):
        """获取当前用户车场"""
        self.url = "/mgr/parkingBaseData/getParkingBaseDataTree.do"
        re = self.get(self.api, headers = json_headers)
        return re

    def getSellListByPage(self,parkName):
        """获取售卖记录"""
        parkNameDict = self.getDictBykey(self.__getParkingBaseDataTree().json(),'name',parkName)
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkNameDict['value'],
            "parkSysType":parkNameDict['parkSysType']
        }
        self.url = "/mgr/coupon/sell/getSellListByPage.do?" + urlencode(data)
        re = self.get(self.api, headers = json_headers)
        return re.json()
