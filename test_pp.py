#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : test_pp.py

from Api.parkingManage_service.carTypeManage_service.emergencyCarNum import EmergencyCarNum
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import CarType,ParkVisitor, ParkBlack,ParkWhitelist
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.index_service.index import Index
import pytest


class TestAAA():
    # @pytest.mark.parametrize('sentryLogin', [{'user':'zhangsi','pwd':'123456'}], indirect=True)
    # @pytest.mark.parametrize('userLogin', [{'user': 'ljxtest', 'pwd': '123456'}], indirect=True)
    def test_A(self,userLogin):

        # re = Coupon(userLogin).getParkingBaseTree('智泊云接口测试专用停车场')
        # re = CityCoupon(openYDTLogin).grantCityOperationCoupon('8STJJ8D6TU72','粤Y98075')
        # re = CarInOutHandle(sentryLogin).getCarOutRecord('粤W13584','智泊云接口测试专用停车场')
        # re = CarInOutHandle(sentryLogin).getCarInRecord('桂AAAABC4','澳门旧葡京')
        # re = CarInOutHandle(sentryLogin).getCarInRecord('桂AAAABC4','智泊云接口测试专用停车场')
        # re = ParkingSetting(userLogin).updataOperatorParkCofigInfo('智泊云接口测试专用停车场',['data','parkCloudDetailVo','openFuzzyMatch'],False)
        # re = ParkingSetting(userLogin).getOperatorParkConfigInfo('智泊云接口测试专用停车场')
        # re = SellManage(userLogin).couponRefund('智泊云接口测试专用停车场','api退款劵0328')
        re = Information(userLogin).cleanCarNum('智泊云接口测试专用停车场','粤A12346')
        # re = Index(userLogin).getNewMeun()
        # re = CarType(userLogin).updataSpecialCarTypeConfig('kkk779','kkk889')
        # re = EmergencyCarNum(userLogin).delEmergencyCarNum('智泊云接口测试专用停车场', '粤A*')
        # re = ParkWhitelist(userLogin).delWhilelist('粤55555')
        re.json()


