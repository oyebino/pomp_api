#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 17:13
# @Author  : 叶永彬
# @File    : test_vemsIntelligenceCleanCarByTime.py

import allure,pytest
from common.utils import YmlUtils
from Api.information_service.information import Information
from Api.offLineParking_service.openYDTReq import OpenYDTReq
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/carNumSearch/vemsIntelligenceCleanCarByTime.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询-车辆查询")
@allure.story('vems智能盘点-按时间方式盘点离')
class TestVemsIntelligenceCleanCarByTime(BaseCase):
    """按时间智能盘点,在在场车辆中查看不到该盘点车辆，在异常进场中可以查看到该车辆"""
    def test_mockCarIn(self,openYDTLogin,send_data,expect):
        """模拟车辆进场"""
        re = OpenYDTReq(openYDTLogin).carInOut(send_data["parkCode"],send_data["carNum"],0)
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_intelligenceCheckCarOut(self, userLogin, send_data, expect):
        """选择一条进行批量盘点"""
        re = Information(userLogin).intelligenceCheckCarOut(send_data['parkName'])
        result = re['status']
        Assertions().assert_text(result, expect["cleanCarCheckOutMsg"])

    def test_checkPresentCar(self, userLogin, send_data, expect):
        """在场车辆中查看不到该盘点车辆"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNum'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkPresentCarMsg"])

    def test_checkAbnormalInCar(self, userLogin, send_data, expect):
        """异常进场中可以查看到该车辆"""
        re = Information(userLogin).getAbnormalInCar(send_data['parkName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["checkAbnormalInCar"])