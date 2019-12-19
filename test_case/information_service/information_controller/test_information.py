#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 16:34
# @Author  : 叶永彬
# @File    : test_information.py

from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service

class TestParkingInformation():

    def test_checkInsideCar(self,userLogin):
        cloudparking_service().mock_car_in_out()
        re =Information_controller(userLogin).getPresentCar("3751")
        print(re.json())