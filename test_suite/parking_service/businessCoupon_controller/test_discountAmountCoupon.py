#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 17:41
# @Author  : 叶永彬
# @File    : test_discountAmountCoupon.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.parking_service.businessCoupon_service import werXin,Coupon_controller
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parking_service/businessCoupon_controller/discountCoupon.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("优惠劵管理")
class TestCouponDiscountAmount():
    """折扣劵创建并使用"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon_controller(userLogin).addCoupon(send_data["couponName"],send_data["couponType"],send_data["faceValue"],send_data["isCover"])
        result = re.json()
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon_controller(userLogin).addSell(send_data["traderName"],send_data["couponName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["addSellMessage"])

    def test_sendCoupon(self,send_data,expect):
        """发放优惠劵"""
        re = werXin().send_Business_coupon(send_data["couponName"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information_controller().centralPay(send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费流水"""
        re = Information_controller(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkParkingBillDetailMessage"])

    def test_checkCouponGrantList(self,userLogin,send_data,expect):
        """查看发放流水"""
        re = Coupon_controller(userLogin).getCouponGrantList(send_data["parkId"])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkCouponGrantListMessage"])

    def test_checkSerialList(self,userLogin,send_data,expect):
        """查看使用流水"""
        re = Coupon_controller(userLogin).getCouponSerialList(send_data["parkId"])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkSerialListMessage"])