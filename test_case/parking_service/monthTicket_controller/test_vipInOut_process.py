#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 15:33
# @Author  : 叶永彬
# @File    : test_vipInOut_process.py

from Api.parking_service.monthTicket_service import monthTicket_controller
class TestMonthTicket():
    def test_vip_car_in(self,userLogin):
        re = monthTicket_controller(userLogin).save_monthTicketType()
        print(re.json())