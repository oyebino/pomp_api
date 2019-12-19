#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 10:15
# @Author  : 叶永彬
# @File    : test_parkingBillDetail.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/information_service/parkingBillDetail.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询模块")
class TestParkingBillDetail():
    """查看车辆收费明细"""

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        re = Information_controller(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message"])