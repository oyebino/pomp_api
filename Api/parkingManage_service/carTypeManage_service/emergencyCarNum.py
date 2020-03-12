#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 14:36
# @Author  : 叶永彬
# @File    : emergencyCarNum.py

from common.Req import Req
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class EmergencyCarNum(Req):
    """指定车牌录入"""

    def __getParkingBaseDataTree(self):
        """获取车场树"""
        data = {
            "parkSysType":1
        }
        self.url = "/mgr/parkingBaseData/getParkingBaseDataTree.do?" + urlencode(data)
        re = self.get(self.api)
        return re

    def __isExistCarNum(self, id, carNum):
        """检查车牌是否存在"""
        self.url = "/mgr/park/emergency/carNo/check.do"
        data = {
            "carCode": carNum,
            "parkIds": id
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def createEmergencyCarNum(self, parkName, carNum, tel):
        """创建指定车牌"""
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(), 'name', parkName)
        isExistCar = self.__isExistCarNum(parkDict['value'], carNum)
        if isExistCar.json()['message'] == None:
            self.url = "/mgr/park/emergency/carNo/create.do"
            data = {
                "id":0,
                "carCode": carNum + '蓝',
                "mobile": tel,
                "parkIds": parkDict['value']
            }
            re = self.post(self.api, data = data, headers = form_headers)
            return re
        else:
            return isExistCar

    def updateEmergencyCarNum(self, parkName, OldCarNum, newCarNum):
        """修改指定车牌"""
        EmergencyCarNumInfoDict = self.__getEmergencyCarNumById(parkName, OldCarNum).json()['data']
        isExistCar = self.__isExistCarNum(EmergencyCarNumInfoDict['parkIdList'][0], newCarNum)
        if isExistCar.json()['message'] == None:
            data = {
                "id": EmergencyCarNumInfoDict['id'],
                "carCode": newCarNum + '蓝',
                "mobile": EmergencyCarNumInfoDict['mobile'],
                "parkIds": EmergencyCarNumInfoDict['parkIdList'][0]
            }
            self.url = "/mgr/park/emergency/carNo/update.do"
            re = self.post(self.api, data = data, headers = form_headers)
            return re
        else:
            return isExistCar

    def __getEmergencyCarNumById(self, parkName, carNum):
        """通过Id获取指定车牌信息"""
        EmergencyCarNumDict = self.getDictBykey(self.getEmergencyCarNumList(parkName).json(), 'carCode', carNum + '蓝')
        data = {
            "id": EmergencyCarNumDict['id']
        }
        self.url = "/mgr/park/emergency/carNo/getById.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def delEmergencyCarNum(self, parkName, carNum):
        """删除指定车牌"""
        EmergencyCarNumDict = self.getDictBykey(self.getEmergencyCarNumList(parkName).json(), 'carCode', carNum + '蓝')
        self.url = "/mgr/park/emergency/carNo/delete.do"
        data = {
            "id": EmergencyCarNumDict['id']
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def getEmergencyCarNumList(self, parkName):
        """获取指定车牌列表"""
        parkDict = self.getDictBykey(self.__getParkingBaseDataTree().json(), 'name', parkName)
        data = {
            "page": 1,
            "pageSize": 20,
            "parkIds": parkDict['value'],
            "parkSysType": 1
        }
        self.url = "/mgr/park/emergency/carNo/list.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def __getEmergencyConfigList(self):
        """查询告警设置"""
        self.url = "/mgr/park/emergency/config/getCarlist.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def updateEmergencySetting(self, carnoIn = True, carnoOut = True, lmCarcodeIn = True, lmCarcodeOut = True):
        """设置告警设置"""
        EmergencyConfigDict = self.__getEmergencyConfigList().json()['data']
        self.url = "/mgr/park/emergency/config/updateCarlist.do"
        data = {
            "id":EmergencyConfigDict['id'],
            "carnoIn": carnoIn,
            "carnoOut": carnoOut,
            "lmCarcodeIn": lmCarcodeIn,
            "lmCarcodeOut": lmCarcodeOut
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re
