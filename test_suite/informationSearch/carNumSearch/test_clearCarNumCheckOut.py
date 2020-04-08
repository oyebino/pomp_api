#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 16:56
# @Author  : 叶永彬
# @File    : test_clearCarNumCheckOut.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/carNumSearch/clearCarNumCheckOut.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询-车辆查询")
@allure.story('批量盘点-在场车辆中查看不到该盘点车辆-异常进场能查看到该车辆')
class TestClearCarNumCheckOut(BaseCase):

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_cleanCarCheckOut(self, userLogin, send_data, expect):
        """选择一条进行批量盘点"""
        re = Information(userLogin).cleanCarCheckOut(send_data['parkName'], send_data['carNum'])
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