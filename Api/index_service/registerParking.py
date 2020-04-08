#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/3 11:03
# @Author  : 叶永彬
# @File    : registerParking.py
import os
from common.Req import Req
from urllib.parse import urlencode
from common.superAction import SuperAction as SA
json_headers = {"Content-Type": "application/json;charset=UTF-8"}
form_headers = {"content-type": "application/x-www-form-urlencoded"}
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))

class RegisterParking(Req):
    """注册车场"""
    def registerUser(self,activationCode,managerName,userAccount,pwd):
        """注册用户"""
        data = {
            "managerName": managerName,
            "userAccount": userAccount,
            "firstPwd": pwd,
            "confirmPwd": pwd,
            "activationCode": activationCode
        }
        re = self.__validateActivationCode(activationCode)
        if re.json()['message'] == '激活码正确':
            re = self.__validUser(userAccount)
            if re.text == 'true':
                self.url = "/mgr/normal/ajax/registerUser.do"
                re = self.post(self.api, data = data, headers = form_headers)
        return re.json()

    def __validateActivationCode(self, code):
        """验证激活码是否正确"""
        data = {
            "code": code
        }
        self.url = "/mgr/normal/ajax/validateActivationCode.do?" + urlencode(data)
        re = self.get(self.api)
        return re

    def __validUser(self,loginId):
        """验证用户是否已存在"""
        self.url = "/mgr/normal/ajax/validUser.do"
        data = {
            "loginId": loginId
        }
        re = self.post(self.api, data = data, headers = form_headers)
        return re

    def __checkValidateCode(self, activationCode):
        """查看key"""
        data = {"activationCode": activationCode}
        self.url = "/mgr/operatorPark/checkValidateCode?" + urlencode(data)
        re = self.get(self.api)
        return re

    def __isExistParkName(self,parkName):
        data = {
            "parkName": parkName
        }
        self.url = "/mgr/operatorPark/hasExistParkName?" + urlencode(data)
        re = self.get(self.api)
        return re

    def addOperatorPark(self, activationCode, parkName, picName = 'pic.jpg'):
        """增加停车场配置信息"""
        picPath = os.path.join(root_path, 'upload', picName)
        data = {
                "parkBaseInfo": {
                    "address": "佛山市南海区桂城街道万科广场",
                    "areaFullPath": "110000000.110100000.110101000",
                    "areaID": "110101000",
                    "areaName": "北京市-市辖区-东城区",
                    "chargePicChangeFlag": False,
                    "chargeRulePicStr": "{}".format(SA().getPicBase64(picPath)),
                    "chargeRulePicType": "jpeg",
                    "chargeRulePicUrl": "",
                    "customParkCode": "",
                    "flagTag": "",
                    "freeTime": "",
                    "fullPath": "",
                    "gpsX": "116.416443",
                    "gpsY": "39.927711",
                    "id": None,
                    "isTemplatePay": False,
                    "isTradecouponOnlinesettle": False,
                    "name": parkName,
                    "parkCode": "",
                    "parkType": 0,
                    "parkingSupervisor": SA.create_name(),
                    "parkingSupervisorPhone": 13800137999,
                    "partWay": 0,
                    "picChangeFlag": False,
                    "picPath": "",
                    "picStr": "{}".format(SA().getPicBase64(picPath)),
                    "picType": "jpeg",
                    "pkGlobalid": "",
                    "slotsNumber": 100,
                    "tempCarports": 10,
                    "timeoutLength": "10",
                    "parkSysType": 0,
                    "fixNumber": 90
                },
                "operatorInitInfo": {
                    "activationCode": activationCode,
                    "protocolKey": ""
                },
                "parkChargeBaseVoList": [{
                    "typeName": "计费组1",
                    "actionType": 0,
                    "carType": False,
                    "chargeTypeSeq": 0,
                    "isDefault": True,
                    "isFree": "收费车场",
                    "uiOpt": {
                        "isShow": True,
                        "carTypeOpt": [{
                            "name": "蓝牌车",
                            "value": 1,
                            "disabled": False
                        },
                        {
                            "name": "黄牌车",
                            "value": 2,
                            "disabled": False
                        },
                        {
                            "name": "新能源小车",
                            "value": 4,
                            "disabled": False
                        },
                        {
                            "name": "新能源大车",
                            "value": 3,
                            "disabled": False
                        },
                        {
                            "name": "不区分",
                            "value": 0,
                            "disabled": False
                        }]
                    },
                    "parkChargeStandardVoList": [{
                        "uiOpt": {
                            "splitTimeOpt": ["不分时段",
                            "分时段"],
                            "curSplitTime": "不分时段",
                            "splitTimeCount": 2,
                            "isMaxCharge": False,
                            "customIsMaxCharge": False,
                            "curTimeType": "分钟",
                            "isShowRuleDetail": True
                        },
                        "actionType": 0,
                        "carType": 0,
                        "chargeTypeSeq": 0,
                        "chargeUnit": "",
                        "cmxSettleType": 0,
                        "customMaxCharge": "",
                        "customMaxUnit": "",
                        "freeTime": 9,
                        "freeTimeAcc": False,
                        "loopType": 1,
                        "maxCharge": "",
                        "minCharge": 0,
                        "mxSettleType": 0,
                        "natureDay": 0,
                        "natureFreeTime": 0,
                        "parkChargeStandardPeriodVoList": [{
                            "uiOpt": {
                                "ruleTypeOpt": ["按次定额收费",
                                "按单价收费",
                                "递增收费"],
                                "curRuleType": "按次定额收费"
                            },
                            "maxCharge": 0,
                            "mxSettleType": 0,
                            "parkChargeStandardPeriodDetailVoList": [{
                                "chargeAmount": 5,
                                "chargeType": 3,
                                "chargeUnit": 1,
                                "periodDetailSeq": "",
                                "standardPeriodSeq": "",
                                "stepType": None
                            }],
                            "standardPeriodSeq": "",
                            "standardSeq": "",
                            "timeArray": ["00:00:00",
                            "23:59:59"]
                        }],
                        "remark": "",
                        "standardName": "默认规则",
                        "standardSeq": 0,
                        "startTime": "00:00:00",
                        "type": 0
                    }]
                }],
                "parkSpecialChargeVoList": [],
                "channelVoList": [{
                    "uiOpt": {
                        "isShow": False,
                        "curTab": "语音播报",
                        "tabData": ["语音播报",
                        "更多设置"],
                        "voiceOpenPeriod": ["00:00",
                        "23:59"],
                        "displayContentArray": [[{
                            "key": "%CN",
                            "text": "通道名称",
                            "previewText": ""
                        }],
                        [{
                            "key": "%T",
                            "text": "时间",
                            "previewText": ""
                        }],
                        [],
                        []],
                        "screenSettingType": "1"
                    },
                    "qrcodePicUrl": "",
                    "actionType": 0,
                    "areaID": 0,
                    "blacklistPassMode": 1,
                    "boxId": 0,
                    "boxStatus": 0,
                    "customCode": "",
                    "deviceNetModel": 0,
                    "deviceVolume": 50,
                    "displayContent": "{\"displayContentArray\":[[\"%CN\"],[\"%T\"],[],[]]}",
                    "displayViewModel": 0,
                    "dynamicVipToNormalMode": 2,
                    "enable": True,
                    "entranceName": "入口{}".format(SA().create_randomNum(val=2)),
                    "entranceType": 1,
                    "id": 0,
                    "isRootChannel": False,
                    "isSelfOpenGate": 0,
                    "localVipCarPassMode": 2,
                    "noChannelMode": 2,
                    "noPlatePassMode": 3,
                    "normalCarPassMode": 2,
                    "parkCode": "",
                    "parkGlobalID": "",
                    "parkName": "",
                    "qrCodeStr": "",
                    "qrCodeValue": "",
                    "redListPassMode": 2,
                    "settlementType": 0,
                    "shareListPassMode": 0,
                    "thirdPartyVipCarPassMode": 0,
                    "timeArray": ["00:00",
                    "23:59"],
                    "vipNotInPassMode": 2,
                    "visitorListPassMode": 1,
                    "voiceOpenPeriod": "00:00-23:59",
                    "ytjSeq": 0,
                    "ytjStatus": 0
                },
                {
                    "uiOpt": {
                        "isShow": False,
                        "curTab": "语音播报",
                        "tabData": ["语音播报",
                        "更多设置"],
                        "voiceOpenPeriod": ["00:00",
                        "23:59"],
                        "displayContentArray": [[{
                            "key": "%CN",
                            "text": "通道名称",
                            "previewText": ""
                        }],
                        [{
                            "key": "%T",
                            "text": "时间",
                            "previewText": ""
                        }],
                        [],
                        []],
                        "screenSettingType": "1"
                    },
                    "qrcodePicUrl": "",
                    "actionType": 0,
                    "areaID": 0,
                    "blacklistPassMode": 1,
                    "boxId": 0,
                    "boxStatus": 0,
                    "customCode": "",
                    "deviceNetModel": 0,
                    "deviceVolume": 50,
                    "displayContent": "{\"displayContentArray\":[[\"%CN\"],[\"%T\"],[],[]]}",
                    "displayViewModel": 0,
                    "dynamicVipToNormalMode": 2,
                    "enable": True,
                    "entranceName": "出口{}".format(SA().create_randomNum(val=2)),
                    "entranceType": 2,
                    "id": 0,
                    "isRootChannel": False,
                    "isSelfOpenGate": 0,
                    "localVipCarPassMode": 2,
                    "noChannelMode": 2,
                    "noPlatePassMode": 3,
                    "normalCarPassMode": 2,
                    "parkCode": "",
                    "parkGlobalID": "",
                    "parkName": "",
                    "qrCodeStr": "",
                    "qrCodeValue": "",
                    "redListPassMode": 2,
                    "settlementType": 0,
                    "shareListPassMode": 0,
                    "thirdPartyVipCarPassMode": 0,
                    "timeArray": ["00:00",
                    "23:59"],
                    "vipNotInPassMode": 2,
                    "visitorListPassMode": 1,
                    "voiceOpenPeriod": "00:00-23:59",
                    "ytjSeq": 0,
                    "ytjStatus": 0
                }],
                "parkCloudDetailVo": {
                    "defaultProvince": "京"
                }
            }
        re = self.__isExistParkName(parkName)
        if re.json()['status'] == 1:
            re = self.__checkValidateCode(activationCode)
            if re.json()['status'] == 1:
                self.url = "/mgr/operatorPark/addOperatorPark"
                re = self.post(self.api, json=data, headers= json_headers)
        return re.json()


