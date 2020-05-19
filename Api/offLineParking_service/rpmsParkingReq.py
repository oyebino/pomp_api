#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 16:07
# @Author  : 叶永彬
# @File    : rpmsParkingReq.py
from common.superAction import SuperAction as SA
from common.Req import Req
from urllib.parse import urlencode
from bs4 import BeautifulSoup

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json"}

class RpmsParkingReq(Req):
    """路边车场业务"""
    def __updateDiciStatus(self, parkingState, cmcId, pmdId):
        """
        上报地磁状态
        :param parkingState: 无车or有车
        :param cmcId: 控制器编号
        :param pmdId: 地磁编号
        :return:
        """
        parkingStateDict = {"无车":0, "有车":1}
        obj = SA().execjs("encrypt.js","encrypt",parkingStateDict.get(parkingState),cmcId,pmdId)
        data = {
            "parkingState": parkingStateDict.get(parkingState),
            "cmcId": cmcId,
            "pmdId": pmdId,
            "key": obj.get("account"),
            "timestamp": obj.get("timestamp"),
            "sign": obj.get("sign"),
            "data": obj.get("data")
        }
        self.url = "/parking/dici/status/update.do"
        re = self.post(self.roadSide_api, data=data, headers = form_headers)
        return re

    def carIn(self, parkCode, rmpsParkName, carNum,):
        """
        车辆进场
        :param parkCode: 车场编码
        :param position: 停车位编号
        :param carNum:  车牌
        :return:
        """
        parkPortDict = self.__listDeviceWaitSureList(rmpsParkName ,'无车')
        re = self.__updateDiciStatus("有车",parkPortDict.get("控制器编号"),parkPortDict.get("地磁编号"))
        data = {
            "parkCode": parkCode,
            "position": parkPortDict.get("停车位"),
            "carNo": carNum
        }
        self.url = "/parking/test/carIn.do"
        if re.json().get("code") == 1:
            re = self.post(self.roadSide_api, data=data, headers=form_headers)
        return re.json()

    def carOut(self,parkCode,rmpsParkName, carNum):
        """车辆离场"""
        carPositionName = self.getDashboardParkingslotStatus(rmpsParkName,carNum)
        parkPortDict = self.__listDeviceWaitSureList(rmpsParkName, '有车',carPositionName)
        re = self.__updateDiciStatus("无车", parkPortDict.get("控制器编号"), parkPortDict.get("地磁编号"))
        data = {
            "parkCode": parkCode,
            "position": carPositionName,
            "carNo": carNum
        }
        self.url = "/parking/test/carOut.do?" + urlencode(data)
        if re.json().get("code") == 1:
            re = self.post(self.roadSide_api)
        return re.json()

    def __userParkTreeList(self):
        """用户车场列表"""
        data = {
            "showCheckBox": False,
            "_": SA.getTimeStamp()
        }
        self.url = "/parking/carrier/tree/park/user/list.do?" + urlencode(data)
        re = self.get(self.roadSide_api)
        return re.json()


    def __listByParkId(self,parkName):
        """车场车位管理"""
        parkDict = self.getDictBykey(self.__userParkTreeList(),'name',parkName)
        data = {
            "parkId":parkDict.get("id"),
            "pageNow": 1,
            "pageSize": 50
        }
        self.url = "/parking/carrier/carPosition/listByParkId.do"
        re = self.post(self.roadSide_api, data = data, headers = form_headers)
        return re.json()

    def __listDeviceWaitSureList(self, parkName, statusStr, carPositionName = ""):
        """车位地磁绑定"""
        positionList =  self.__listByParkId(parkName).get('dataList')
        if statusStr == "无车":
            diciCode = self.__checkAvailableDiciCode(parkName, positionList, statusStr)
        else:
            diciCode = ""
        data = {
            "diciCode":diciCode,
            "carPositionName":carPositionName,
            "dqrtype":1,
            "pageNow":1,
            "pageSize":50
        }
        self.url = "/parking/carrier/device/listDeviceWaitSureList.do"
        re = self.post(self.roadSide_api, data = data, headers = form_headers)
        return self.__packDiciDict(re.text)

    def __packDiciDict(self, html):
        """"整合车位地磁对象"""
        pm = dict()
        th_list = []
        soup = BeautifulSoup(html, 'lxml')
        for th in soup.find_all(name='th'):
            th_list.append(str(th.string).strip())
        for i,li in enumerate(soup.find_all(name='td')):
            pm[th_list[i]] = str(li.string).strip()
        return pm

    def __checkAvailableDiciCode(self,parkName, positionList, statusStr):
        """查找可用地磁,返回 地磁编号"""
        diciCode = None
        for i in positionList:
            if i.get("diciName") != "" and i.get("statusStr") == statusStr:
                return i.get("diciName")
        if diciCode == None:
            raise ValueError("【{}】路边车场无可用地磁！".format(parkName))

    def getDashboardParkingslotStatus(self, parkName, carNum):
        """获取车位车位实时状态,返回当前车辆的车位号"""
        parkDict = self.getDictBykey(self.__userParkTreeList(), 'name', parkName)
        data = {
            "page":"parkingslotstatus",
            "pId": parkDict.get("id"),
            "pageNow": "0",
            "pageSize": "24",
        }
        self.url = "/parking/carrier/getDashboardParkingslotStatus.do?"
        re = self.post(self.roadSide_api, data = data, headers=form_headers)
        for th in BeautifulSoup(re.text, 'lxml').find_all(name='li', attrs={"class": "d_car"}):
            if carNum in th.text:
                span = th.find(name='span', attrs={"class": "space font_01"})
                return span.text
        return re.text




