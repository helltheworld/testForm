# -*- coding: utf-8 -*-
import unittest
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,urllib2,cookielib,urllib,json
from bs4 import BeautifulSoup
from test_data import *


class public_tools():

    def find_ele(self, methods):  # 定位函数
        method = methods.split(",")[0]
        value = methods.split(",")[1]
        if method == "name":
            locate = self.driver.find_element_by_name(value)
        elif method == "id":
            print 1
            locate = self.driver.find_element_by_id(value)
        elif method == "xpath":
            locate = self.driver.find_element_by_xpath(value)
        elif method == "class":  # 传入复合类名称时，会报错，挑选合适的类名
            locate = self.driver.find_element_by_class_name(value)
        elif method =="link_text":
            locate =self.driver.find_element_by_link_text(value)

        else:
            raise NameError("get a invalid type of selector name")
        return locate

    def type(self, methods, text):  # 输入函数
        locate = self.find_ele(methods)
        locate.clear()
        locate.send_keys(text)

    def clickButton(self, methods):
        button = self.find_ele(methods)
        time.sleep(1)
        button.click()

    def do_login(self, name, password):
        self.driver.get(host+page_path["pathLogin"])
        self.type("name,email", name)
        self.type('name,password', password)
        self.clickButton('class,btn-success')

    def set_page(self,pageSize, pageNum=1):
        """
        输入每页显示多少条（10,20,30,40）
        输入需要进入第几页
        :param pageSize:
        :param pageNum:
        :return:
        """
        toto=True
        if type(pageNum) != int and type(pageSize) != int:
            print "set page failed ,please enter a number in pageSize and pageNum"
        elif pageSize == 10:
            self.clickButton("xpath,.//span[@class='el-pagination__sizes']/div/div/i")
            self.clickButton("xpath,html/body/div[2]/div/div[1]/ul/li[1]")
        elif pageSize == 20:
            self.clickButton("xpath,.//span[@class='el-pagination__sizes']/div/div/i")
            self.clickButton("xpath,html/body/div[2]/div/div[1]/ul/li[2]")
        elif pageSize ==30:
            self.clickButton("xpath,.//span[@class='el-pagination__sizes']/div/div/i")
            self.clickButton("xpath,html/body/div[2]/div/div[1]/ul/li[3]")
        elif pageSize ==40:
            self.clickButton("xpath,.//span[@class='el-pagination__sizes']/div/div/i")
            self.clickButton("xpath,html/body/div[2]/div/div[1]/ul/li[4]")
        else:
            toto=False
        if toto:
            formAll=self.form_all()
            pageAll=formAll/pageSize
            self.type("class,el-pagination__editor",pageNum)
            self.clickButton("class,formList")
            time.sleep(2)
        else:
            raise  NameError ("there is no pageSize %s")%pageSize

    def form_all(self):
        self.assertEqual()
        formNum=int(self.find_ele("class,formAll").text.split(":")[1])
        return  formNum

    def excute_js(self,js,r=0):
        """
        如果传入值 r=1，那么执行的js会根据js内容 返回值
        :param js:
        :param r:
        :return:
        """
        if r==0:
            self.driver.execute_script(js)
        elif r==1:
            content=self.driver.execute_script(js)
            return content
        else:
            raise NameError

    def login_api(self):
        """
        获取登录token，并且登录
        :return:
        """
        self.cj=cookielib.CookieJar()
        self.handler=urllib2.HTTPCookieProcessor(self.cj)
        self.opener=urllib2.build_opener(self.handler)
        urllib2.install_opener(self.opener)
        res = urllib2.Request(host+page_path["pathLogin"])
        req = urllib2.urlopen(res)
        soup=BeautifulSoup(req,"lxml")
        token=soup.find("input" ).get("value")
        data={
            '_token':token,
            'email':email["email_r"],
            "password":pwd["pwd_r"]
        }
        data_encode=urllib.urlencode(data)
        log_req=urllib2.Request(host+page_path["pathLogin"],data=data_encode)
        log_res=urllib2.urlopen(log_req).read()
        for i ,x in enumerate(self.cj):
            print i,x


    def form_list_api(self,page="all"):
        """
        page="all' or page='a',requst formAll,
        page='collect' or ppage='c' ,request mycollect
        #details="status,catagroy,projectid,searchcontent,collectForm,pageSize,authid"
        :param details:
        :return:
        """
        self.login_api()
        self.list_req=urllib2.Request(host+page_path["pathApiList"])
        listPostData="status=all&categoryId=all&projectId=all&searchContent=&collectForm=0&pageSize=10&authorId=7"
        self.list_res=urllib2.urlopen(self.list_req,data=listPostData)
        formAll=json.load(self.list_res)
        return formAll
def single_suite(testClass,testCase):
    """
    testsuite支持单用例调用测试，可以在编写用例的过程中进行单独用例的测试验证
    传入值为：测试用例的函数名称即可，单次可上传一个
    :return:
    """
    suite=unittest.TestSuite()
    suite.addTest(testClass(testCase))
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
def single_test_loader(cls):
    """
    在testloader中，需要在套件中传入测试类的名称，而不是测试用例的名称
    所以testloader是进行测试调用的测试方法
    :return:
    """
    loader=unittest.TestLoader()
    suite1=loader.loadTestsFromTestCase(cls)
    suite=unittest.TestSuite([suite1,])
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__=="__main__":
    #unittest.main(verbosity=2) #执行当前类中所有的测试用例
    #single_test_loader(formLogin) #执行指定类下的测试用例
    #single_suite(formCenter,"test_enter_formList")  #执行单条测试用例
    a=public_tools()
    a.login_api()