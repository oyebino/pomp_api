#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 16:39
# @Author  : 叶永彬
# @File    : test_couponRefund.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.parkingManage_service.businessCoupon_service.sellManage import SellManage
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/couponRefund.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("优惠劵管理")
class TestCouponRefund(BaseCase):
    """优惠劵退款"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon(userLogin).addCoupon(send_data["couponName"],send_data["parkName"],send_data["traderName"],send_data["couponType"])
        result = re.json()
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon(userLogin).addSell(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["addSellMessage"])

    def test_checkCouponOnTrader(self,weiXinLogin,send_data,expect):
        """商户端查看优惠劵"""
        re = WeiXin(weiXinLogin).findCouponList()
        result = re.json()
        Assertions().assert_in_text(result, expect["checkCouponOnTraderMsg"])

    def test_refundCoupon(self,userLogin,send_data,expect):
        """优惠劵退款"""
        re = SellManage(userLogin).couponRefund(send_data['parkName'],send_data['couponName'])
        result = re.json()
        Assertions().assert_in_text(result, expect["refundCouponMsg"])

    def test_checkCouponAgain(self,weiXinLogin,send_data,expect):
        """商户端再次查看优惠劵"""
        re = WeiXin(weiXinLogin).findCouponList()
        result = re.json()
        Assertions().assert_not_in_text(result, expect["checkCouponOnTraderMsg"])
