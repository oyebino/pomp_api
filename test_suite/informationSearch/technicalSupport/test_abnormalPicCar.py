#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/24 14:35
# @Author  : 何涌
# @File    : test_abnormalPicCar.py

import pytest,os
import allure
from Api.cloudparking_service import cloudparking_service
from common.utils import YmlUtils
from common.Assert import Assertions
from Api.information_service.information import Information

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/informationSearch/technicalSupport/abnormalPicCar.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云")
class TestabnormalPicCar():

    """临时车严进后，不进场，再来一台临时车严进，有异常拍照上报"""

    def test_mockCarIn(self, send_data, expect):
        """第一辆车模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["StrictRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarIn2(self, send_data, expect):
        """第二辆车模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum2"], 0, send_data["StrictRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarIn2Message"])

    def test_getAbnormalPicCar(self, userLogin, send_data, expect):
        """POMP上查看异常拍照记录"""
        re = Information(userLogin).getAbnormalPicCar(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["getAbnormalPicCarMsg"])
        Assertions().assert_in_text(result["data"]["carCode"], expect["carNum"])

