#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 12:07
# @Author  : 叶永彬
# @File    : test_moreCoverTimeCouponUsed.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.centralTollCollection_service.presentCarHandle import PresentCarHandle
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/moreCoverTimeCouponUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("优惠劵管理")
class TestMoreCoverTimeCouponUsed(BaseCase):
    """多种（5种不一样的）可叠加时间券，售卖，进出场使用，查看收费流水，券发放流水和使用记录"""
    def test_additionalRecording(self,centralTollLogin, send_data, expect):
        """车辆补录"""
        re = PresentCarHandle(centralTollLogin).additionalRecording(send_data['parkName'], send_data['carNum'], send_data['enterTime'])
        result = re.json()['status']
        Assertions().assert_in_text(result, expect["additionalRecordingMsg"])

    def test_sendCouponA(self,weiXinLogin,send_data,expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponNameA"],send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_sendCouponB(self, weiXinLogin, send_data, expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponNameB"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])
    def test_sendCouponC(self, weiXinLogin, send_data, expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponNameC"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])
    def test_sendCouponD(self, weiXinLogin, send_data, expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponNameD"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])
    def test_sendCouponEE(self, weiXinLogin, send_data, expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponNameE"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

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
        result = re.json()
        Assertions().assert_in_text(result['rows'], expect["checkCouponGrantListMessage"])
        Assertions().assert_in_text(result['total'], expect["checkCouponGrantListCount"])

    def test_checkCouponUsedList(self,userLogin,send_data,expect):
        """查看使用流水"""
        re = Coupon(userLogin).getCouponSerialList(send_data["parkName"],send_data["carNum"])
        result = re.json()['rows']
        Assertions().assert_in_text(result, expect["checkSerialListAMessage"])
        Assertions().assert_in_text(result, expect["checkSerialListBMessage"])
        Assertions().assert_in_text(result, expect["checkSerialListCMessage"])
        Assertions().assert_in_text(result, expect["checkSerialListDMessage"])
        Assertions().assert_in_text(result, expect["checkSerialListEMessage"])
