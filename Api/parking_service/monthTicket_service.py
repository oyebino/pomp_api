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
from common.XmlHander import XmlHander as xmlUtil

class monthTicket_controller(Req):
    """
    月票管理
    """
    api_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def save_monthTicketType(self,monthTicketName):
        """
        创建月票类型
        """
        self.url = "/mgr/monthTicketConfig/save.do"
        json_data = {
            "ticketName": monthTicketName,
            "ticketType": "OUTTER",
            "renew": 1,
            "price": 30,
            "renewMethod": "NATURAL_MONTH",
            "maxSellLimit": "NO",
            "financialParkId": 3751,
            "parkJson": const.parkJson,
            "renewFormerDays": 0,
            "inviteCarTotal": 1,
            "continueBuyFlag": 1,
            "supportVirtualCarcode": 0,
            "parkVipTypeJson": const.parkVipTypeJson,
            "inviteCarSwitcher": 0,
            "validTo": "2030-01-31 23:59:59",
            "sellFrom": SA().get_now_time(),
            "sellTo": SA().get_now_time(),
            "showMessage": const.showMessage
        }
        re = self.post(self.api, data=json_data, headers=self.api_headers)
        return re

    def open_monthTicket(self, carNum, monthTicketName):
        """
        开通月票
        """
        self.url = "mgr/monthTicketBill/open.do"
        monthTicketIdSql = "select id from month_ticket_config where TICKET_NAME = '"+monthTicketName+"'"
        monthTicketId = db().select(monthTicketIdSql)
        json_data = {
        "monthTicketId": monthTicketId,
        "monthTicketName": monthTicketName,
        "timeperiodListStr": SA().get_two_natural_month(),
        "userName": "autotest",
        "userPhone": "15012345678",
        "price": 30,
        "totalValue": 30.00,
        "openMonthNum": 1,
        "realValue": 30,
        "inviteCarTotal": 1,
        "dynamicCarportNumber": 1,
        "carCode": carNum,
        }
        re = self.post(self.api, data=json_data, headers=self.api_headers)
        return re

    def renew_monthTicket(self, carNum, monthTicketName):
        """
        月票续费
        """
        self.url = "mgr/monthTicketBill/renew.do"
        monthTicketIdSql = "select id from month_ticket_config where TICKET_NAME = '"+monthTicketName+"'"
        monthTicketId = db().select(monthTicketIdSql)
        monthTicketBillIdSql = "select id from MONTH_TICKET_BILL where CAR_CODE = '"+carNum+"' ORDER BY id DESC LIMIT 1;"
        monthTicketBillId = db().select(monthTicketBillIdSql)
        json_data = {
        "monthTicketId": monthTicketId,
        "monthTicketName": monthTicketName,
        "monthTicketBillId": monthTicketBillId,
        "timeperiodListStr": SA().get_next_natural_month(),
        "userName": "autotest",
        "userPhone": "15012345678",
        "price": 30,
        "totalValue": 30.00,
        "openMonthNum": 1,
        "realValue": 30,
        "dynamicCarportNumber": 1,
        }
        re = self.post(self.api, data=json_data, headers=self.api_headers)
        return re

    def refund_monthTicket(self, carNum):
        """
        月票退款
        """
        self.url = "mgr/monthTicketBill/refund.do"
        monthTicketBillIdSql = "select id from MONTH_TICKET_BILL where CAR_CODE = '"+carNum+"' ORDER BY id DESC LIMIT 1;"
        monthTicketBillId = db().select(monthTicketBillIdSql)
        json_data = {
        "monthTicketBillId": monthTicketBillId,
        "refundValue": 30,
        "remark": "接口退款",
        "realValue": 6000

        }
        re = self.post(self.api, data=json_data, headers=self.api_headers)
        return re
    def create_monthTicket(self):
        pass

if __name__ == "__main__":
    re =monthTicket_controller().save_monthTicketType()
    print(re.json())