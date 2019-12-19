#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 10:26
# @Author  : 叶永彬
# @File    : cloudparking_service.py



from common.Req import Req
from common.db import Db as db
from common.superAction import SuperAction as SA
from Config.Config import Config

class cloudparking_service(Req):
    """
    模拟智泊云设备
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}

    def mock_car_in_out(self,carNum,mockType,ytj_id):
        url = "http://10.10.17.219:9002/mock_car_in_out"
        json_data = {
        "message_id":SA().get_uuid(),
        "timestamp":SA().get_time(),
        "biz_content":{
            "car_plate":carNum,
            "mock_type":mockType,
            "ytj_id":ytj_id,
            "job_id":SA().get_uuid()
            }
        }

        re = self.post(url, json=json_data, headers=self.api_headers)
        return re

if __name__ == "__main__":
    s = cloudparking_service().mock_car_in_out("粤NB6667","1","20190507171500")