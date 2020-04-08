#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 11:44
# @Author  : 叶永彬
# @File    : test_createGrantUser.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from common.BaseCase import BaseCase
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/createGrantUser.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("商家应用")
@allure.story('创建发放员并发劵')
class TestCreateGrantUser(BaseCase):
    """商户应用-发劵授权-创建发放员并发劵"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon(userLogin).addCoupon(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon(userLogin).addSell(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re
        Assertions().assert_in_text(result, expect["addSellMessage"])

    def test_createGrantUser(self, weiXinLogin, send_data, expect):
        """在发劵授权-创建发放员"""
        re = WeiXin(weiXinLogin).createGrantUser(send_data['grantUserName'], send_data['account'], send_data['pwd'])
        result = re
        self.save_data('grantUserName', send_data['grantUserName'])
        self.save_data('account', send_data['account'])
        Assertions().assert_in_text(result, expect['createGrantUserMsg'])

    @pytest.mark.parametrize('weiXinLogin',[{'user':'${mytest.account}','pwd':'123456'}], indirect= True)
    def test_grantUserSendCouponToCar(self, weiXinLogin, send_data, expect):
        """发放员放发优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data['couponName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["grantUserSendCouponToCarMsg"])

    def test_checkCouponSendList(self,userLogin,send_data,expect):
        """查看发放流水"""
        re = Coupon(userLogin).getCouponGrantList(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkCouponSendListMsg"])

    def test_delGrantUser(self, weiXinLogin, send_data, expect):
        """删除发放员"""
        re = WeiXin(weiXinLogin).delGrantUser(send_data['grantUserName'])
        result = re
        Assertions().assert_in_text(result, expect["delGrantUserMsg"])

    def test_isDelGrantUser(self, weiXinLogin, send_data, expect):
        """查看已删除发放员是否存在"""
        re = WeiXin(weiXinLogin).getGrantUserList()
        result = re
        Assertions().assert_not_in_text(result, expect["isDelGrantUser"])