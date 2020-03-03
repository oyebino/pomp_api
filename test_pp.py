#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : test_pp.py

import pytest
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.parkingConfig_service.parkingSetting import ParkingSetting
from Api.index_service.index import Index

class TestAAA():
    # @pytest.mark.parametrize('userLogin', [{'user':'yeyongbin','pwd':'123456'}], indirect=True)
    def test_A(self,sentryLogin):

        # re = Coupon(userLogin).getParkingBaseTree('智泊云接口测试专用停车场')
        # re = Coupon(userLogin).getCouponGrantList('智泊云接口测试专用停车场','粤E84352')
        # re = CarInOutHandle(sentryLogin).match_carNum('桂CCCBC4','桂CCCBC7')
        re = CarInOutHandle(sentryLogin).carInOutHandle('桂AAAABC4','登记放行')
        # re = ParkingSetting(userLogin).getOperatorParkConfigListView()
        # re = Information(userLogin).getPresentCar('智泊云接口测试专用停车场','桂AAAABC4')
        # re = Index(userLogin).getNewMeun()
        re.json()