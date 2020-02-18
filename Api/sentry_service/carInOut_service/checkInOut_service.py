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
            "real_value": "1"
        }
        re = self.post(self.zby_api, data=data, headers=form_headers)
        return re.text


if __name__ == '__main__':
    CheckInOut().normal_car_out('54a33015-d405-499e-bce2-e569cd9dce6a')