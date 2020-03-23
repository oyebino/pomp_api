#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 13:58
# @Author  : 叶永彬
# @File    : monthTicketConfig.py

from common.Req import Req
from common import const
from common.superAction import SuperAction as SA
from Api.index_service.index import Index
from urllib.parse import urlencode
import json

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class MonthTicketConfig(Req):
    """月票类型"""
    aList = []
    def createMonthTicketConfig(self,parkName, ticketTypeName,renewMethod,validTo):
        """
        创建月票类型
        :param parkName:
        :param ticketName:
        :param renewMethod: '自然月','自定义'
        :param validTo: '2020-5-19'
        :return:
        """
        renewMethodDict = {
            "自然月": "NATURAL_MONTH",
            "自定义": "CUSTOM"
        }
        parkInfoDict = self.getDictBykey(Index(self.Session).getUnsignedParkList().json(), 'name', parkName)
        optionArrList = self.__selectChargeGroupList(parkInfoDict['parkUUID']).json()['data'][parkInfoDict['parkUUID']]
        parkJson = [{
            "parkSysType": 1,
            "parkVipTypeId": "",
            "parkId": parkInfoDict['id'],
            "parkUuid": parkInfoDict['parkUUID'],
            "parkName": parkName,
            "chargeGroupCode": "0",
            "optionArr": optionArrList
        }]

        channelAuthTree = self.getDictBykey(self.__getChannelAuthTreeMultiPark().json(), 'name', parkName)
        self.__getDictChildList(channelAuthTree, 'childrenList')
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
            "ticketName": ticketTypeName,
            "ticketType": 'OUTTER',
            "renew": 1,
            "price": 35,
            "renewMethod": renewMethodDict[renewMethod],
            "maxSellLimit": 'NO',
            "financialParkId": parkInfoDict['id'],
            "parkJson": str(parkJson),
            "remark": 'pytest',
            "renewFormerDays": 60, # 允许向前续费天数
            "inviteCarTotal": 0,
            "continueBuyFlag":1,
            "supportVirtualCarcode": 0,
            "parkVipTypeJson": str(parkVipTypeJson),
            "inviteCarSwitcher": 0,
            "validTo": "{} 23:59:59".format(validTo),
            "sellFrom": SA().get_time(strType='%Y-%m-%d %H:%M:%S'),
            "sellTo": SA().get_time(strType='%Y-%m-%d %H:%M:%S'),
            "showMessage": const.showMessage
        }
        self.url = "/mgr/monthTicketConfig/save.do"
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def editMonthTicketConfig(self, parkName, oldTypeName, newTypeName):
        """
        修改月票类型-
        条件sellNum > 0强制编辑，等于0，编辑，
        parkSysType==0 并且 ticketStatus==='VALID'是不可以编辑和强制编辑
        :param parkName:
        :param oldTypeName:
        :param newTypeName:
        :return:
        """
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        typeConfigDict = self.getDictBykey(self.getMonthTicketList(parkName,oldTypeName).json(), 'ticketName', oldTypeName)
        typeConfigDetailDict = self.__getMonthTicketCofigDetail(typeConfigDict['id']).json()['data']
        optionArrList = self.__selectChargeGroupList(parkDict['parkId']).json()['data'][parkDict['parkId']]
        optionArrDict = {'optionArr': optionArrList}
        parkJsonList = []
        configDict = typeConfigDetailDict['parkList'][0]
        configDict.update(optionArrDict)
        parkJsonList.append(configDict)

        channelAuthTree = typeConfigDetailDict['channelArr']
        parkVipTypeDict = typeConfigDetailDict['parkVipType']

        parkVipTypeJson = {
            "id": parkVipTypeDict['id'],
            "customVipName": parkVipTypeDict['customVipName'],
            "settlementType": parkVipTypeDict['settlementType'],
            "settlementAmount": parkVipTypeDict['settlementAmount'],
            "isDynamicMode": parkVipTypeDict['isDynamicMode'],
            "dynamicCarportNumber": parkVipTypeDict['dynamicCarportNumber'],
            "isDatePrivilege": parkVipTypeDict['isDatePrivilege'],
            "isTimePrivilege": parkVipTypeDict['isTimePrivilege'],
            "privilegeTimePeriod": parkVipTypeDict['privilegeTimePeriod'],
            "isChargeGroupRelated": parkVipTypeDict['isChargeGroupRelated'],
            "chargeGroupCode": parkVipTypeDict['chargeGroupCode'],
            "vipGroupType": parkVipTypeDict['vipGroupType'],
            "dynamicFullLimit": parkVipTypeDict['dynamicFullLimit'],
            "dynamicCarNumber": parkVipTypeDict['dynamicCarNumber'],
            "vipNearExpiredDayThreshold": parkVipTypeDict['vipNearExpiredDayThreshold'],
            "vipDeleteExpiredDayThreshold": parkVipTypeDict['vipDeleteExpiredDayThreshold'],
            "openVipFullLimit":parkVipTypeDict['openVipFullLimit'],
            "vipFullLimitValue": parkVipTypeDict['vipFullLimitValue'],
            "vipFullOpenModel": parkVipTypeDict['vipFullOpenModel'],
            "vipRecoverTime": parkVipTypeDict['vipRecoverTime'],
            "priDateArrStr": parkVipTypeDict['priDateArrStr'],
            "parkId": parkVipTypeDict['parkId'],
            "parkName": parkVipTypeDict['parkName'],
            "channelAuthTree": channelAuthTree,
            "channelSeqList":parkVipTypeDict['channelSeqList'],
            "autoSwitchVip":parkVipTypeDict['autoSwitchVip'],
            "offLine":parkVipTypeDict['offLine']
        }
        data = {
            "id":typeConfigDetailDict['id'],
            "parkSysType": typeConfigDetailDict['parkSysType'],
            "price": typeConfigDetailDict['price'],
            "ticketName": newTypeName,
            "ticketType": typeConfigDetailDict['ticketType'],
            "renewMethod": typeConfigDetailDict['renewMethod'],
            "maxSellLimit": typeConfigDetailDict['maxSellLimit'],
            "maxSellNum": typeConfigDetailDict['maxSellNum'],
            "sellNum": typeConfigDetailDict['sellNum'],
            "remark": typeConfigDetailDict['remark'],
            "renewFormerDays": typeConfigDetailDict['renewFormerDays'],
            "renew": typeConfigDetailDict['renew'],
            "inviteCarTotal": typeConfigDetailDict['inviteCarTotal'],
            "financialParkId": typeConfigDetailDict['financialParkId'],
            "continueBuyFlag": 1,
            "supportVirtualCarcode": typeConfigDetailDict['supportVirtualCarcode'],
            "validTo": SA().timestamp_to_format(typeConfigDetailDict['validTo']),
            "parkJson": json.dumps(parkJsonList),
            "sellFrom": SA().timestamp_to_format(typeConfigDetailDict['sellFrom']),
            "sellTo": '4020-03-19 00:00:00',
            "parkVipTypeJson": json.dumps(parkVipTypeJson),
            "inviteCarSwitcher": 0,
            "showMessage":typeConfigDetailDict['showMessage']
        }
        if typeConfigDetailDict['sellNum'] == 0:
            self.url = "/mgr/monthTicketConfig/save.do"
        else:
            self.url = "/mgr/monthTicketConfig/forceSave.do"
        re = self.post(self.api, data=data, headers= form_headers)
        return re



    def __selectChargeGroupList(self, parkUUID):
        """列出计费组"""
        data = {
            "parkIdList": parkUUID
        }
        self.url = "/mgr/monthTicketConfig/selectChargeGroupList2.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
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

    def __getDictChildList(self, json, key):
        """查找json的key把对应的value对象递归存放在list"""
        self.aList.append(json)
        for item in json:
            if item == key:
                if isinstance(json[key], list):
                    for i in json[key]:
                        self.__getDictChildList(i, key)

    def getMonthTicketList(self, parkName, typeName =""):
        """获取月票类型列表"""
        if typeName != "":
            allTypeName = self.__findConfigNameList().json()['data']
            if typeName in allTypeName:
                return self.__getMonthTicketListChoose(parkName, typeName)
            else:
                print("【"+ typeName +"】不存在列表里")
        else:
            return self.__getMonthTicketListChoose(parkName, typeName)

    def __getMonthTicketListChoose(self, parkName, typeName):
        """"选择性获取月票类型"""
        parkInfoDict = self.getDictBykey(Index(self.Session).getUnsignedParkList().json(), 'name', parkName)
        data = {
            "page": 1,
            "rp": 20,
            "query_parkId": parkInfoDict['id'],
            "parkSysType": 1,
            "query_ticketName": typeName
        }
        self.url = "/mgr/monthTicketConfig/list.do?" + urlencode(data)
        re = self.get(self.api, headers=form_headers)
        return re

    def __findConfigNameList(self):
        """列出全部月票类型名称"""
        self.url = "/mgr/commonFun/monthticket/findConfigNameList.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def __getMonthTicketCofigDetail(self, monthTicketConfigId):
        """月票类型详情"""
        data = {
            "monthTicketConfigId": monthTicketConfigId
        }
        self.url = "/mgr/monthTicketBill/configDetail.do?" + urlencode(data)
        re = self.get(self.api)
        return re

    def updateStatusMonthTicketConfig(self, parkName, ticketConfigName, monthTicketStatus):
        """月票类型上架与下架"""
        statusDict = {
            "上架": 'VALID',
            "下架": 'INVALID'
        }
        ticketConfigDict = self.getDictBykey(self.getMonthTicketList(parkName, ticketConfigName).json(),'ticketName',ticketConfigName)
        self.url = "/mgr/monthTicketConfig/updateStatus.do"
        data = {
            "monthTicketConfigId":ticketConfigDict['id'],
            "monthTicketStatus":statusDict[monthTicketStatus]
        }
        re = self.post(self.api, data=data, headers= form_headers)
        return re

    def delMonthTicketConfig(self, parkName, ticketConfigName):
        """删除月票类型"""
        ticketConfigDict = self.getDictBykey(self.getMonthTicketList(parkName, ticketConfigName).json(), 'ticketName',ticketConfigName)
        self.url = "/mgr/monthTicketConfig/del.do"
        data = {
            "monthTicketConfigId": ticketConfigDict['id']
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

