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
    host = "http://10.10.17.219:9002"

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

    def check_car_in(self,carNum,job_id):
        """
        严进-确认放行进场
        :param carNum:
        :param job_id:
        :return:
        """
        carInOutIdSql = "SELECT id FROM realtime_car_in_out WHERE car_no='" + carNum +"'  ORDER BY id DESC LIMIT 1"
        carInOutId = db().select(carInOutIdSql)
        url = "https://zbcloud.k8s.yidianting.com.cn/car-in-out-handler-service/in-out/check-car-in"

        json_data = {
          "carInOutId": carInOutId,
          "operateTime": SA().get_time(strType ="%Y-%m-%dT%H:%M:%S.000Z"),
          "operator": "auto",
          "reason": "登记放行"
        }
        self.post(url, json=json_data, headers=self.api_headers)
        re = self.mock_open_gate(job_id)
        return re

    def check_car_out(self,carNum,job_id):
        """
        严出-确认放行
        :param carNum:
        :param job_id:
        :return:
        """
        carInOutIdSql = "SELECT id FROM realtime_car_in_out WHERE car_no='" + carNum +"'  ORDER BY id DESC LIMIT 1"
        carInOutId = db().select(carInOutIdSql)
        url = "https://zbcloud.k8s.yidianting.com.cn/car-in-out-handler-service/in-out/check-car-out"
        json_data={
          "carInOutId": carInOutId,
          "leaveType": 2,   # 放行类型 2:收费放行 3:异常放行
          "operateTime": SA().get_time(strType ="%Y-%m-%d %H:%M:%S"),
          "operator": "auto",
          "payVal": 0,
          "reason": "收费放行"
        }
        self.post(url, json=json_data, headers=self.api_headers)
        re = self.mock_open_gate(job_id)
        return re

    def mock_open_gate(self,job_id):
        url = "http://10.10.17.219:9002/get_open_gate_msg"
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
    a = cloudparking_service().mock_car_in_out("粤T54613","1","20200116092930")
    job_id = a.json()['biz_content']['job_id']
    s = cloudparking_service().check_car_out("粤T54613",job_id)
    # b = cloudparking_service().mock_open_gate("383711eaa5ef7427eac14803")
    print(a.json())