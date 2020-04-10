#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/06 11:15
# @Author  : 叶永彬
# @File    : test_carLightRuleOut_noInside.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/freeParking/lightRuleChannel/carLightRuleOutNoInside.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-免费停车场")
@allure.story('临时车无在场宽出')
class TestCarLightRuleOutNoInside(BaseCase):
    """临时车无在场宽出"""
    def test_mockCarOut(self,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])

