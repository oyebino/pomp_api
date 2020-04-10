#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 9:18
# @Author  : 叶永彬
# @File    : test_centralPayWithCoupon.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.centralTollCollection_service.presentCarHandle import PresentCarHandle
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centralTollCollectionRoom/presentCarHandle/centralPayWithCoupon.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央收费处")
@allure.story('中央收费处选择有商家券的车牌进行缴费')
class TestCentralPayWithCoupon(BaseCase):
    """中央收费处选择有商家券的车牌进行缴费"""
    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_sendCoupon(self,weiXinLogin,send_data,expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_centryPay(self,centralTollLogin, send_data, expect):
        """中央查费-收费"""
        re = PresentCarHandle(centralTollLogin).centraPay(send_data['carNum'])
        result = re
        Assertions().assert_in_text(result['parkFee'], expect["centryPayMsg"])

    def test_checkCentralChargeRecord(self, centralTollLogin, send_data, expect):
        """中央查询-缴费明细"""
        re = PresentCarHandle(centralTollLogin).centralChargeRecord(send_data['carNum'])
        result = re[0]
        Assertions().assert_in_text(result['realValue'], expect["centralChargeRecordMsg"])
        Assertions().assert_in_text(result['reliefValue'], expect["reliefValueMsg"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['realValue'],expect["parkingBillDetailMessage"])

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