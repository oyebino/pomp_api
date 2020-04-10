#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 14:27
# @Author  : 叶永彬
# @File    : test_centralAdjustCarType

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.centralTollCollection_service.presentCarHandle import PresentCarHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centralTollCollectionRoom/presentCarHandle/centralAdjustCarType.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央收费处")
@allure.story('中央校正车辆类型')
class TestCentralAdjustCarType(BaseCase):
    """中央校正车辆类型"""
    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_centralAdjustCarType(self, centralTollLogin, send_data, expect):
        """中央-校正在场车牌"""
        re = PresentCarHandle(centralTollLogin).centralRecordsPath(send_data['carNum'], carType = send_data['adjustCarType'])
        result = re
        Assertions().assert_in_text(result, '')

    def test_centralPresentCarType(self, centralTollLogin, send_data, expect):
        """中央查看在场车辆类型"""
        re = PresentCarHandle(centralTollLogin).centerRecords(send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['carType'], expect['presentCarTypeMsg'])

    def test_centryPay(self,centralTollLogin, send_data, expect):
        """中央查费-收费"""
        re = PresentCarHandle(centralTollLogin).centraPay(send_data['carNum'])
        result = re
        Assertions().assert_in_text(result['parkFee'], expect["centryPayMsg"])

    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
