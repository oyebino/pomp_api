#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 17:27
# @Author  : 叶永彬
# @File    : carType.py

from common.Req import Req
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CarType(Req):
    """车辆分类"""
    def createSpecialType(self, parkName, carSpecialType, typeName):
        """创建特殊类型"""
        self.url = "/mgr/park/specialCarTypeConfig/add.do"
        data = {
            "id":None,
            "parkSysType": 1,
            "vipGroupType": 2,
            "name": typeName,
            "description": "pytest",
            "parkJson":1,
            "renewFormerDays":1,
            "inviteCarTotal":3,
            "parkVipTypeJson":1,
            "showMessage":1
        }
