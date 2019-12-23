#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 16:38
# @Author  : 叶永彬
# @File    : test_trader.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.parking_service.businessCoupon_service import Businessman_controller
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parking_service/businessCoupon_controller/trader.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("商户管理")
class TestTrader():
    """新增商户流程"""
    def test_addTrader(self,userLogin,send_data,expect):
        re = Businessman_controller(userLogin).addTrader(send_data["name"])
        result = re.json()
        Assertions().assert_in_text(result,expect["addTraderMessage"])

    def test_enableTrader(self,userLogin,send_data,expect):
        re = Businessman_controller(userLogin).enableTrader(send_data["name"])
        result = re.json()
        Assertions().assert_in_text(result, expect["enableTraderMessage"])

    def test_deleteTrader(self,userLogin,send_data,expect):
        re = Businessman_controller(userLogin).deleteTrader(send_data["name"])
        result = re.json()
        Assertions().assert_in_text(result, expect["deleteTraderMessage"])