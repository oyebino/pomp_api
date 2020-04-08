#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 10:50
# @Author  : 叶永彬
# @File    : test_centralAdditionalRecord.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.centralTollCollection_service.presentCarHandle import PresentCarHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centralTollCollectionRoom/presentCarHandle/centralAdditionalRecord.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央收费处")
@allure.story('中央收费处补录车牌')
class TestCentralAdditionalRecord(BaseCase):
    """中央收费处补录车牌"""
    def test_centralAdditionalRecord(self, centralTollLogin, send_data,expect):
        """中央-补录车牌"""
        re = PresentCarHandle(centralTollLogin).additionalRecording(send_data['parkName'], send_data['carNum'],send_data['enterTime'])
        result = re['status']
        Assertions().assert_in_text(result, expect["centralAdditionalRecord"])

    def test_centryPay(self,centralTollLogin, send_data, expect):
        """中央查费-收费"""
        re = PresentCarHandle(centralTollLogin).centraPay(send_data['carNum'])
        result = re.json()['parkFee']
        Assertions().assert_in_text(result, expect["centryPayMsg"])

    def test_checkCentralChargeRecord(self, centralTollLogin, send_data, expect):
        """中央查询-缴费明细"""
        re = PresentCarHandle(centralTollLogin).centralChargeRecord(send_data['carNum'])
        result = re[0]
        Assertions().assert_in_text(result['realValue'], expect["centralChargeRecordMsg"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['realValue'],expect["parkingBillDetailMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])