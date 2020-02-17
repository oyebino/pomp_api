"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
from urllib.parse import urlencode
from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class CheckInOut(Req):
    """
    pc收费端相关业务：获取所有消息id，对消息记录确认放行、收费放行、异常放行
    """

    def check_message_in_out(self):
        """
        获取所有消息并提取最新id
        """
        print("self.host****",self.host)
        data = {
            "type": "undeal",
            "pageNumber": "1",
            "pageSize": "250"
        }
        self.url = "/ydtp-backend-service/api/messages?" + urlencode(data)
        re = self.get(self.api, headers=form_headers)
        print("消息：",re.json())
        messageList = re.json()['list']
        if len(messageList) != 0:
            id = re.json()["list"][0]["id"]
            print("消息id:",id)
            return id
        else:
            return None

    def check_car_in_out(self,id):
        """
        点击消息，然后点击确认放行
        """
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "确认放行",
            "reason": ""
        }
        re = self.post(self.api, data=data, headers=form_headers)
        return re.json()

    def normal_car_out(self,id):
        """
        点击收费放行
        """
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "收费放行",
            "reason": ""
        }

        re = self.post(self.api, data=data, headers=form_headers)
        return re.text

    def abnormal_car_out(self, id):
        """
        异常放行
        """
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "异常放行",
            "reason": "",
            "real_value": "1"
        }
        re = self.post(self.api, data=data, headers=form_headers)
        return re.text