# coding: utf-8

import urllib
import urllib2
import re
import pdb
import os
import cookielib
import StringIO
import ConfigParser
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/stdout.log',
                filemode='a')
console = logging.StreamHandler()
class Smzdm(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(console)
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self.account = dict()
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
            'Referer' : 'http://www.smzdm.com/',
            'Origin' : 'http://www.smzdm.com/'
        }
        self.weixin_headers = {
            "Host": "api.smzdm.com",
            "Connection" : " keep-alive",
            "Content-Length" : " 134",
            "Accept" : " */*",
            "Origin" : " https://api.smzdm.com",
            "X-Requested-With" : " XMLHttpRequest",
            "User-Agent" : " Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 wechatdevtools/0.7.0 MicroMessenger/6.3.9 Language/zh_CN webview/0",
            "Content-Type" : " application/x-www-form-urlencoded; charset=UTF-8",
            "Referer" : " https://api.smzdm.com/v1/weixin/bandext?FromUserName=o6HKTjmQ-JPBVtaQ_2gQmlQnWTTQ&key=6a404cd42e1c8daaae40d2bf3b68adf6&f=weixin",
            "Accept-Encoding" : " gzip, deflate",
            "Accept-Language" : " zh-CN,zh;q=0.8",
            "Cookie" : " __jsluid=113fe510ed4b4c950c5e46b3fe321626" }

    # 登录
    def login(self, account):
        self.account = account
        url = "https://zhiyou.smzdm.com/user/login/ajax_check"
        data = urllib.urlencode({
            'username' : account['username'],
            'password' : account['password'],
            'rememberme' : 'on',
            'redirect_url' : 'http://www.smzdm.com'
        })
        req = urllib2.Request(url, headers = self.headers, data = data)
        content = self.opener.open(req)
        return content

    def weixin_bind(self, account):
        # url = "https://api.smzdm.com/v1/weixin/bandext?FromUserName=o6HKTjmQ-JPBVtaQ_2gQmlQnWTTQ&key=6a404cd42e1c8daaae40d2bf3b68adf6&f=weixin"
        url = "https://api.smzdm.com/v1/user/weixin/bind?f=weixin"
        data = urllib.urlencode({
            'username' : account['username'],
            'password' : account['password']
        })

        req = urllib2.Request(url, headers = self.weixin_headers, data = data)
        content = self.opener.open(req)
        return content


    # 退出
    def logout(self):
        url = "http://zhiyou.smzdm.com/user/logout"
        req = urllib2.Request(url, headers = self.headers)
        self.opener.open(req)

    # 签到
    def checkin(self):
        user_name = self.account["username"]
        url = "http://zhiyou.smzdm.com/user/checkin/jsonp_checkin"
        req = urllib2.Request(url, headers = self.headers)
        res = self.opener.open(req)
        content = res.read()
        # content_dict = json.loads(content)
        # error_code = content_dict.get("error_code")
        # if error_code == 99:
        #     # 登录失败 或者 已经签到都会有这种情况
        #     error_msg = content_dict.get("error_msg")
        #     self.logger.error(user_name + u"登录失败或已经签到!" + error_msg)
        # else:
        #     # 签到成功的情况
        #     detail_data = content_dict["data"]
        #     check_in_slogan = detail_data.get("slogan")
        #     pattern = re.compile("<.*?>")
        #     log_data = re.sub(pattern, "", check_in_slogan)
        #     self.logger.info(log_data)

    # 查看是否签到
    def is_checkin(self):
        user_name = self.account["username"]
        url = "http://zhiyou.smzdm.com/user/info/jsonp_get_current?"
        req = urllib2.Request(url, headers = self.headers)
        response = self.opener.open(req)
        content = response.read()
        content_dict = json.loads(content)
        smzdm_id = content_dict.get("smzdm_id", 0)
        if smzdm_id == 0:
            # 登录失败
            self.logger.error(user_name + u"登录失败!")
        else:
            # 签到成功的情况
            detail_data = content_dict["checkin"]
            #客户端未签到的情况
            client_has_checkin = content_dict.get("client_has_checkin", False)
            check_in_slogan = detail_data.get("slogan")
            pattern = re.compile("<.*?>")
            log_data = re.sub(pattern, "", check_in_slogan)
            self.logger.info(user_name + " : "+ log_data)


    def start_checkin(self):
        parser = ConfigParser.RawConfigParser()
        parser.read("config/account.ini")
        for user in parser.sections():
            account = dict()
            account['username'] = parser.get(user, 'username')
            account['password'] = parser.get(user, 'password')
            self.login(account)
            self.checkin()
            self.is_checkin()
            self.logout()
if __name__ == '__main__':
    smzdm = Smzdm()
    smzdm.start_checkin()
