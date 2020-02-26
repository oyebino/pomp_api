"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
import json
from time import sleep

import requests

from Api.cloudparking_service import cloudparking_service
from common.Req import Req
from common.db import Db
from common.superAction import SuperAction
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class CarInOutHandle(Req):
    """pc收费端相关业务：获取所有消息id，对消息记录确认放行、收费放行、异常放行"""
    date = SuperAction().get_today_data()

    def check_car_in_out(self, carNum, jobId=""):
        """
        点击消息，然后点击确认放行
        """
        topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
        topBillCode = Db().select(topBillCodeSql)
        messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
        message_id = Db().select(messageIdSql)

        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "确认放行",
            "reason": ""
        }
        re = self.post(self.zby_api, data=data, headers=form_headers)
        sleep(3)  # 可能需要加上延时
        if jobId != "":
            if "success" in re.json() and re.json()["success"] == True:
                result = cloudparking_service().get_car_msg_ytj(jobId)
                return result
        else:
            return re

    def normal_car_out(self, carNum ,jobId=""):
        """
        点击收费放行
        """
        topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
        topBillCode = Db().select(topBillCodeSql)
        messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
        message_id = Db().select(messageIdSql)

        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "收费放行",
            "reason": ""
        }
        re = self.post(self.zby_api, data=data, headers=form_headers)
        if jobId != "":
            if "success" in re.json() and re.json()["success"] == True:
                result = cloudparking_service().get_car_msg_ytj(jobId)
                return result
        else:
            return re


    def abnormal_car_out(self, carNum, jobId=""):
        """
        异常放行
        """
        topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
        topBillCode = Db().select(topBillCodeSql)
        messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
        message_id = Db().select(messageIdSql)

        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "异常放行",
            "reason": "",
            "real_value": '1'
        }
        self.save('real_value',data['real_value'])

        re = self.post(self.zby_api, data=data, headers=form_headers)

        if jobId != "":
            if "success" in re.json() and re.json()["success"] == True:
                result = cloudparking_service().get_car_msg_ytj(jobId)
                return result
        else:
            return re

    def adjust_carNum_carType(self, carNum, adjustCarNum, carType = None):
        """校正车牌与类型"""
        topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
        topBillCode = Db().select(topBillCodeSql)
        messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
        message_id = Db().select(messageIdSql)

        self.url = "/ydtp-backend-service/api/messages/{}/carCode".format(message_id)
        data = {
            "car_code": adjustCarNum,
            "operateSource": "2",
            "carType": carType
        }
        re =self.post(self.zby_api,data=data,headers = form_headers)
        print(re.text)
        if re.json()['open_gate'] == "false":
            re = self.__update_msgId(message_id)
            return re
        else:
            return re

    def __update_msgId(self,id):
        """更新id信息"""
        self.url = "/ydtp-backend-service/api/messages/{}".format(id)
        re = self.get(self.zby_api, headers=form_headers)
        return re

    def match_carNum(self,parkUuid,carNum):
        """人工匹配车牌"""
        topBillCodeSql = "select top_bill_code from area_parking_record where car_code = '{}' ORDER BY enter_time ASC".format(carNum)
        top_bill_code =Db().select(topBillCodeSql)
        recordCodeSql = "select record_code from area_parking_record where car_code = '{}' ORDER BY enter_time ASC".format(carNum)
        record_code = Db().select(recordCodeSql)
        MsgIdSql = "SELECT id FROM park_sentry_duty_message WHERE park_id = '{}' ORDER BY id DESC LIMIT 1".format(parkUuid)
        message_id = Db().select(MsgIdSql)

        self.url = "/ydtp-backend-service/api/messages/{}/match".format(message_id)
        data = {
            "top_bill_code": top_bill_code,
            "area_record_code": record_code,
            "park_uuid":parkUuid
        }
        re = self.post(self.zby_api,data=data,headers=form_headers)
        if re.json()['open_gate'] == False:
            re = self.__update_msgId(message_id)
            return re
        else:
            return re

    def record_car_in(self,car_code,parkId='',mode=''):
        """
        获取进场记录
        """

        data ={
            "car_code":car_code,
            "park_id": parkId,
            "mode":mode,
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "in"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers=form_headers)
        return re

    def record_car_out(self,carNum,mode = "",parkId = ""):
        """
        获取出场记录
        """

        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "car_code": carNum,
            "mode": mode,
            "park_id": parkId,
            "record_type": "out"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers=form_headers)
        return re


if __name__ == '__main__':
    # f =CarInOutHandle()
    # a = f._openGateFail()
    # print(type(a))
    # dict
    # ' object has no attribute '
    # json
    # '
    s = {'a': 5}
    print(json.dumps(s))