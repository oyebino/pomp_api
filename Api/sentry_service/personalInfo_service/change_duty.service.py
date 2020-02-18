"""
 Created by lgc on 2020/2/16 17:24.
 微信公众号：泉头活水
"""
from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class ChangeDuty(Req):

    def web_hand_over_duty(self):

        """交接班"""
        self.url = "/ydtp-backend-service/api/web_hand_over_duty"
        data = {
            "user_id": "all_apitest",
            "password": "123456"
        }
        self.post(url= self.api,data=data, headers=form_headers)