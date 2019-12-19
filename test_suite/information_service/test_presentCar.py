#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 9:19
# @Author  : 叶永彬
# @File    : test_presentCar.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/information_service/presentCar.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询模块")
class TestPresentCar():
    """查看在场车辆"""

    def test_presentCar(self,userLogin,send_data,expect):
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message"])