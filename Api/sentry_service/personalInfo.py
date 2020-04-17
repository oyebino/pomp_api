"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
from urllib.parse import urlencode
from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}

class PersonalInfo(Req):
    """个人中心"""

    def webHandOverDuty(self,handUser,pwd):

        """交接班"""
        self.url = "/ydtp-backend-service/api/web_hand_over_duty"
        data = {
            "user_id": handUser,
            "password": pwd
        }
        re = self.post(url=self.zby_api,data=data, headers=form_headers)
        return re.text


    def offduty(self):

        """退出登录"""
        self.url = "/ydtp-backend-service/api/offduty"
        re = self.post(url=self.zby_api, headers=form_headers)
        return re.text

    def dutyInfo(self):

        """个人信息"""
        self.url = "/ydtp-backend-service/api/duty"
        re =self.get(url=self.zby_api, headers=form_headers)
        return re.json()

    def __shiftRecords(self):
        """收费汇总列表"""
        data = {
            "pageNumber": 1,
            "pageSize": 1
        }
        self.url = "/ydtp-backend-service/api/shift_records?" + urlencode(data)
        re = self.get(self.zby_api)
        return re

    def shiftMoneys(self):
        """查看收费流水清单"""
        id = self.__shiftRecords().json()['list'][0]['id']
        data = {
            "pageNumber": 1,
            "pageSize": 20
        }
        self.url = "/ydtp-backend-service/api/shift_records/{}/shift_moneys?{}".format(id,urlencode(data))
        re = self.get(self.zby_api)
        return re.json()['list']
