#coding=UTF-8
from selenium import webdriver
import time


driver=webdriver.Chrome()

driver.get('http://www.baidu.com')
time.sleep(2)
#driver.implicitly_wait(2)
driver.maximize_window()
