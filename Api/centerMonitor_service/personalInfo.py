"""
 Created by lgc on 2020/2/26 15:32.
 微信公众号：泉头活水
"""
import json

from common.Req import Req


form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CenterPersonalInfo(Req):

    """
     查看操作日志
     """
    def logList(self):
        self.url = "/zbcloud/center-monitor-service/log/list"
        data = {
                "pageNumber": "1",
                "pageSize": "20"
            }
        re = self.post(self.monitor_api, json=data, headers=json_headers)
        return re