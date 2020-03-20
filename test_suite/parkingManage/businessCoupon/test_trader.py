#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 16:38
# @Author  : 叶永彬
# @File    : test_trader.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.trader import Trader
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
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
        re = Trader(userLogin).addTrader(send_data["name"],send_data["parkName"],send_data['account'],send_data['couponName'],send_data['pwd'])
        result = re.json()
        self.save_data('account', send_data['account'])
        self.save_data('pwd', send_data['pwd'])
        Assertions().assert_in_text(result,expect["addTraderMessage"])

    def test_disAbleTrader(self,userLogin,send_data,expect):
        """商户冻结"""
        re = Trader(userLogin).disAbleTrader(send_data['parkName'], send_data["name"])
        result = re.json()
        Assertions().assert_in_text(result, expect["disAbleTraderMessage"])

    @pytest.mark.parametrize('weiXinLogin',[{'user':'${mytest.account}','pwd':'${mytest.pwd}'}], indirect=True)
    def test_disAbleLoginWeiXin(self,weiXinLogin,send_data,expect):
        """商户不能操作微信客户端"""
        re = WeiXin(weiXinLogin).getMyCoupons()
        result = re.text
        Assertions().assert_in_text(result, expect["disAbleLoginWeiXinMsg"])

    def test_enableTrader(self,userLogin,send_data,expect):
        """商户启用"""
        re = Trader(userLogin).enableTrader(send_data['parkName'],send_data["name"])
        result = re.json()
        Assertions().assert_in_text(result, expect["enableTraderMessage"])

    @pytest.mark.parametrize('weiXinLogin', [{'user': '${mytest.account}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_enableLoginWeiXin(self,weiXinLogin,send_data,expect):
        """商户可以操作微信客户端"""
        re = WeiXin(weiXinLogin).getMyCoupons()
        result = re.json()
        Assertions().assert_in_text(result, expect["enableLoginWeiXinMessage"])

    def test_editTrader(self,userLogin,send_data,expect):
        """商户编辑"""
        re = Trader(userLogin).editTrader(send_data['name'],send_data["editName"],send_data['parkName'])
        result = re.json()
        self.save_data('editName',send_data["editName"])
        Assertions().assert_in_text(result, expect["editTraderMessage"])

    def test_checkEditTrader(self,userLogin,send_data,expect):
        """查看修改后商户"""
        re = Trader(userLogin).getTraderListData(send_data["parkName"],send_data["editName"])
        result = re.json()['data']['rows']
        Assertions().assert_in_text(result, expect["checkEditTraderMessage"])

    def test_deleteTrader(self,userLogin,send_data,expect):
        """商户删除"""
        re = Trader(userLogin).deleteTrader(send_data['parkName'],send_data["editName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["deleteTraderMessage"])

    def test_checkDeleteTrader(self,userLogin,send_data,expect):
        """查看已删除商户是否存在"""
        re = Trader(userLogin).getTraderListData(send_data['parkName'],send_data["editName"])
        result = re.json()['data']['rows']
        Assertions().assert_not_in_text(result, expect["checkDeleteTraderMsg"])