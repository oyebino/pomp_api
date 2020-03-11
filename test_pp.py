#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : test_pp.py

from Api.parkingManage_service.carTypeManage_service.carTypeManage import CarTypeManage
from Api.parkingManage_service.carTypeManage_service.carType import CarType
import pytest


class TestAAA():
    # @pytest.mark.parametrize('userLogin', [{'user':'yeyongbin','pwd':'123456'}], indirect=True)
    def test_A(self,userLogin):

        # re = Coupon(userLogin).getParkingBaseTree('智泊云接口测试专用停车场')
        # re = CityCoupon(openYDTLogin).grantCityOperationCoupon('8STJJ8D6TU72','粤Y98075')
        # re = CarInOutHandle(sentryLogin).getCarOutRecord('粤W13584','智泊云接口测试专用停车场')
        # re = CarInOutHandle(sentryLogin).carInOutHandle('桂AAAABC4','登记放行')
        # re = ParkingSetting(userLogin).updataOperatorParkCofigInfo('智泊云接口测试专用停车场',['data','parkCloudDetailVo','openFuzzyMatch'],False)
        # re = ParkingSetting(userLogin).getOperatorParkConfigInfo('智泊云接口测试专用停车场')
        # re = SellManage(userLogin).couponRefund('智泊云接口测试专用停车场','api退款劵0328')
        # re = Information(userLogin).getPresentCar('智泊云接口测试专用停车场','桂AAAABC4')
        # re = Index(userLogin).getNewMeun()
        re = CarType(userLogin).updataSpecialCarTypeConfig('kkk779','kkk889')
        # re = CarType(userLogin).runTest()
        re.json()


