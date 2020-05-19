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
    carTypeDict = {'蓝牌车':1, '黄牌车':2, '新能源小车':4, '新能源大车': 3}

    def mockCarInOut(self,carNum,mockType,ytj_id,confidence = 91,carType = '蓝牌车'):
        self.url = "/mock_car_in_out"
        json_data = {
        "message_id":SA().get_uuid(),
        "timestamp":SA().get_time(),
        "biz_content":{
            "car_plate":carNum,
            "mock_type":mockType, # 取消进出类型
            "ytj_id":ytj_id,
            "confidence": confidence,
            "job_id":SA().get_uuid(),
            "car_size": self.carTypeDict[carType]
            }
        }
        re = self.post(self.mock_api, json=json_data, headers=self.api_headers)
        try:
            if str(mockType) == '1':
                self.save('carOut_jobId',re.json()['biz_content']['job_id'])
            elif str(mockType) == '0':
                self.save('carIn_jobId', re.json()['biz_content']['job_id'])
        except KeyError:
            raise KeyError("【{}】一体机状态异常，无法进出车！".format(ytj_id))
        return re.json()['biz_content']['result']

    def getCarMsgYtj(self,job_id):
        """
        获取车场进出场一体机的返回的信息
        :param job_id:
        :return:
        """
        self.url = "/get_ytj_msg"
        json_data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content": {
                "job_id": job_id
            }
        }
        re = self.post(self.mock_api, json=json_data, headers=self.api_headers)
        return re.json()['biz_content']['result']

    def _getCenterMonitorHandleCarMsg(self, carNum):
        """远程值班 -获取车场进出场处理车辆信息"""
        data = {
           "message_id": SA().get_uuid(),
           "timestamp": SA().get_time(),
           "biz_content":{
              }
        }
        self.url = "/get_center_monitor_msg"
        re = self.post(self.mock_api, json=data, headers=self.api_headers)
        result = re.json()['biz_content']['center_monitor_msg']
        if result['msgType'] == "CORRECT_CAR_NO_ALERT" :
            if result['data']['carNo'] == carNum :
                return result['data']
        else:
            result = result['data']
            if result['msg_type'] == '进车':
                if result['carInMsg']['carNo'] == carNum:
                    return result
                else:
                    # print('该进车信息不是车辆【{}】'.format(carNum))
                    result = self.setValueByDict(result, ['carInMsg','carNo'], carNum)
                    return result
            elif result['msg_type'] == '出车':
                if result['carOutMsg']['leaveCarNo'] == carNum:
                    return result
                else:
                    # print('该出车信息不是车辆【{}】'.format(carNum))
                    result = self.setValueByDict(result, ['carOutMsg', 'leaveCarNo'], carNum)
                    return result
            else:
                print('接口返回值错误！！')

    def getCenterMonitorMsgList(self):
        """获取远程值班-接收信息列表"""
        data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content": {
            }
        }
        self.url = "/get_center_monitor_msg_list"
        re = self.post(self.mock_api, json=data, headers=self.api_headers)
        return re.json()

    def checkYtjOnlineList(self):
        """查看在线一体机"""
        self.url = "/check_ytj_list"
        data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content": {
            }
        }
        re = self.post(self.mock_api, json=data, headers = self.api_headers)
        return re


if __name__ == "__main__":
    b = cloudparking_service().mockCarInOut("粤A75034",0,"20190507171501")
    # b = cloudparking_service().checkYtjOnlineList()

    # print(b.json())