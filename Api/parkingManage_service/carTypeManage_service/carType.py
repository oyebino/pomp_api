#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 17:27
# @Author  : 叶永彬
# @File    : carType.py

from common.Req import Req
from urllib.parse import urlencode
from Api.index_service.index import Index
from common import const
import json

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

specialCarTypeDict = {
    "黑名单":2,
    "访客":1,
    "预定":3
}

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
        visitorConfigParkDict = self.getDictBykey(typeConfigDetailDict['visitorlistConfigParkList'][0], 'parkId', typeConfigDetailDict['financialParkId'])
        optionArrList = self.__selectChargeGrooupList(typeConfigDict['financialParkId']).json()['data'][typeConfigDict['financialParkId']]
        optionArrDict = {'optionArr':optionArrList}
        visitorConfigParkDict.update(optionArrDict)
        parkJsonList = []
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

if __name__ == "__main__":
   aa = {
            "chkDisabled": False,
            "parkUuid": "54a33015-d405-499e-bce2-e569cd9dce6a",
            "level": 0,
            "hasChildren": True,
            "name": "智泊云接口测试专用停车场",
            "parkSysType": 1,
            "checked": False,
            "nocheck": False,
            "type": 0,
            "childrenList": [{
                "chkDisabled": False,
                "level": 1,
                "hasChildren": True,
                "name": "外场区域",
                "parkSysType": 1,
                "checked": False,
                "id": 223,
                "nocheck": False,
                "type": 1,
                "childrenList": [{
                    "chkDisabled": False,
                    "parkName": "智泊云接口测试专用停车场",
                    "level": 2,
                    "hasChildren": False,
                    "parkSysType": 1,
                    "type": 2,
                    "parkId": 3751,
                    "parkUuid": "54a33015-d405-499e-bce2-e569cd9dce6a",
                    "areaId": 223,
                    "channelSeq": 2022,
                    "name": "智泊云接口测试入口",
                    "checked": False,
                    "nocheck": False,
                    "open": True,
                    "channelId": 2022
                },
                {
                    "chkDisabled": False,
                    "parkName": "智泊云接口测试专用停车场",
                    "level": 2,
                    "hasChildren": False,
                    "parkSysType": 1,
                    "type": 2,
                    "parkId": 3751,
                    "parkUuid": "54a33015-d405-499e-bce2-e569cd9dce6a",
                    "areaId": 223,
                    "channelSeq": 2023,
                    "name": "智泊云接口测试出口",
                    "checked": False,
                    "nocheck": False,
                    "open": True,
                    "channelId": 2023
                },
                {
                    "chkDisabled": False,
                    "parkName": "智泊云接口测试专用停车场",
                    "level": 2,
                    "hasChildren": False,
                    "parkSysType": 1,
                    "type": 2,
                    "parkId": 3751,
                    "parkUuid": "54a33015-d405-499e-bce2-e569cd9dce6a",
                    "areaId": 223,
                    "channelSeq": 2063,
                    "name": "智泊云接口测试入口-严进",
                    "checked": False,
                    "nocheck": False,
                    "open": True,
                    "channelId": 2063
                },
                {
                    "chkDisabled": False,
                    "parkName": "智泊云接口测试专用停车场",
                    "level": 2,
                    "hasChildren": False,
                    "parkSysType": 1,
                    "type": 2,
                    "parkId": 3751,
                    "parkUuid": "54a33015-d405-499e-bce2-e569cd9dce6a",
                    "areaId": 223,
                    "channelSeq": 2064,
                    "name": "智泊云接口测试出口-严出",
                    "checked": False,
                    "nocheck": False,
                    "open": True,
                    "channelId": 2064
                }],
                "open": True
            }],
            "open": True
        }
   CarType().__getDictChildList(aa, 'childrenList')
   print(Req().setValueByDict(CarType().aList,['checked'],'true'))