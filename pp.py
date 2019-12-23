#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : pp.py
from Api.parking_service.businessCoupon_service import Coupon_controller
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions

class TestA():
    def test_A(self,userLogin):
       re = Information_controller(userLogin).getCarLeaveHistory("3751","粤Q12345")
       result = re.json()

