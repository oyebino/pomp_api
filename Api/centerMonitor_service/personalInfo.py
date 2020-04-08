"""
 Created by lgc on 2020/2/26 15:32.
 微信公众号：泉头活水
"""
from common.superAction import SuperAction as SA
from urllib.parse import urlencode
from common.Req import Req


form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class PersonalInfo(Req):

    """
     查看操作日志
     """
    def logList(self):
        self.url = "/zbcloud/center-monitor-service/log/list"
        data = {
                "pageNumber": "1",
                "pageSize": "1"
            }
        re = self.post(self.monitor_api, json=data, headers=json_headers)
        return re.json()['list']

    def getCendutySeat(self):
        """获取当前中央值班人员信息"""
        data = {
            "t": SA.getTimeStamp()
        }
        self.url = "/zbcloud/center-monitor-service/cenduty/seat/vo?" + urlencode(data)
        re = self.get(self.monitor_api)
        return re.json()

    def cendutySeatChangeStatus(self, status):
        """
        远程值班人员上班状态，
        :param status: 上班，离开，下班
        :return:
        """
        statusDict = {
            "上班": 1,
            "离开": 2,
            "下班": 0
        }
        data = {
            "onlineStatus": statusDict[status]
        }
        self.url = "/zbcloud/center-monitor-service/cenduty/seat/change?" + urlencode(data)
        re = self.post(self.monitor_api)
        return re.json()

