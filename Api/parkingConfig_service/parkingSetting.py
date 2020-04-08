#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 17:00
# @Author  : 叶永彬
# @File    : parkingSetting.py

from common.Req import Req
from Api.index_service.index import Index
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json"}

configName = {
        '满位限行':'openFullLimit',
        '模糊匹配':'openFuzzyMatch',
        '车牌强制转换':'carNoForceCovertFlag'
    }
openFlat = {
    '0': False,
    '1': True
}

class ParkingSetting(Req):
    """车场配置"""


    def updataOperatorParkCofigInfo(self,parkName,key,setValue):
        """
        修改车场配置
        :param jsonObject: 车场原来配置
        :param key: 需要修改的功能名(车牌强制转换，模糊匹配，...)
        :param setValue: 1（启用）,0（禁用）
        :return:
        """
        parkDict = self.getDictBykey(self.__getOperatorParkConfigListView().json(), 'parkName', parkName)
        OldParkConfigDict = self.getOperatorParkConfigInfo(parkName)

        parkConfigDict = self.__setValueByAllkey(OldParkConfigDict,"parkId",parkDict['parkId'])
        parkConfigDict = self.__setValueByAllkey(parkConfigDict, "parkCloudChargeCustomCarTypeVoList", [])
        updataParkConfigDict = self.__setValueByAllkey(parkConfigDict,configName[key],openFlat[str(setValue)])
        self.url = "/mgr/operatorPark/updateOperatorParkConfigInfo"
        data = updataParkConfigDict
        re = self.post(self.api, json = data, headers = json_headers)
        return re.json()

    def getOperatorParkConfigInfo(self,parkName):
        """获取车场配置信息"""
        parkDict = self.getDictBykey(self.__getOperatorParkConfigListView().json(), 'parkName', parkName)
        data = {
            "parkID":parkDict['parkId']
        }
        self.url = "/mgr/operatorPark/getOperatorParkConfigInfo?" + urlencode(data)
        re = self.get(self.api, headers = json_headers)
        return re.json()['data']

    def __getOperatorParkConfigListView(self):
        """获取当前用户车场列表"""
        re = Index(self.Session).getNewMeun()
        operatorID = re.json()["user"]["operatorID"]
        json_data = {
            "pageNumber":1,
            "pageSize":6,
            "sortType":"ASC"
        }
        data = {
            "operatorId": operatorID,
            "parkName":""
        }
        self.url = '/mgr/operatorPark/getOperatorParkConfigListView?' + urlencode(data)
        re = self.post(self.api,json = json_data, headers = json_headers)
        return re

    def __setValueByAllkey(self, json, key, setValue ):
        """修改传入json对象的全部key的value值"""
        jsonNew = json
        for i in jsonNew.keys():
            if i == key:
                if isinstance(jsonNew[i], dict):
                    jsonNew = jsonNew[i]
                else:
                    jsonNew[i] = setValue
            elif isinstance(jsonNew[i], dict):
                self.__setValueByAllkey(jsonNew[i], key, setValue)
            elif isinstance(jsonNew[i], list):
                for item in jsonNew[i]:
                    if isinstance(item, dict):
                        self.__setValueByAllkey(item, key, setValue)

        return json
