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
    const.parkJson = str([{"parkVipTypeId":"","parkId":3751,"parkUuid":"54a33015-d405-499e-bce2-e569cd9dce6a","parkName":"智泊云接口测试专用停车场","chargeGroupCode":"0","optionArr":[{"chargeTypeSeq":"0","typeName":"接口测试专用计费组1","parkUuid":"54a33015-d405-499e-bce2-e569cd9dce6a"},{"chargeTypeSeq":"316","typeName":"接口测试专用计费组2","parkUuid":"54a33015-d405-499e-bce2-e569cd9dce6a"}],"parkSysType":1}])

    const.parkVipTypeJson = str({"customVipName" : "","settlementType" : 0,"isDynamicMode" : 0,"isDatePrivilege" : 0,"isTimePrivilege" : 0,"privilegeTimePeriod" : "","isChargeGroupRelated" : 0,"vipGroupType" : 0,"dynamicFullLimit" : 0,"vipNearExpiredDayThreshold" : "10","vipDeleteExpiredDayThreshold" : 0,"openVipFullLimit" : 0,"vipFullLimitValue" : 0,"vipFullOpenModel" : 0,"priTimeArrFrom" : "","priTimeArrTo" : "","priDateArrStr" : "","parkId" : "","parkName" : "","channelAuthTree" : "[{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2022,\"name\":\"智泊云接口测试入口\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2022,\"isHidden\":false,\"isFirstNode\":true,\"tId\":\"ParkTree_195\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isLastNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false},{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2023,\"name\":\"智泊云接口测试出口\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2023,\"tId\":\"ParkTree_196\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isFirstNode\":false,\"isLastNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false,\"isHidden\":false},{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2063,\"name\":\"智泊云接口测试入口-严进\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2063,\"tId\":\"ParkTree_197\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isFirstNode\":false,\"isLastNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false,\"isHidden\":false},{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2063,\"name\":\"智泊云接口测试入口-严进\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2063,\"tId\":\"ParkTree_198\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isFirstNode\":false,\"isLastNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false,\"isHidden\":false},{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2064,\"name\":\"智泊云接口测试出口-严出\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2064,\"tId\":\"ParkTree_199\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isFirstNode\":false,\"isLastNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false,\"isHidden\":false},{\"chkDisabled\":false,\"parkName\":\"智泊云接口测试专用停车场\",\"level\":2,\"hasChildren\":false,\"parkSysType\":1,\"type\":2,\"parkId\":3751,\"parkUuid\":\"54a33015-d405-499e-bce2-e569cd9dce6a\",\"areaId\":223,\"channelSeq\":2064,\"name\":\"智泊云接口测试出口-严出\",\"checked\":true,\"nocheck\":false,\"open\":false,\"channelId\":2064,\"isHidden\":false,\"isLastNode\":true,\"tId\":\"ParkTree_200\",\"parentTId\":\"ParkTree_194\",\"isParent\":false,\"zAsync\":true,\"isFirstNode\":false,\"isAjaxing\":false,\"pId\":223,\"checkedOld\":false,\"halfCheck\":false,\"check_Child_State\":-1,\"check_Focus\":false,\"isHover\":false,\"editNameFlag\":false}]","channelSeqList" : [],"autoSwitchVip" : 0,"offLine" : 1})

    const.showMessage = str({"validInWarnOut":{"carIn":{"easy":{"text":"%P\\%VM","voice":"%P%VM"},"hard":{"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}},"carOut":{"easy":{"text":"%P\\%VM","voice":"%P%VM"},"hard":{"text":"%P\\%VM请稍候","voice":"%P%VM请稍候"}}},"validInWarnIn":{"carIn":{"easy":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}},"carOut":{"easy":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"},"hard":{"text":"%P\\剩余%VT天","voice":"%P剩余%VT天"}}},"validOutDelIn":{"carIn":{"easy":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"}},"carOutPay":{"easy":{"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"},"hard":{"text":"%VM已过期\\应缴费%C元","voice":"%VM已过期应缴费%C元"}},"carOutNoPay":{"easy":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"},"hard":{"text":"%P\\%VM已过期","voice":"%P%VM已过期"}}}})

class tempDataPath():

    temporaryDataPath = root_path + '/temporaryDataLog' # 父目录

    runingCaseName = 'default'   # 当前运行的案例名

    cur_time = None

if __name__ == "__main__":
    print(root_path)