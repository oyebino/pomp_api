"""
 Created by lgc on 2020/2/26 15:32.
 微信公众号：泉头活水
"""

from common.Req import Req

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CarInOutHandle(Req):
    """远程值班室-处理车辆"""
    def checkIn(self):

        data = {
            "carInOutId": 1,
            "dutyMessage": 1,
            "handleMessage": "放行原因为：",
            "reason": ""
        }
        self.url = "/zbcloud/center-monitor-service/in-out/check-in"
        re = self.post(self.monitor_api, json = data, headers = json_headers)