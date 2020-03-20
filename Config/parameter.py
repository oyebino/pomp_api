#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 13:39
# @Author  : 叶永彬
# @File    : parameter.py

from common import const
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))


class Parameter():
    """
    设置常用变量
    """
    const.showMessage = str({"validInWarnOut":{"carIn":{"easy":{"text":"%P\\%VM","voice":"%P%VM"},"hard":{"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}},"carOut":{"easy":{"text":"%P\\%VM","voice":"%P%VM"},"hard":{"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}}},"validInWarnIn":{"carIn":{"easy":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}},"carOut":{"easy":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}}},"validOutDelIn":{"carIn":{"easy":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"}},"carOutPay":{"easy":{"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"},"hard":{"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"}},"carOutNoPay":{"easy":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"}}}})

class tempDataPath():

    temporaryDataPath = root_path + '/temporaryDataLog' # 父目录

    runingCaseName = 'default'   # 当前运行的案例名

    cur_time = None

class LoginReponse():

    loginRe = None

if __name__ == "__main__":
    print(root_path)