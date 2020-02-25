#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : pp.py


# from Api.parkingManage_service.businessCoupon import Businessman
# class TestAAA():
#
#     def test_A(self,userLogin):
#         re = Businessman(userLogin).getCoupon2BugByTraderId('897')
#         re.json()

a ={
    "a":1,
    "b":[
        {
            "c":1
        },{
            "c":2
        },{
            "c":3
        }
    ]
}

for i,val in enumerate(a['b']):
    if val['c'] == 3:
        print(i)