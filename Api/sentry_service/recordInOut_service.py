"""
 Created by lgc on 2020/2/9 19:33.
 微信公众号：泉头活水
"""

import requests

from common.superAction import SuperAction

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class RecordInOut():
    """
    获取pc端进出场记录
    """
    def __init__(self, host="https://zbcloud.k8s.yidianting.com.cn"):
        self.S = requests.Session()
        self.host = host

    def record_car_in(self,token):
        """
        获取进场记录
        """
        url = self.host + "/ydtp-backend-service/api/records"
        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "in",
            "begin_time": "{} 00:00:00".format(SuperAction().get_time(strType="%Y-%m-%d")),
            "end_time": "{} 23:59:59".format(SuperAction().get_time(strType="%Y-%m-%d"))
        }
        form_headers['user'] = token
        form_headers['type'] = 'ydtp-pc'
        re = self.S.get(url,params=data, headers=form_headers)
        r = re.json()
        return r

    def record_car_out(self,token):
        """
        获取出场记录
        """
        url = self.host + "/ydtp-backend-service/api/records"
        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "out",
            "begin_time": "{} 00:00:00".format(SuperAction().get_time(strType="%Y-%m-%d")),
            "end_time": "{} 23:59:59".format(SuperAction().get_time(strType="%Y-%m-%d"))
        }
        form_headers['user'] = token
        form_headers['type'] = 'ydtp-pc'
        re = self.S.get(url,params=data, headers=form_headers)
        r = re.json()
        return r

if __name__ == "__main__":
    s = RecordInOut()
    # r = s.record_car_in("8e690b90f4197fee9d2cf6265fb34aa3")
    r = s.record_car_out("8e690b90f4197fee9d2cf6265fb34aa3")
    print(r)
