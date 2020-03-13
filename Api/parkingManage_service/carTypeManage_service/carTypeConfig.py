#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 17:27
# @Author  : 叶永彬
# @File    : carTypeConfig.py

from common.Req import Req
from urllib.parse import urlencode
from common.superAction import SuperAction as SA
from common import const
import json

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

specialCarTypeDict = {
    "黑名单":2,
    "访客":1,
    "预定":3
}
today = SA().get_today_data()

class CarType(Req):
    """车辆分类"""
    aList = []
    def createSpecialType(self, parkName, specialCarType, typeName):
        """创建特殊类型"""
        parkInfoDict = self.getDictBykey(Index(self.Session).getUnsignedParkList().json(), 'name', parkName)
        optionArrList = self.__selectChargeGrooupList(parkInfoDict['parkUUID']).json()['data'][parkInfoDict['parkUUID']]
        parkJson = [{
            "parkSysType": 1,
            "parkVipTypeId": "",
            "parkLongId": parkInfoDict['id'],
            "parkId": parkInfoDict['parkUUID'],
            "parkName": parkName,
            "chargeGroupCode": "0",
            "optionArr": optionArrList
        }]
        channelAuthTree = self.getDictBykey(self.__getChannelAuthTreeMultiPark().json(), 'name', parkName)
        self.__getDictChildList(channelAuthTree,'childrenList')
        newChannelAuthTree = json.dumps(self.setValueByDict(self.aList, ['checked'], True))

        parkVipTypeJson = {
            "customVipName": "",
            "settlementType": 0,
            "isDynamicMode": 0,
            "isDatePrivilege": 0,
            "isTimePrivilege": 0,
            "privilegeTimePeriod": "",
            "isChargeGroupRelated": 0,
            "vipGroupType": 0,
            "dynamicFullLimit": 0,
            "vipNearExpiredDayThreshold": 10,
            "vipDeleteExpiredDayThreshold": 0,
            "openVipFullLimit": 0,
            "vipFullLimitValue": "",
            "vipFullOpenModel": 0,
            "priTimeArrFrom": "",
            "priTimeArrTo": "",
            "priDateArrStr": "",
            "parkId": "",
            "parkName": "",
            "channelAuthTree": str(newChannelAuthTree),
            "channelSeqList": [],
            "autoSwitchVip": 0,
            "offLine": 1
        }
        data = {
            "parkSysType": 1,
            "vipGroupType": specialCarTypeDict[specialCarType],
            "name": typeName,
            "description": "pytest",
            "parkJson": str(parkJson),
            "renewFormerDays":1,
            "inviteCarTotal":3,
            "parkVipTypeJson": str(parkVipTypeJson),
            "showMessage": const.showMessage
        }
        self.url = "/mgr/park/specialCarTypeConfig/add.do"
        print(data['parkVipTypeJson'])
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def __getChannelAuthTreeMultiPark(self):
        """获取全部车场区域进出口树"""
        self.url = "/mgr/vip/vipType/getChannelAuthTreeMultiPark.do"
        data = {
            "parkId":None,
            "vipTypeId":None,
            "parkSysType":1,
            "canCheckAll":1
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def __selectChargeGrooupList(self,parkId):
        """列出车场全部计费组"""
        data = {
            "parkIdList": parkId
        }
        self.url = "/mgr/park/specialCarTypeConfig/selectChargeGroupList2.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def getSpecialCarTypeCofig(self):
        """获取特殊车辆配置列表"""
        data = {
            "page":1,
            "rp":20,
        }
        self.url = "/mgr/park/specialCarTypeConfig/pageList.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def updataSpecialCarTypeConfig(self, oldTypeName, newTypeName):
        """编辑车辆基础配置"""
        typeConfigDict = self.getDictBykey(self.getSpecialCarTypeCofig().json(), 'name', oldTypeName)
        typeConfigDetailDict = self.getSpecialCarTypeDetail(typeConfigDict['id']).json()['data']
        optionArrList = self.__selectChargeGrooupList(typeConfigDict['financialParkId']).json()['data'][typeConfigDict['financialParkId']]
        optionArrDict = {'optionArr': optionArrList}
        parkJsonList = []
        if typeConfigDetailDict['vipGroupType'] == specialCarTypeDict['黑名单']:
            blacklistConfigDict = self.getDictBykey(typeConfigDetailDict['blacklistConfigParkList'][0], 'parkId', typeConfigDetailDict['financialParkId'])
            blacklistConfigDict.update(optionArrDict)
            parkJsonList.append(blacklistConfigDict)
        elif typeConfigDetailDict['vipGroupType'] == specialCarTypeDict['访客']:
            visitorConfigParkDict = self.getDictBykey(typeConfigDetailDict['visitorlistConfigParkList'][0], 'parkId', typeConfigDetailDict['financialParkId'])
            visitorConfigParkDict.update(optionArrDict)
            parkJsonList.append(visitorConfigParkDict)

        channelAuthTree = typeConfigDetailDict['channelAuthTree']
        parkVipTypeDict = typeConfigDetailDict['parkVipType']
        parkVipTypeJson = {
            "id": parkVipTypeDict['id'],
            "customVipName": parkVipTypeDict['customVipName'],
            "settlementType": parkVipTypeDict['settlementType'],
            "settlementAmount": parkVipTypeDict['settlementAmount'],
            "isDynamicMode": parkVipTypeDict['isDynamicMode'],
            "isDatePrivilege": parkVipTypeDict['isDatePrivilege'],
            "isTimePrivilege": parkVipTypeDict['isTimePrivilege'],
            "privilegeTimePeriod": parkVipTypeDict['privilegeTimePeriod'],
            "isChargeGroupRelated": parkVipTypeDict['isChargeGroupRelated'],
            "vipGroupType": parkVipTypeDict['vipGroupType'],
            "dynamicFullLimit": parkVipTypeDict['dynamicFullLimit'],
            "dynamicCarNumber": parkVipTypeDict['dynamicCarNumber'],
            "vipNearExpiredDayThreshold": parkVipTypeDict['vipNearExpiredDayThreshold'],
            "vipDeleteExpiredDayThreshold": parkVipTypeDict['vipDeleteExpiredDayThreshold'],
            "openVipFullLimit": parkVipTypeDict['openVipFullLimit'],
            "vipFullOpenModel": parkVipTypeDict['vipFullOpenModel'],
            "priDateArrStr": parkVipTypeDict['priDateArrStr'],
            "parkId": parkVipTypeDict['parkId'],
            "parkName": parkVipTypeDict['parkName'],
            "channelAuthTree": channelAuthTree
        }
        data = {
            "id": typeConfigDetailDict['id'],
            "vipGroupType": typeConfigDetailDict['vipGroupType'],
            "parkSysType": typeConfigDetailDict['parkSysType'],
            "name": newTypeName,
            "description": typeConfigDetailDict['description'],
            "financialParkId": typeConfigDetailDict['financialParkId'],
            "parkJson": json.dumps(parkJsonList),
            "parkVipTypeJson": json.dumps(parkVipTypeJson),
            "showMessage": typeConfigDetailDict['showMessage']
        }
        self.url = "/mgr/park/specialCarTypeConfig/edit.do"
        re = self.post(self.api, data= data, headers = form_headers)
        return re

    def delSpecialCarType(self, typeName):
        """删除特殊车辆分类配置"""
        typeConfigDict = self.getDictBykey(self.getSpecialCarTypeCofig().json(), 'name', typeName)
        self.url = "/mgr/park/specialCarTypeConfig/del.do"
        data = {
            "configId": typeConfigDict['id']
        }
        re = self.post(self.api, data=data, headers=form_headers)
        return re

    def getSpecialCarTypeDetail(self, typeId):
        """按记录查看特殊车辆配置详细信息"""
        data = {
            "id":typeId
        }
        self.url = "/mgr/park/specialCarTypeConfig/detail.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def __getDictChildList(self, json, key):

        """查找json的key把对应的value对象递归存放在list"""
        self.aList.append(json)
        for item in json:
            if item == key:
                if isinstance(json[key], list):
                    for i in json[key]:
                        self.__getDictChildList(i, key)

from Api.index_service.index import Index
class ParkVisitor(Req):
    """访客车录入"""
    def addVisitor(self, visitorType, carNum):
        """新建访客车辆"""
        visitorTypeDict = self.getDictBykey(self.__getVisitorConfigList().json(), 'name', visitorType)
        self.url = "/mgr/park/parkVisitorlist/save.do"
        data = {
            "specialCarTypeConfigId": visitorTypeDict['id'],
            "carLicenseNumber": carNum,
            "owner": 'apipytest',
            "ownerPhone": '135' + SA().create_randomNum(val = 8),
            "visitReason": 'apipytest',
            "remark1": "apipytest",
            "visitFrom": today +' 00:00:00',
            "visitTo": today + ' 23:59:59'
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def delVisitor(self, parkName, carNum):
        """删除访客车辆"""
        visitorDict = self.getDictBykey(self.getParkVisitorList(parkName).json(), 'carLicenseNumber', carNum)
        self.url = "/mgr/park/parkVisitorlist/del.do"
        data = {
            "parkVisitorlistId": visitorDict['id'],
        }
        re = self.post(self.api, data= data, headers = form_headers)
        return re

    def __getVisitorConfigList(self):
        """查看访客配置列表"""
        self.url = "/mgr/park/parkVisitorlist/getVisitorConfigList.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def getParkVisitorList(self, parkName):
        """获取访客录入车辆"""
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp": 20,
            "startDate": today + ' 00:00:00',
            "endDate": today + ' 23:59:59',
            "parkIds": parkDict['value'],
            "parkSysType": 1,
        }
        self.url = "/mgr/park/parkVisitorlist/getParkVisitorlist.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

class ParkBlacklist(Req):
    """黑名单录入"""
    def addBlacklist(self, blackType, carNum):
        """新建黑名单车辆"""
        blackTypeDict = self.getDictBykey(self.__getBlacklistConfig().json(), 'name', blackType)
        self.url = "/mgr/park/parkBlacklist/save.do"
        data = {
            "specialCarTypeConfigId": blackTypeDict['id'],
            "carLicenseNumber": carNum,
            "owner": 'apipytest',
            "reason": 'pytest',
            "remark1": 'pytest',
            "blacklistForeverFlag": 'CLOSE',
            "availTimeFromTo": today + ' 00:00:00~' + today + ' 23:59:59',
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def __getBlacklistConfig(self):
        """获取黑名单配置"""
        self.url = "/mgr/park/parkBlacklist/getBlacklistConfigList.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def delBlacklist(self, parkName, carNum):
        """删除黑名单"""
        blacklistDict = self.getDictBykey(self.getBlacklist(parkName).json(), 'carLicenseNumber', carNum)
        self.url = "/mgr/park/parkBlacklist/del.do"
        data = {
            "parkBlacklistId": blacklistDict['id']
        }
        re = self.post(self.api, data= data, headers= form_headers)
        return re

    def getBlacklist(self, parkName):
        """获取黑名单列表"""
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp": 20,
            "startDate": today + ' 00:00:00',
            "endDate": today + ' 23:59:59',
            "parkIds": parkDict['value'],
            "parkSysType": 1,
        }
        self.url = '/mgr/park/parkBlacklist/getParkBlacklist.do?' + urlencode(data)
        re = self.get(self.api)
        return re

class ParkWhitelist(Req):
    """白名单"""
    def addWhitelist(self, parkName, carNum):
        """录入白名单"""
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        self.url = "/mgr/park/park_redlist/add.do"
        data = {
            "redlistParam":carNum,
            "parkIds": parkDict['value']
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def delWhilelist(self, carNum):
        """删除白名单规则"""
        WhilelistDict = self.getDictBykey(self.getWhilelistRuleList().json(), 'redlistParam', carNum)
        self.url = "/mgr/park/park_redlist/del.do"
        data = {
            "id": WhilelistDict['id']
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def getWhilelistRuleList(self):
        """获取白名单规则列表"""
        self.url = "/mgr/park/park_redlist/getRules.do"
        re = self.get(self.api, headers = form_headers)
        return re