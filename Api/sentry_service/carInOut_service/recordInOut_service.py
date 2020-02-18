"""
 Created by lgc on 2020/2/9 19:33.
 微信公众号：泉头活水
"""

from common.Req import Req
from common.superAction import SuperAction

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class RecordInOut(Req):
    """
    获取pc端进出场记录
    """
    def record_car_in(self):
        """
        获取进场记录
        """
        self.url = "/ydtp-backend-service/api/records"
        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "in",
            "begin_time": "{} 00:00:00".format(SuperAction().get_time(strType="%Y-%m-%d")),
            "end_time": "{} 23:59:59".format(SuperAction().get_time(strType="%Y-%m-%d"))
        }
        re = self.get(self.zby_api, params=data, headers=form_headers)
        r = re.json()
        return r

    def record_car_out(self):
        """
        获取出场记录
        """
        self.url = "/ydtp-backend-service/api/records"
        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "out",
            "begin_time": "{} 00:00:00".format(SuperAction().get_time(strType="%Y-%m-%d")),
            "end_time": "{} 23:59:59".format(SuperAction().get_time(strType="%Y-%m-%d"))
        }

        re = self.get(self.zby_api, params=data, headers=form_headers)
        r = re.json()
        return r
