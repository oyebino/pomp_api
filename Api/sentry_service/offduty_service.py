"""
 Created by lgc on 2020/2/16 15:48.
 微信公众号：泉头活水
"""

from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}

class SentryOffduty(Req):

    def offduty(self):
        """退出登录"""
        self.url = "/ydtp-backend-service/api/offduty"
        self.post(url= self.api, headers=form_headers)




# class LoginStatus(Req):
#
#     def status(self):
#         """登录或退出检查点"""
#         self.url = "/ydtp-backend-service/api/duty_channel_status"
#         r = self.get(url=self.api, headers=form_headers)
#         r_json = r.json()
#         print("登录检查点：", r_json)
#         print(r.status_code)
#         return r.status_code
