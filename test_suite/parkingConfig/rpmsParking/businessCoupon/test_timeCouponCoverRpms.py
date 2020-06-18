#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 15:28
# @Author  : 叶永彬
# @File    : test_timeCouponCoverRpms.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.offLineParking_service.rpmsParkingReq import RpmsParkingReq
from Api.parkingManage_service.businessCoupon_service.trader import Trader
from Api.information_service.information import Information
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/rpmsParking/businessCoupon/timeCouponCover.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("线下车场-电子优惠管理模块")
@allure.story('rmps可叠加时间劵创建并使用')
@pytest.mark.skip(reason='存在bug，编号：15503')
class TestRpmsTimeCouponCover():
    """rmps可叠加时间劵创建并使用"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon(userLogin).addCoupon(send_data["couponName"],send_data["parkName"],send_data["traderName"],send_data["couponType"],faceValue =send_data["faceValue"],isCover=send_data["isCover"])
        result = re
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon(userLogin).addSell(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re
        Assertions().assert_in_text(result, expect["addSellMessage"])
    def test_checkTraderAccount(self,userLogin,send_data,expect):
        """查找商家"""
        re =Trader(userLogin).getTraderListData(send_data['parkName'],send_data['traderName'])
        result = re
        self.save_data('traderAccount',result[0]['account'])
        Assertions().assert_in_text(result, expect["traderAccountMsg"])

    @pytest.mark.parametrize('weiXinLogin', [{'user': '${mytest.traderAccount}', 'pwd': '123456'}], indirect=True)
    def test_sendCoupon(self,weiXinLogin,send_data,expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_mockCarIn(self, rmpsLogin,send_data,expect):
        """模拟车辆进场"""
        re = RpmsParkingReq(rmpsLogin).carIn(send_data["parkCode"], send_data['rmpsParkName'], send_data["carNum"])
        result = re['message']
        Assertions().assert_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self,rmpsLogin,send_data, expect):
        """模拟车辆出场"""
        re = RpmsParkingReq(rmpsLogin).carOut(send_data["parkCode"], send_data["rmpsParkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费流水"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkParkingBillDetailMessage"])

    def test_checkCouponSendList(self,userLogin,send_data,expect):
        """查看发放流水"""
        re = Coupon(userLogin).getCouponGrantList(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkCouponGrantListMessage"])

    def test_checkCouponUsedList(self,userLogin,send_data,expect):
        """查看使用流水"""
        re = Coupon(userLogin).getCouponSerialList(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkSerialListMessage"])