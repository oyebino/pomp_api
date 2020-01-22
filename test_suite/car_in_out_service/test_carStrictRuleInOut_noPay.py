#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 11:15
# @Author  : 叶永彬
# @File    : test_carStrictRuleInOut_noPay.py

import pytest
import allure
from common.utils import YmlUtils
from common.baseCase import BaseCase
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/car_in_out_service/carStrictRuleInOutNoPay.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarStrictRuleInOutNoPay(BaseCase):
    """临时车严进，不需缴费严出"""
    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],0,send_data['inClientID'])
        result = re.json()
        self.save_data('carIn_jobId',result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCheckCarIn(self,send_data,expect):
        re = cloudparking_service().check_car_in(send_data['carNum'],self.get_caseData('carStrictRuleInOutNoPay','carIn_jobId'))
        result = re.json()['biz_content']['result']['open_gate']
        Assertions().assert_in_text(result, expect["isOpenGate"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        self.save_data('carOut_jobId', result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_mockCheckCarOut(self,send_data,expect):
        re = cloudparking_service().check_car_out(send_data['carNum'],self.get_caseData('carStrictRuleInOutNoPay','carOut_jobId'))
        result = re.json()['biz_content']['result']['open_gate']
        Assertions().assert_in_text(result, expect["isOpenGate"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])