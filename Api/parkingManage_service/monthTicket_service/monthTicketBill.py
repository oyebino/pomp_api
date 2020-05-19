#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 11:05
# @Author  : 叶永彬
# @File    : monthTicketBill.py

from common.Req import Req
from common.superAction import SuperAction as SA
from Api.index_service.index import Index
from urllib.parse import urlencode
from common.excelUnitl import ExcelUnitl
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../../.."))

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class MonthTicketBill(Req):
    """
    月票管理
    """
    def openMonthTicketBill(self, carNum, ticketName, timeperiodListStr):
        """
        开通月票
        :param carNum:
        :param ticketName:
        :param timeperiodListStr: ‘2020-02-01 00:00:00 - 2020-02-29 23:59:59’
        :return:
        """
        if ',' in carNum:
            carNumList = carNum.split(',')
        else:
            carNumList = list()
            carNumList.append(carNum)
        ticketNameDict = self.getDictBykey(self.getValidCofigList(), 'ticketName', ticketName)
        if ticketNameDict['renewMethod'] == 'NATURAL_MONTH':
            openMonthNum = self.__getMonthCount(timeperiodListStr)
        elif ticketNameDict['renewMethod'] == 'CUSTOM':
            openMonthNum = self.__getDayCount(timeperiodListStr)
        price = self.__operationPrice(ticketNameDict['price'])

        json_data = {
            "monthTicketId": ticketNameDict['id'],
            "monthTicketName": ticketNameDict['ticketName'],
            "timeperiodListStr": timeperiodListStr,
            "userName": "pytest",
            "userPhone": "135{}".format(SA().create_randomNum(val=8)),
            "price": price,
            "totalValue": int(float(price) * openMonthNum * len(carNumList)),
            "openMonthNum": openMonthNum,
            "realValue": 10,
            "inviteCarTotal": len(carNumList),
            "dynamicCarportNumber": 1,
            "carCode": carNumList,
        }
        self.url = "mgr/monthTicketBill/open.do"
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re.json()

    def __getDayCount(self, str):
        """计算时间段的天数"""
        import time
        s1 = str.split(' - ')
        start = time.mktime(time.strptime(s1[0], '%Y-%m-%d %H:%M:%S'))
        end = time.mktime(time.strptime(s1[1], '%Y-%m-%d %H:%M:%S'))
        count_days = int((end - start) / (24 * 60 * 60))
        return count_days + 1

    def __getMonthCount(self, str):
        """计算时间段的月份个数"""
        from datetime import datetime
        s1 = str.split(' - ')
        end_date = s1[1]
        start_date = s1[0]
        year_end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').year
        month_end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').month
        year_start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').year
        month_start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').month
        interval = (year_end - year_start) * 12 + (month_end - month_start)
        return interval + 1


    def __operationPrice(self, price):
        """浮点数精度计算-针对月票单价/30=计算天数价格"""
        result = int(float(price) / 30 * 100) / 100 + 0.01
        return '{:.2f}'.format(result)

    def getMonthTicketBillList(self, parkName, carNum = "", combinedStatus=""):
        """
        获取已开通月票记录列表
        :param parkName:
        :param carNum:
        :param combinedStatus: 状态‘不在有效期，生效中，已退款’
        :return:
        """
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        statusDict = {
            "不在有效期":0,
            "生效中":1,
            "已退款":2,
            "":""
        }
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkDict['value'],
            "parkSysType":parkDict['parkSysType'],
            "query_carCode":carNum,
            "combinedStatus":statusDict[combinedStatus]
        }
        self.url = "/mgr/monthTicketBill/list.do?" + urlencode(data)
        re = self.get(self.api, headers=form_headers)
        return re.json()

    def editOpenMonthTicketBill(self, parkName, carNum, editUser, status = '生效中'):
        """
        修改已开通月票
        :param parkName:
        :param carNum:
        :param editUser: 修改车主名
        :return:
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, status), 'carCode',carNum)
        isDynamicMode = self.__checkMonthTicketBillIsDynamicMode(monthTicketBillDict['id']).json()['data']['isDynamicMode']

        data = {
            "id":monthTicketBillDict['id'],
            "monthTicketId": monthTicketBillDict['monthTicketId'],
            "monthTicketName": monthTicketBillDict['ticketName'],
            "userName": editUser,
            "userPhone": monthTicketBillDict['userPhone'],
            "carCode": monthTicketBillDict['carCode'],
            "remark1":monthTicketBillDict['remark1'],
            "dynamicCarportNumber":monthTicketBillDict['dynamicCarportNumber'],
            "isDynamicMode": isDynamicMode,
            "supportVirtualCarcode":monthTicketBillDict['supportVirtualCarcode']
        }
        if self.__preeditMonthTicketBill(data).json()['status'] == 1:
            self.url = "/mgr/monthTicketBill/editMonthTicketBill.do"
            re =self.post(self.api, data = data, headers = form_headers)
            return re.json()

    def __preeditMonthTicketBill(self, data):
        """预编辑"""
        self.url = "/mgr/monthTicketBill/preeditMonthTicketBill.do"
        re = self.post(self.api, data= data, headers = form_headers)
        return re

    def __checkMonthTicketBillIsDynamicMode(self, id):
        """查看月票记录详情"""
        data = {
            "id":id
        }
        self.url = "/mgr/monthTicketBill/checkMonthTicketBillIsDynamicMode.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def __findConfigNameList(self):
        """获取全部月票名"""
        self.url = "/mgr/commonFun/monthticket/findConfigNameList.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def getValidCofigList(self):
        """获取月票类型list"""
        self.url = "/mgr/monthTicketBill/validConfigList.do"
        re = self.get(self.api, headers = form_headers)
        return re.json()

    def renewMonthTicketBill(self, parkName, carNum, status , date = None):
        """
        月票续费，默认续费10天
        :param parkName:
        :param carNum:
        :param refundValue: 续费折扣价格
        :param status: 月票有效状态：
        :paramdate 续费的时间点，'2020-02-02'
        :return:
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, status), 'carCode', carNum)
        self.url = "/mgr/monthTicketBill/renew.do"
        if monthTicketBillDict['renewMethod'] == 'NATURAL_MONTH':
            openMonthNum = 2
            timeperiodListStr = SA().cal_getTheMonth(date = date, n = openMonthNum - 1)
        else:
            openMonthNum = 10
            if date == None:
                date = SA().get_today_data()
            else:
                if not isinstance(date, str):
                    # dateType = datetime.datetime.strptime(date, '%Y-%m-%d')
                    date = date.strftime("%Y-%m-%d")
            timeperiodListStr = date + " 00:00:00 - " + SA().cal_get_day(strType='%Y-%m-%d', days=int(openMonthNum), date=date) + " 23:59:59"
        price = self.__operationPrice(monthTicketBillDict['price'])
        data = {
            "monthTicketId": monthTicketBillDict['monthTicketId'],
            "monthTicketName": monthTicketBillDict['ticketName'],
            "monthTicketBillId": monthTicketBillDict['id'],
            "timeperiodListStr": timeperiodListStr,
            "userName": monthTicketBillDict['userName'],
            "userPhone": monthTicketBillDict['userPhone'],
            "price": price,
            "totalValue": monthTicketBillDict['totalValue'],
            "openMonthNum": openMonthNum,
            "realValue": 19,
            "remark1": 'pytest续费',
            "dynamicCarportNumber": monthTicketBillDict['dynamicCarportNumber'],
        }
        re = self.post(self.api, data= data, headers = form_headers)
        return re.json()


    def refundMonthTicketBill(self, parkName, carNum, refundValue):
        """
        月票退款
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '生效中'), 'carCode', carNum)
        realValue = (monthTicketBillDict['totalValue'] - monthTicketBillDict['reliefValue']) * 100
        json_data = {
        "monthTicketBillId": monthTicketBillDict['id'],
        "refundValue": refundValue,
        "remark": "pytest接口退款",
        "realValue": realValue
        }
        if realValue < refundValue * 100:
            print("退款金额不能大于实付金额")
        else:
            self.url = "mgr/monthTicketBill/refund.do"
            re = self.post(self.api, data=json_data, headers=form_headers)
            return re.json()

    def getListBillUpdateRecord(self, parkName, carNum):
        """查看月票日志"""
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '生效中'), 'carCode',carNum)
        data = {
            "monthTicketBillId": monthTicketBillDict['id'],
            "page":1,
            "rp":1
        }
        self.url = '/mgr/monthTicketBill/listBillUpdateRecord?' + urlencode(data)
        re =self.get(self.api, headers = form_headers)
        return re.json()

    def batchOpenMonthTicketBill(self,parkName, typeName, carNum, fileName = '批量开通月票.xls'):
        """批量开通月票"""
        file = root_path + '/upload/' + fileName
        Index(self.Session).downloadExcelTmp("month_ticket_bill.xls", file)
        ticketConfigDict = self.getDictBykey(MonthTicketConfig(self.Session).getMonthTicketList(parkName,typeName),'ticketName',typeName)
        self.__editOpenBillFile(file, ticketConfigDict['ticketCode'], carNum)
        file = {
            "importFile": open(file, 'rb'),
            "im12portFile": "self.importFile.importFile"
        }
        self.url = "/mgr/monthTicketBill/importBills.do"
        re = self.post(self.api, files = file, headers = {'User-Agent':'Chrome/71.0.3578.98'})
        if re.json()['status'] == 1:
            re = self.__getImportBillResut()
        return re.json()['data']

    def __getImportBillResut(self):
        """获取导入结果"""
        self.url = "/mgr/monthTicketBill/getImportBillResult.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def __editOpenBillFile(self,file,ticketCode,carNum):
        """修改批量开通月票excel文件"""
        excel = ExcelUnitl(file)
        excel.editCell(1, 0, ticketCode)
        excel.editCell(1, 1, SA.create_name())
        excel.editCell(1, 2, "135{}".format(SA().create_randomNum(val=8)))
        excel.editCell(1, 3, carNum)
        excel.editCell(1, 4, "{} 00:00:00".format(SA().get_today_data()))
        excel.editCell(1, 5, "{} 23:59:59".format(SA().cal_get_day(strType ="%Y-%m-%d", days=15)))
        excel.editCell(1, 7, 30)

    def batchRefundMonthTicketBill(self, parkName, carNum, fileName = '批量退费月票.xls'):
        """批量退费月票"""
        file = root_path + '/upload/' + fileName
        Index(self.Session).downloadExcelTmp("refund_month_ticket_bill.xls", file)
        billDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '生效中'), 'carCode',carNum)
        excel = ExcelUnitl(file)
        excel.editCell(1, 0, billDict['ticketCode'])
        excel.editCell(1, 3, carNum)
        excel.editCell(1, 7, '1')
        file = {
            "refundFile": open(file,'rb'),
            "im12portFile": "self.importFile.importFile"
        }
        self.url = "/mgr/monthTicketBill/batchRefund.do"
        re =self.post(self.api, files = file, headers = {'User-Agent':'Chrome/71.0.3578.98'})
        if re.json()['status'] == 1 :
            re = self.__getBatchRefundResult()
        return re.json()['data']

    def __getBatchRefundResult(self):
        """获取批量退费结果"""
        self.url = "/mgr/monthTicketBill/getBatchRefundResult.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def batchRenewMonthTicketBill(self, parkName, carNum, fileName = "批量续费月票.xls"):
        """批量续费月票"""
        file = root_path + '/upload/' + fileName
        Index(self.Session).downloadExcelTmp("renew_month_ticket_bill.xls", file)
        ticketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '不在有效期'),'carCode',carNum)
        self.__editBatchRenewBillFile(file, ticketBillDict['ticketCode'], carNum)
        file = {
            "renewFile": open(file,'rb')
        }
        self.url = "/mgr/monthTicketBill/renewBills.do"
        re = self.post(self.api, files = file, headers = {'User-Agent':'Chrome/71.0.3578.98'})
        if re.json()['status'] == 1:
            re = self.__getRenewBillResult()
        return re.json()['data']

    def __editBatchRenewBillFile(self, file, ticketCode, carNum):
        """修改批量续费excel文件"""
        excel = ExcelUnitl(file)
        excel.editCell(1, 0, ticketCode)
        excel.editCell(1, 3, carNum)
        excel.editCell(1, 4, "{} 00:00:00".format(SA().get_today_data()))
        excel.editCell(1, 5, "{} 23:59:59".format(SA().cal_get_day(strType="%Y-%m-%d", days=15)))
        excel.editCell(1, 7, 30)

    def __getRenewBillResult(self):
        """获取续费导入结果"""
        self.url = "/mgr/monthTicketBill/getRenewBillsResult.do"
        re =self.get(self.api, headers = form_headers)
        return re


    def resyncMonthTicketBill(self,parkName, carNum, combinedStatus='生效中'):
        """重新同步月票订单"""
        ticketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName,combinedStatus = combinedStatus),'carCode',carNum)
        data = {
            "monthTicketBillId":ticketBillDict.get('id'),
            "ticketCode":ticketBillDict.get('ticketCode')
        }
        self.url = "/mgr/monthTicketBill/resync.do"
        re = self.post(self.api, data = data, headers =form_headers)
        return re.json()