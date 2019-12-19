#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 15:26
# @Author  : 叶永彬
# @File    : pp.py
from Api.parking_service.monthTicket_service import monthTicket_controller

class TestA():
    def test_A(self,userLogin):
       re = monthTicket_controller(userLogin).save_monthTicketType()
       print(re.json())
