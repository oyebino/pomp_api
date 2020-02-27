#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : test_pp.py

import pytest
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
class TestAAA():
    @pytest.mark.parametrize('weiXinLogin', [{'user':'13504915876','pwd':'123456'}], indirect=True)
    def test_A(self,weiXinLogin):
        re = WeiXin(weiXinLogin).findCouponList()
        re.json()


