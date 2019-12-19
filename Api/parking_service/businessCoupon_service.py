#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 15:23
# @Author  : 叶永彬
# @File    : businessCoupon_service.py

from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from common.XmlHander import XmlHander as xmlUtil

class Businessman(Req):
    """商户管理"""
    api_headers = {"content-type": "application/x-www-form-urlencoded"}
    def addTrader(self):
        """
        新增商家
        :return:
        """
        self.url = "/mgr/trader/addTrader.do"
        json_data ={
            "parkName":xmlUtil().getValueByName("parkName"),
            "parkId": xmlUtil().getValueByName("lightRule_parkUUID"),
            "type":"美食",
            "contact":"auto-zbyun",
            "tel":"1380013812",
            "password":"123456",
            "confirmPassword":"123456",
            "isLimitBuy":0,
            "userCount":2,
            "telIsEdit":"true"
        }
        re = self.post(self.api,data=json_data,headers=self.api_headers)
        return re