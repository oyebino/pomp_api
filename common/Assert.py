# -*- coding: utf-8 -*-
# @File  : test_order.py
# @Author: 叶永彬
# @Date  : 2018/9/10
# @Desc  :
"""
封装Assert方法

"""
from common.logger import logger
from common import Consts
import json,os
from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))

class Assertions:
    def __init__(self):
        self.log = logger
        # if len(tempDataPath.changeCaseNameListList) > 0:
        #     tempDataPath.changeCaseNameList.pop(0)
        # else:
        #     tempDataPath.changeCaseNameList = eval(tempDataPath.caseNameList)

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            self.log.info("===验证状态码：{}=={}".format(code,expected_code))
            return True
        except:
            self.log.error("===状态码错误, 预期验证码是：{}, 实际验证码是: {} ".format(code,expected_code))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            self.log.info("===验证结果值：{}=={}".format(msg,expected_msg))
            return True

        except:
            self.log.error("===响应结果值 != 预期值, 预期值是：{} , 响应结果值：{}".format(expected_msg, body_msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值是否包含
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert str(msg) in str(self.__formatExpected(expected_msg))
            self.log.info("===验证结果值：{}包含{}".format(msg, expected_msg))
            return True

        except:
            self.log.error("===响应结果值 不包含 预期值, 预期值是：{} , 响应结果值：{}".format(expected_msg, body_msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            expected_msg = self.__formatExpected(str(expected_msg)).lower()
            text = json.dumps(body, ensure_ascii=False).lower()
            # print(text)
            assert expected_msg in text
            self.log.info("===响应的结果值包含预期值,响应值：{},预期值:{}".format(text,expected_msg))
            return True

        except:
            self.log.error("===响应的结果值不包含预期值, 响应值：{},预期值:{}".format(text,expected_msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_not_in_text(self, body, expected_msg):
        """
        验证response body中不包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg not in text
            self.log.info("===响应的结果值不包含预期值,响应值：{},预期值:{}".format(text,expected_msg))
            return True

        except:
            self.log.error("===响应的结果值包含预期值, 响应值：{},预期值:{}".format(text,expected_msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == self.__formatExpected(expected_msg)
            self.log.error("===响应结果与预期值一致, 预期值是： {}, 响应结果是： {}".format(expected_msg, body))
            return True

        except:
            self.log.error("===响应结果 != 预期值, 预期值是： {}, 响应结果是： {}".format(expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            self.log.info("===响应时间<预期响应时间,预期响应时间：{},响应时间:{}".format(expected_time,time))
            return True

        except:
            self.log.error("===响应时间 > 预期响应时间, 预期响应时间:{}, 响应时间:{}".format(expected_time, time))
            Consts.RESULT_LIST.append('fail')

            raise

    def __formatExpected(self,template):
        """
        解析期望值传进的值
        :return:
        """
        import re
        rule = r'\${(.*)}'
        textList = re.findall(rule, template)
        text_dic = {}
        for key in textList:
            caseName = str(key).split('.')[0]
            keyProperty = str(key).split('.')[1]
            value = self.__get_caseData(keyProperty, caseName)
            text_dic[key] = value
        for key in list(text_dic.keys()):
            strKey = "${" + key + "}"
            template = template.replace(strKey, text_dic[key])
        return template

    def __get_caseData(self,nodeName,caseName = None):
        """
        提取运行案例值
        :return:
        """
        if caseName ==None:
            caseName = str(tempDataPath.runingCaseName).lower()
        else:
            caseName = str(caseName).lower()
        fileList = FloderUtil().getListFloder(root_path + "/temporaryDataLog")
        for file in fileList:
            if str(file).lower().find(caseName):
                run_data = XmlHander(file).getValueByName(nodeName)
                return run_data
            else:
                pass