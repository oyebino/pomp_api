#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 16:38
# @Author  : 叶永彬
# @File    : test_trader.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.businessman import Businessman
from common.Assert import Assertions
from common.BaseCase import BaseCase


args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/trader.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("商户管理")
class TestTrader(BaseCase):
    """新增商户流程"""
    def test_addTrader(self,userLogin,send_data,expect):
        """商户新增"""
        re = Businessman(userLogin).addTrader(send_data["name"],send_data["parkName"],send_data['couponName'])
        result = re.json()
        Assertions().assert_in_text(result,expect["addTraderMessage"])



    def test_editTrader(self,userLogin,send_data,expect):
        """商户编辑"""
        re = Businessman(userLogin).editTrader(send_data['name'],send_data["editName"],send_data["tel"],send_data['parkName'])
        result = re.json()
        self.save_data('editName',send_data["editName"])
        Assertions().assert_in_text(result, expect["editTraderMessage"])

    def test_checkEditTrader(self,userLogin,send_data,expect):
        """查看修改后商户"""
        re = Businessman(userLogin).getTraderListData(send_data["parkName"],send_data["editName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkEditTraderMessage"])

    # def test_deleteTrader(self,userLogin,send_data,expect):
    #     """商户删除"""
    #     re = Businessman(userLogin).deleteTrader(send_data["editName"])
    #     result = re.json()
    #     Assertions().assert_in_text(result, expect["deleteTraderMessage"])