#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 11:15
# @Author  : 叶永彬
# @File    : test_carLightRuleInOut_noPay.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/carLightRuleInOutNoPay.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarLightRuleInOutNoPay(BaseCase):
    """临时车宽进，不需缴费宽出"""
    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],0,send_data['inClientID'])
        result = re.json()
        self.save_data('job_id',result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
