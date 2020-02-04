#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : test_pp.py
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions
class TestAAA():
    def test_A(self,userLogin):
        re = Information_controller(userLogin).getPresentCar("3751","云M6UJ7F")
        print(re.json())

