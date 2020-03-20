#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 11:26
# @Author  : 叶永彬
# @File    : test_traderSell.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.trader import Trader
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/traderSell.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("商户管理")
class TestTraderSell(BaseCase):
    """商家售卖-在商家管理页面售卖券"""
    def test_addTrader(self,userLogin,send_data,expect):
        """新增商户"""
        re = Trader(userLogin).addTrader(send_data["traderName"], send_data["parkName"], send_data['account'],send_data['couponName'])
        result = re.json()
        self.save_data('account', send_data['account'])
        Assertions().assert_in_text(result, expect["addTraderMessage"])

    def test_traderSell(self,userLogin,send_data,expect):
        """商家售卖"""
        re = Trader(userLogin).addSell(send_data['parkName'], send_data['traderName'],send_data['couponName'])
        result = re.json()
        Assertions().assert_in_text(result, expect["traderSellMsg"])

    @pytest.mark.parametrize('weiXinLogin',[{'user':'${mytest.account}','pwd':'123456'}],indirect=True)
    def test_grantCouponToCar(self,weiXinLogin,send_data,expect):
        """商家下发优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data['couponName'],send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["grantCouponToCarMsg"])

    def test_deleteTrader(self,userLogin,send_data,expect):
        """商户删除"""
        re = Trader(userLogin).deleteTrader(send_data['parkName'],send_data["traderName"])
        result = re.json()
        Assertions().assert_in_text(result, expect["deleteTraderMessage"])

    def test_checkDeleteTrader(self,userLogin,send_data,expect):
        """查看已删除商户是否存在"""
        re = Trader(userLogin).getTraderListData(send_data['parkName'],send_data["traderName"])
        result = re.json()['rows']
        Assertions().assert_not_in_text(result, expect["checkDeleteTraderMsg"])
