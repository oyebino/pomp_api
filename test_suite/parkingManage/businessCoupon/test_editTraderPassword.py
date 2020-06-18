#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 14:22
# @Author  : 叶永彬
# @File    : test_editTraderPassword.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.trader import Trader
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/editTraderPassword.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("商户管理")
@allure.story('新增-修改-删除商户流程')
@pytest.mark.skip(reason='bug号：16593')
class TestEditTraderPassword(BaseCase):
    """新增商户流程"""
    def test_addTrader(self,userLogin,send_data,expect):
        """商户新增"""
        re = Trader(userLogin).addTrader(send_data["name"],send_data["parkName"],send_data['account'],send_data['couponName'],send_data['pwd'])
        result = re
        self.save_data('account',send_data['account'])
        self.save_data('pwd', send_data['pwd'])
        Assertions().assert_in_text(result,expect["addTraderMessage"])

    def test_editTraderPwd(self,userLogin,send_data,expect):
        """修改密码"""
        re = Trader(userLogin).editTrader(send_data['name'],send_data['name'],send_data['parkName'],send_data['editPwd'])
        result = re
        self.save_data('editPwd',send_data['editPwd'])
        Assertions().assert_in_text(result, expect["editTraderPwdMsg"])

    @pytest.mark.parametrize('weiXinLogin',[{'user':'${mytest.account}','pwd':'${mytest.pwd}'}], indirect=True)
    def test_disAbleLoginWeiXin(self,weiXinLogin,send_data,expect):
        """旧密码商户不能操作微信客户端"""
        re = WeiXin(weiXinLogin).checkTraderCouponPay()
        result = re
        Assertions().assert_in_text(result, expect["disAbleLoginWeiXinMsg"])

    @pytest.mark.parametrize('weiXinLogin', [{'user': '${mytest.account}', 'pwd': '${mytest.editPwd}'}], indirect=True)
    def test_enAbleLoginWeiXin(self,weiXinLogin,send_data,expect):
        """新密码商户能登录微信商户端"""
        re = WeiXin(weiXinLogin).checkTraderCouponPay()
        result = re
        Assertions().assert_in_text(result, expect["enAbleLoginWeiXinMsg"])

    def test_deleteTrader(self,userLogin,send_data,expect):
        """商户删除"""
        re = Trader(userLogin).deleteTrader(send_data['parkName'],send_data["name"])
        result = re
        Assertions().assert_in_text(result, expect["deleteTraderMessage"])

    @pytest.mark.parametrize('weiXinLogin', [{'user': '${mytest.account}', 'pwd': '${mytest.editPwd}'}], indirect=True)
    def test_disAbleLoginWeiXinAfterDel(self,weiXinLogin,send_data,expect):
        """商户删除不能登录"""
        re = WeiXin(weiXinLogin).checkTraderCouponPay()
        result = re
        Assertions().assert_in_text(result, expect["disAbleLoginWeiXinAfterDelMsg"])