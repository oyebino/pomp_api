# -*- coding: utf-8 -*-
# @File  : News_page.py
# @Author: 叶永彬
# @Date  : 2018/11/15
# @Desc  :


from Pages.base_page import BasePage


class NewsPage(BasePage):
    """私隐设置页面"""

    url = "/duty/privacysettings.html"

    def settings(self,keyword):

        self.open()
