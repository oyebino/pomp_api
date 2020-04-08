#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 15:41
# @Author  : 叶永彬
# @File    : test_centralHandOverCentralDuty.py

import allure,pytest
from common.utils import YmlUtils
from Api.centralTollCollection_service.centralPersonalInfo import CentralPersonalInfo
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centralTollCollectionRoom/personalInfo/centralHandOverCentralDuty.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央收费处")
@allure.story('中央收费处交接班')
class TestCentralHandOverCentralDuty(BaseCase):

    def test_handOverCentralDuty(self, centralTollLogin, send_data,expect):
        """中央交接班"""
        re = CentralPersonalInfo(centralTollLogin).handOverCentralDuty(send_data['handOverUser'],send_data['handOverPwd'])
        result = re['nick_name']
        Assertions().assert_text(result, expect['handOverCentralDutyMsg'])