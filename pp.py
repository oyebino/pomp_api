#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : pp.py
from Api.parking_service.businessCoupon_service import Coupon_controller
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions
# import sys,os
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
# class TestAAA():
#     def test_A(self):
#        # re = Information_controller(userLogin).getParkingBillDetail("3751","粤Y59084")
#        # result = re.json()
#        print(BASE_DIR)
#        print('kkkkkkkk:'+str(os.path.exists('E:\POMP_API/test_data/commo1nData.xml')))
#        print(os.getcwd())
#        print(os.path.basename(__file__))
#        print("["+sys._getframe().f_code.co_name+"]")

from Config.parameter import tempDataPath

from common.superAction import SuperAction
parm = {'str':3}
pa=1,2
key = "runTest"
c = getattr(SuperAction(),key)

value = c(*pa,**parm)
print(value)


# key = "create_carNum(1,2)"
# indexNum =key.index('(')
# funName = key[0:indexNum]
# if key[indexNum+1:-1]=="":
#     pass
# else:
#     parmList = key[indexNum+1:-1].split(',')
#     kwargsList=list()
#     argsList=list()
#     for parm in parmList:
#         if parm.rfind('=')>=0:
#             kwargsList.append(parm)
#         else:
#             argsList.append(parm)
#
#     print(kwargsList)
#     s = ",".join(kwargsList)
#     kwargsdict=dict((l.split('=') for l in s.split(',')))
#     print(kwargsdict)
#     print(len(argsList)==0)
    # print(tuple(argsList))
