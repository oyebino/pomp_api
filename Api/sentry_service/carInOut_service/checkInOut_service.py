"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""

from common.Req import Req
from common.db import Db

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class CheckInOut(Req):
    """
    pc收费端相关业务：获取所有消息id，对消息记录确认放行、收费放行、异常放行
    """

    # def check_message_in_out(self):
    #     """
    #     获取所有消息并提取最新id--该方法废弃！
    #     """
    #     print("self.host****",self.host)
    #     data = {
    #         "type": "undeal",
    #         "pageNumber": "1",
    #         "pageSize": "250"
    #     }
    #     self.url = "/ydtp-backend-service/api/messages?" + urlencode(data)
    #     re = self.get(self.api, headers=form_headers)
    #     print("消息：",re.json())
    #     messageList = re.json()['list']
    #     if len(messageList) != 0:
    #         id = re.json()["list"][0]["id"]
    #         print("消息id:",id)
    #         return id
    #     else:
    #         return None

    def check_car_in_out(self,parkId):
        """
        点击消息，然后点击确认放行
        """
        sql = "SELECT id FROM park_sentry_duty_message WHERE park_id = '{}' ORDER BY id DESC LIMIT 1".format(parkId)
        message_id = Db().select(sql)
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "确认放行",
            "reason": ""
        }
        re = self.post(self.zby_api, data=data, headers=form_headers)
        return re.json()

    def normal_car_out(self, parkId):
        """
        点击收费放行
        """
        sql = "SELECT id FROM park_sentry_duty_message WHERE park_id = '{}' ORDER BY id DESC LIMIT 1".format(parkId)
        message_id = Db().select(sql)
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "收费放行",
            "reason": ""
        }

        re = self.post(self.zby_api, data=data, headers=form_headers)
        return re.text

    def abnormal_car_out(self, parkId):
        """
        异常放行
        """
        sql = "SELECT id FROM park_sentry_duty_message WHERE park_id = '{}' ORDER BY id DESC LIMIT 1".format(parkId)
        message_id = Db().select(sql)
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
        data = {
            "type": "异常放行",
            "reason": "",
            "real_value": '1'
        }
        self.save('real_value',data['real_value'])
        re = self.post(self.zby_api, data=data, headers=form_headers)
        return re.text

    def adjust_carNum_carType(self,parkId,adjustCarNum,carType = None):
        """校正车牌与类型"""
        sql = "SELECT id FROM park_sentry_duty_message WHERE park_id = '{}' ORDER BY id DESC LIMIT 1".format(parkId)
        message_id = Db().select(sql)
        self.url = "/ydtp-backend-service/api/messages/{}/carCode".format(message_id)
        data = {
            "car_code": adjustCarNum,
            "operateSource": "2",
            "carType": carType
        }
        re =self.post(self.zby_api,data=data,headers = form_headers)
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

if __name__ == '__main__':
    CheckInOut().normal_car_out('fc41068f-3862-4979-a87d-d303893b1151')