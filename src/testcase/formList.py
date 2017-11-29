#coding=UTF-8

import unittest
from testtoll import *
from selenium import webdriver
import time
import urllib2

class formList(unittest.TestCase,public_tools):
    def setUp(self):
        self.driver=webdriver.Chrome()
        self.do_login(email["email_r"], pwd["pwd_r"])
        self.driver.get(host+page_path["pathList"])

    def test_allForm(self):
        self.excute_js('document.getElementsByClassName("el-tabs__nav")[0].children[0].click()')
        tab_status = self.excute_js('return document.getElementsByClassName("el-tabs__item")[1].getAttribute("class").split(" ")[1]',1)  # 获取的是全部的激活属性
        self.assertEqual("is-active", tab_status)
        # style_display=self.excute_js('return document.getElementsByClassName("el-tab-pane formTable")[0].getAttribute("style")',1)
        # self.assertEqual(None,style_display)
    def test_MyCollection(self):
        self.excute_js('document.getElementsByClassName("el-tabs__nav")[0].children[1].click()')
        tab_status=self.excute_js('return document.getElementsByClassName("el-tabs__item")[1].getAttribute("class").split(" ")[1]',1)#获取的是收藏按钮的激活属性
        self.assertEqual("is-active", tab_status)
        #style_display=self.excute_js('return document.getElementsByClassName("el-tab-pane formTable")[1].getAttribute("style")',1) #获取的是全部/收藏tab的style属性
        #self.assertEqual(None, style_display)

    def tearDown(self):
        time.sleep(10)
        self.driver.quit()


if __name__ == "__main__":
    single_suite(formList,"test_MyCollection")