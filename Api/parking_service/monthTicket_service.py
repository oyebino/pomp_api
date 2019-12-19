#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 11:05
# @Author  : 叶永彬
# @File    : monthTicket_service.py

from common import const
from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from Config.Config import Config

class monthTicket_controller(Req):
    """
    月票管理
    """
    api_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def save_monthTicketType(self):
        self.url = "/mgr/monthTicketConfig/save.do"
        json_data1 = {
            "ticketName": "接1口测试api",
            "ticketType": "OUTTER",
            "renew": 1,
            "price":10,
            "renewMethod":"NATURAL_MONTH",
            "maxSellLimit":"NO",
            "financialParkId":3751,
            "parkJson":const.parkJson,
            "renewFormerDays":0,
            "inviteCarTotal":1,
            "continueBuyFlag":1,
            "supportVirtualCarcode":0,
            "parkVipTypeJson":const.parkVipTypeJson,
            "inviteCarSwitcher":0,
            "validTo":"2020-01-31 23:59:59",
            "sellFrom":"2019-12-17 11:12:06",
            "sellTo":"2019-12-17 11:12:06",
            "showMessage":const.showMessage
        }
        json_data = {
            "id": None,
            "parkSysType": None,
            "ticketName": "apitest11",
            "ticketType": "OUTTER",
            "renew": 1,
            "price": 10,
            "renewMethod": "NATURAL_MONTH",
            "maxSellLimit": "NO",
            "maxSellNum": None,
            "sellNum": None,
            "financialParkId": 3751,
            "parkJson": str([{"parkVipTypeId":"","parkId":77,"parkUuid":"d7faf2a0-d05d-4c7e-8b84-3c41831f7f5e","parkName":"开发测试停车场","optionArr":[],"parkSysType":0}]),
            "remark": "ddd",
            "renewFormerDays": 0,
            "inviteCarTotal": 0,
            "certifiRuleId": None,
            "continueBuyFlag": 1,
            "supportVirtualCarcode": 0,
            "ticketDesc": None,
            "sellingPic": None,
            "selloutPic": None,
            "sellingPicName": None,
            "selloutPicName": None,
            "parkVipTypeJson": str({'id':None,'customVipName':'','settlementType':0,'settlementAmount':None,'isDynamicMode':0,'dynamicCarportNumber':None,'isDatePrivilege':0,'isTimePrivilege':0,'privilegeTimePeriod':'','isChargeGroupRelated':0,'chargeGroupCode':None,'vipGroupType':0,'dynamicFullLimit':0,'dynamicCarNumber':None,'vipNearExpiredDayThreshold':'10','vipDeleteExpiredDayThreshold':0,'openVipFullLimit':0,'vipFullLimitValue':0,'vipFullOpenModel':0,'vipRecoverTime':None,'priTimeArrFrom':'','priTimeArrTo':'','priDateArrStr':'','parkId':'','parkName':'','channelAuthTree':'[{\'chkDisabled\':false,\'parkName\':\'开发测试停车场\',\'level\':2,\'hasChildren\':false,\'parkSysType\':0,\'type\':2,\'parkId\':77,\'parkUuid\':\'d7faf2a0-d05d-4c7e-8b84-3c41831f7f5e\',\'channelSeq\':30,\'name\':\'进口\',\'checked\':true,\'nocheck\':false,\'open\':false,\'isHidden\':false,\'isFirstNode\':true,\'tId\':\'ParkTree_24\',\'parentTId\':\'ParkTree_23\',\'isParent\':false,\'zAsync\':true,\'isLastNode\':false,\'isAjaxing\':false,\'pId\':32,\'checkedOld\':false,\'halfCheck\':false,\'check_Child_State\':-1,\'check_Focus\':false,\'isHover\':false,\'editNameFlag\':false},{\'chkDisabled\':false,\'parkName\':\'开发测试停车场\',\'level\':2,\'hasChildren\':false,\'parkSysType\':0,\'type\':2,\'parkId\':77,\'parkUuid\':\'d7faf2a0-d05d-4c7e-8b84-3c41831f7f5e\',\'channelSeq\':31,\'name\':\'出口\',\'checked\':true,\'nocheck\':false,\'open\':false,\'isHidden\':false,\'isLastNode\':true,\'tId\':\'ParkTree_25\',\'parentTId\':\'ParkTree_23\',\'isParent\':false,\'zAsync\':true,\'isFirstNode\':false,\'isAjaxing\':false,\'pId\':32,\'checkedOld\':false,\'halfCheck\':false,\'check_Child_State\':-1,\'check_Focus\':false,\'isHover\':false,\'editNameFlag\':false}]','channelSeqList':[],'autoSwitchVip':0,'offLine':1}),
            "inviteCarSwitcher": 0,
            "validTo": "2020-01-31 23:59:59",
            "sellFrom": "2019-12-19 10:36:06",
            "sellTo": "2019-12-19 10:36:06",
            "showMessage": str({"validInWarnOut":{"carIn":{"easy":{"id":None,"text":"%P\\%VM","voice":"%P%VM"},"hard":{"id":None,"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}},"carOut":{"easy":{"id":None,"text":"%P\\%VM","voice":"%P%VM"},"hard":{"id":None,"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}}},"validInWarnIn":{"carIn":{"easy":{"id":None,"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"id":None,"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}},"carOut":{"easy":{"id":None,"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"id":None,"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}}},"validOutDelIn":{"carIn":{"easy":{"id":None,"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"id":None,"text":"%P\\%VM已过期","voice":"%P%VM已过期"}},"carOutPay":{"easy":{"id":None,"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"},"hard":{"id":None,"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"}},"carOutNoPay":{"easy":{"id":None,"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"id":None,"text":"%P\\%VM已过期","voice":"%P%VM已过期"}}}}),
            "continueDiscountJson": None
            }
        re = self.post(self.api, data=json_data,headers=self.api_headers)
        return re


    def create_monthTicket(self):
        pass

if __name__ == "__main__":
    re =monthTicket_controller().save_monthTicketType()
    print(re.json())