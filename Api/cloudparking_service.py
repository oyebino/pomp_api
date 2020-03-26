#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 10:26
# @Author  : 叶永彬
# @File    : cloudparking_service.py

from common.Req import Req
from common.superAction import SuperAction as SA
from Config.parameter import LoginReponse

class cloudparking_service(Req):
    """
    模拟智泊云设备
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    host = "http://10.10.17.219:9002"

    def mockCarInOut(self,carNum,mockType,ytj_id,confidence = 91,carType = 1):
        url = "http://10.10.17.219:9002/mock_car_in_out"
        json_data = {
        "message_id":SA().get_uuid(),
        "timestamp":SA().get_time(),
        "biz_content":{
            "car_plate":carNum,
            "mock_type":mockType, # 取消进出类型
            "ytj_id":ytj_id,
            "confidence": confidence,
            "job_id":SA().get_uuid(),
            "car_size": carType
            }
        }
        LoginReponse.loginRe = {"status":1}
        re = self.post(url, json=json_data, headers=self.api_headers)
        if str(mockType) == '1':
            self.save('carOut_jobId',re.json()['biz_content']['job_id'])
        elif str(mockType) == '0':
            self.save('carIn_jobId', re.json()['biz_content']['job_id'])
        return re

    def getCarMsgYtj(self,job_id):
        """
        获取车场进出场一体机的返回的信息
        :param job_id:
        :return:
        """
        url = "http://10.10.17.219:9002/get_open_gate_msg"
        json_data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content": {
                "job_id": job_id
            }
        }
        LoginReponse.loginRe = {"status": 1}
        re = self.post(url, json=json_data, headers=self.api_headers)
        return re

    def getMonitorHandleCarMsg(self):
        """获取车场进出场远程值班处理车辆信息"""
        data = {
           "message_id": SA().get_uuid(),
           "timestamp": SA().get_time(),
           "biz_content":{
              }
        }
        LoginReponse.loginRe = {"status": 1}
        url = "http://10.10.17.219:9002/get_center_monitor_msg"
        re = self.post(url, json=data, headers=self.api_headers)
        return re

if __name__ == "__main__":
    a = cloudparking_service().mockCarInOut("京DDDDD4",0,"20190507171503")
    # a = cloudparking_service().getMonitorHandleCarMsg()
    re = a.json()
    print(re)