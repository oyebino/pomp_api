#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 15:28
# @Author  : 叶永彬
# @File    : test_reduceAmountCouponCover.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/reduceAmountCouponCover.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("优惠劵管理")
class TestReduceAmountCouponCover():
    """可叠加金额扣减劵创建并使用"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon(userLogin).addCoupon(send_data["couponName"],send_data["parkName"],send_data["traderName"],send_data["couponType"],faceValue=send_data['faceValue'],isCover=send_data['isCover'])
        result = re.json()
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon(userLogin).addSell(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["addSellMessage"])

    def test_sendCoupon(self,weiXinLogin,send_data,expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponName"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNum"],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re.json()
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费流水"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re.json()['rows']
        Assertions().assert_in_text(result, expect["checkParkingBillDetailMessage"])

    def test_checkCouponSendList(self,userLogin,send_data,expect):
        """查看发放流水"""
        re = Coupon(userLogin).getCouponGrantList(send_data["parkName"],send_data["carNum"])
        result = re.json()['rows']
        Assertions().assert_in_text(result, expect["checkCouponGrantListMessage"])

    def test_checkCouponUsedList(self,userLogin,send_data,expect):
        """查看使用流水"""
        re = Coupon(userLogin).getCouponSerialList(send_data["parkName"],send_data["carNum"])
        result = re.json()['rows']
        Assertions().assert_in_text(result, expect["checkSerialListMessage"])