#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : pp.py
from Api.sentry_service.carInOutHandle import CarInOutHandle
# from Api.information.information_controller import Information_controller
import pytest
# class TestAAA():
#
#
#     def test_A(self,sentryLogin):
#         # re = CarInOutHandle(sentryLogin).adjust_carNum_carType("54a33015-d405-499e-bce2-e569cd9dce6a","粤EEEEFG",carType='2')
#         # re = CarInOutHandle(sentryLogin).get_id_message('54a33015-d405-499e-bce2-e569cd9dce6a')
#         # re = CarInOutHandle(sentryLogin).check_car_in_out('54a33015-d405-499e-bce2-e569cd9dce6a')
#         re = CarInOutHandle(sentryLogin).record_car_in('京CCCCC3F')
#
#         # re.json()
#         # b = '3916,3751'
#         # re = Information_controller(userLogin).getAdjustCarWaterNum("粤DDDDFG",b)
#         re.json()

temple = """
    - test:
    name: 临时车宽进-不需缴费宽出
    desc: 临时车宽进-不需缴费宽出
    send_data:
      parkId: ${FreePark_parkID}
      carNum: ${__create_carNum()}
      inClientID: ${freePark_lightRule_inClientID}
      outClientID: ${freePark_lightRule_outClientID}
    except:
      mockCarInMessage: 欢迎光临
      presentCarMessage: ${__create_carNum()}
      parkingBillDetailMessage: ${__create_carNum()}
      mockCarOutMessage: 一路顺风
      carLeaveHistoryMessage: ${__create_carNum()}

"""
import re
rule = r'${__(.*?)}'
a = re.match(rule,temple)
print(a)