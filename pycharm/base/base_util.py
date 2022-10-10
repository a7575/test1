from selenium import webdriver
import pytest
import time
import warnings
from common.logging_util import write_log, error_log

class Library:

    def __init__(self):
        self.driver=None
        if self.driver is None:
            self.driver=webdriver.Chrome()

    def open_browser(self, browser):
        try:
            browser = browser.capitalize()
            warnings.simplefilter('ignore', ResourceWarning)
            self.driver = getattr(webdriver, browser)()
            write_log(f"打开{browser}浏览器成功")
        except:
            error_log(f"打开{browser}浏览器失败")

    def driver_quit(self):
        try:
            self.driver.quit()
            write_log("退出浏览器成功")
        except:
            error_log("退出浏览器失败")


    def load_url(self, url):
        try:
            self.driver.get(url)
            write_log(f"打开项目地址{url}成功")
        except:
            error_log(f"打开项目地址{url}失败")

    # locate_mode定位方法，statement定位语句
    def locator(self, locate_mode, locate_statement):
        try:
            ele = self.driver.find_element(locate_mode, locate_statement)
            write_log(f"元素{ele}定位成功")
            return ele
        except:
            error_log(f"{locate_mode,locate_statement}定位失败")

    def input(self, locate_mode, locate_statement, value):
        try:
            self.locator(locate_mode, locate_statement).send_keys(value)
            write_log(f"元素{value}输入成功")
        except:
            error_log(f"元素{value}输入失败")

    def click(self, locate_mode, locate_statement):
        try:
            self.locator(locate_mode, locate_statement).click()
            write_log(f"元素{locate_statement}点击成功")
        except:
            error_log(f"元素{locate_statement}点击失败")

    def sleep(self, s):
        try:
            time.sleep(s)
            write_log(f"等待{s}秒成功")
        except:
            error_log(f"等待{s}秒失败")


    def asserteque(self, locate_mode, locate_statement, express):

        el = self.locator(locate_mode, locate_statement)
        fact = el.text
        if fact != express:
            raise Exception(f"asserttext:{fact}不等于{express},断言失败")
        #log().getLogger().info(f"断言：{express}  成功")



    def run(self, keyword, *args):
        getattr(self, keyword)(*args)
