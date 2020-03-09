#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 10:26
# @Author  : 叶永彬
# @File    : cloudparking_service.py

from common.Req import Req
from common.superAction import SuperAction as SA

class cloudparking_service(Req):
    """
    模拟智泊云设备
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    host = "http://10.10.17.219:9002"

    # def mock_car_in_out(self,carNum,mockType,ytj_id,confidence = 91,carType = 1):
    def mockCarInOut(self,carNum,mockType,ytj_id,confidence = 91,carType = 1):
        url = "http://mock.dev.yidianting.com.cn/mock_car_in_out"
        json_data = {
        "message_id":SA().get_uuid(),
        "timestamp":SA().get_time(),
        "biz_content":{
            "car_plate":carNum,
            "mock_type":mockType,
            "ytj_id":ytj_id,
            "confidence": confidence,
            "job_id":SA().get_uuid(),
            "car_size": carType
            }
        }
        re = self.post(url, json=json_data, headers=self.api_headers)
        if str(mockType) == '1':
            self.save('carOut_jobId',re.json()['biz_content']['job_id'])
        elif str(mockType) == '0':
            self.save('carIn_jobId', re.json()['biz_content']['job_id'])
        return re

    # def get_car_msg_ytj(self,job_id):
    def getCarMsgYtj(self,job_id):
        """
        获取车场进出场一体机的返回的信息
        :param job_id:
        :return:
        """
        url = "http://mock.dev.yidianting.com.cn/get_open_gate_msg"
        json_data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content": {
                "job_id": job_id
            }
        }
        re = self.post(url, json=json_data, headers=self.api_headers)
        return re

if __name__ == "__main__":
    a = cloudparking_service().mockCarInOut("粤Y98175",0,"20190507171500")
    # a = cloudparking_service().get_car_msg_ytj("52dc11eab4f97427eac14803")
    re = a.json()
    # print(re['result']['voice'])