#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 16:00
# @Author  : 叶永彬
# @File    : information.py

from common.Req import Req
from common.superAction import SuperAction as SA
from Api.index_service.index import Index
import time,os
from urllib.parse import urlencode
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))

class Information(Req):
    """
    信息查询
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    form_headers = {"content-type": "application/x-www-form-urlencoded"}
    data = SA().get_today_data()

    def getPresentCar(self,parkName,carNum = ""):
        """
        获取在场车场
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(),'name',parkName)
        data = {
            "page":1,
            "rp":5,
            "approchTimeFrom":self.data +" 00:00:00",
            "approchTimeTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType":1,
            "plate":carNum
        }
        self.url = "/mgr/park/presentCar/getPresentCar.do?" + urlencode(data)
        re = self.get(self.api,headers= self.api_headers)
        return re.json()["data"]["rows"]

    def getCarLeaveHistory(self,parkName,carNum):
        """
        获取进出场记录
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":1,
            "fromLeaveTime":self.data + " 00:00:00",
            "toLeaveTime":self.data +" 23:59:59",
            "query_carNo":carNum,
            "parkIds":parkDict['value'],
            "parkSysType":1
        }
        self.url = "/mgr/park/carLeaveHistory/pageListParkingRecord.do?" + urlencode(data)
        time.sleep(5)
        re = self.get(self.api,headers= self.api_headers)
        return re.json()["data"]["rows"]

    def getParkingBillDetail(self,parkName,carNum):
        """
        获取收费记录
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        time.sleep(5)
        data = {
            "page":1,
            "rp":1,
            "query_payTimeFrom":self.data + " 00:00:00",
            "query_payTimeTo":self.data + " 23:59:59",
            "query_carCode":carNum,
            "parkIds":parkDict['value']
        }
        self.url = "/mgr/park/parkingBillDetail/list.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()['data']['rows']

    def getAdjustCarWaterNum(self,newCarCode,parkName):
        """
        获取校正流水
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "newCarCode":newCarCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value']
        }
        self.url = "/mgr/park/adjustCarRecord/getAdjustCarRecord.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()["data"]["rows"]


    def getAbnormalInCar(self, parkName, carCode):
        """
        获取异常进场记录
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType": 1
        }
        self.url = "mgr/park/abnormalInCar/getAbnormalInCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()['data']['rows']

    def getAbnormalPicCar(self, parkName, carCode):
        """
        获取异常拍照记录
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType": 1
        }
        self.url = "mgr/park/parkAbnormalPicCar/getParkAbnormalPicCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()['data']['rows']

    def __getParkingBaseTree(self):
        """获取当前用户车场树信息"""
        self.url = "/mgr/parkingBaseData/getParkingBaseDataTree.do"
        re = self.get(self.api,headers=self.api_headers)
        return re

    def getEmergencyCarRecord(self, parkName, carType, carNum):
        """查询指定车牌告警记录"""
        carTypeDict = {"指定车辆": 0, "黑名单": 4, "白名单": 8}
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "pageSize": 1,
            "carType": carTypeDict[carType],
            "carCode": carNum,
            "createTimeFrom": self.data + " 00:00:00",
            "createTimeTo": self.data +" 23:59:59",
            "parkIds": parkDict['value'],
            "parkSysType": 1,
        }
        self.url = "/mgr/park/emergency/record/list.do?" + urlencode(data)
        re = self.get(self.api, headers = self.api_headers)
        return re.json()

    def cleanCarCheckOut(self, parkName, carNum):
        """批量盘点"""
        carNumDict = self.getDictBykey(self.getPresentCar(parkName, carNum), 'carNo', carNum)
        userDict = Index(self.Session).getNewMeun().json()['user']
        data = {
            "topBillCodeList": carNumDict['topBillCode'],
            "operatorName": userDict['nickname'],
            "comment": 'pytest'
        }
        self.url = '/mgr/park/presentCar/clearByTopBillCodeList?' + urlencode(data)
        re = self.post(self.api, headers = self.api_headers)
        return re.json()

    def intelligenceCheckCarOut(self, parkName, cleanType = '按时间条件',carNum = None ):
        """
        智能盘点
        :param parkName:
        :param cleanType: '按时间条件','按在场车辆'
        :param file: 按上传模板
        :return:
        """
        nowTime = SA().get_time('%Y-%m-%d %H:%M:%S')
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        userDict = Index(self.Session).getNewMeun().json()['user']
        if cleanType == '按时间条件':
            re = self.__autoClearCarByTime(nowTime, parkDict['parkId'], userDict['nickname'])
        else:
            re = self.__autoClearCarByFile(nowTime, parkDict['parkId'], userDict['nickname'], carNum)
        return re.json()


    def __autoClearCarByTime(self, clearTime, parkUUID, operatorName):
        """智能盘点-按时间盘点方式"""
        data = {
            "clearTime": clearTime,
            "parkUUID": parkUUID,
            "comment": 'pytest智能盘点',
            "operatorName": operatorName
        }
        if self.__getPresentCarByTime(clearTime, parkUUID).json()['message'] == "OK":
            self.url = "/mgr/park/presentCar/clearByTime?" + urlencode(data)
            re = self.post(self.api, headers=self.api_headers)
            return re


    def __getPresentCarByTime(self, clearTime, parkUUID):
        """按时间获取在场车辆数量"""
        data = {
            "clearTime": clearTime,
            "parkUUID": parkUUID
        }
        self.url = "/mgr/park/presentCar/clearByTimeCheck?" + urlencode(data)
        re = self.post(self.api, headers=self.api_headers)
        return re

    def __autoClearCarCheck(self, clearTime, operatorName, parkUUID, file):
        """按模板获取在场车场信息记录"""
        files = {
            "autoClearFile": open(file, 'rb')
        }

        data = {
            "clearTime": clearTime,
            "operatorName": operatorName,
            "parkUUID": parkUUID
        }
        self.url = "/mgr/park/presentCar/autoClearCarCheck?" + urlencode(data)
        re = self.post(self.api, files=files, headers={'User-Agent':'Chrome/71.0.3578.98 Safari/537.36'})
        return re

    def __autoClearCarByFile(self,clearTime, parkUUID, operatorName, carNum, fileName = "智能盘点.xls"):
        """
        智能盘点-按在场车场，按模板盘点在场车场信息记录
        :param clearTime:
        :param parkUUID:
        :param operatorName:
        :param carNum: 可以输入多个车牌，用','隔开
        :param fileName:
        :return:
        """
        file = root_path + '/upload/' + str(fileName)
        Index(self.Session).downloadExcelTmp("auto_clear_car.xls", file)
        self.__setCarNumInClearCarFile(file, carNum)
        clearCarCheck = self.__autoClearCarCheck(clearTime, operatorName, parkUUID, file).json()
        data = {
            "clearCode":clearCarCheck['data']['clearCode'],
            "comment":'pytest智能盘点按模板',
            "additionRecord": 1,
            "operatorName":operatorName
        }
        self.url = "/mgr/park/presentCar/autoClearCar?" + urlencode(data)
        re = self.post(self.api, headers=self.api_headers)
        return re

    def __setCarNumInClearCarFile(self, file, presentCarNum):
        """往盘点车辆文件设置在场车牌"""
        import xlrd
        from xlutils.copy import copy
        old_excel = xlrd.open_workbook(file, formatting_info=True)
        new_excel = copy(old_excel)
        ws = new_excel.get_sheet(0)
        presentCarNum = presentCarNum.replace('，',',')
        if ',' in presentCarNum:
            carNum = presentCarNum.split(',')
            for index, v in enumerate(carNum):
                ws.write(2 + index, 0, v)
        else:
            ws.write(2, 0, presentCarNum)
        new_excel.save(file)

    def getSystemLog(self, menuLevel = None, operationObject = None):
        """查看系统日志"""
        data = {
            "page": 1,
            "rp": 1,
            "query_startTime": self.data + " 00:00:00",
            "query_endTime": self.data +" 23:59:59",
            "query_menuLevel": menuLevel,
            "query_operationObject": operationObject
        }
        self.url = "/mgr/pomplog/list.do"
        re = self.post(self.api, data = data, headers = self.form_headers)
        return re.json()['data']['rows']

if __name__ == '__main__':
    Information().runTest('E:/POMP_API/upload/auto_clear_car.xls','粤Q12344,粤B12344')
    # carNum =['1','2']
    # print(len(carNum))

