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
import cookielib

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

        self.app_url = "https://api.smzdm.com/v1/user/checkin"
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
            # "Cookie" : " __jsluid=113fe510ed4b4c950c5e46b3fe321626"
        }

        self.app_header = {
            "User-agent" : " smzdm_android_V7.3 rv:345 (MX4 Pro;Android5.1.1;zh)smzdmapp",
            # "Cookie" : " smzdm_device=android;smzdm_user_source=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG;smzdm_version=7.3;",
            # "Cookie" : " pid=866002025010397;partner_id=0;partner_id=0;device_id=c34f3719f4c71385cfe091758b126a8f;imei=3427b9e3efe644cacf6ff9c0117711e0;partner_name=wandoujia;mac=38:bc:1a:e2:a2:90;smzdm_id=7860525979;login=1;device_push=1;network=wifi;device_smzdm_version=7.3;device_smzdm_version_code=345;device_s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG;device_type=MeizuMX4 Pro;device_system_version=5.1.1;device_smzdm=android;",
            "Content-Type" : " application/x-www-form-urlencoded; charset=UTF-8",
            "Host" : " api.smzdm.com",
        }

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

    def app_login(self, account):
        user_name = account["username"]
        password = account["password"]
        app_login_url = "https://h5.smzdm.com/user/login/ajax_7_0_check"
        post_data = "username={0}&password={1}&is_third=0&geetest_challenge=&geetest_validate=&geetest_seccode=".format(user_name, password)
        app_header = {
            "Host" : " h5.smzdm.com",
            "Connection" : " keep-alive",
            "Accept" : " application/json",
            "Origin" : " https://h5.smzdm.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; MX4 Pro Build/LMY48W) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.2214.121 Mobile Safari/537.36 {smzdm_android_V7.3 rv:345 (MX4 Pro;Android5.1.1;zh)smzdmapp}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://h5.smzdm.com/user/login/login_7_0/0",
            # "Cookie" : "partner_id=0; partner_name=wandoujia; smzdm_id=; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; partner_id=0; partner_name=wandoujia; smzdm_id=7860525979; smzdm_user_source=784742AE5BDB6C72DE4163C36CEF4424; PHPSESSID=3jvbg71629noknu1gc84gr0hs3; __jsluid=cfd73a528efc46019ce359b36118b4bb; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1475941209; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1476378465; user=laihongchang%7C7860525979; smzdm_wordpress_360d4e510beef4fe51293184b8908074=sawean%7C1480784185%7C9378c09b7d66165e2dceb285ff047f13; smzdm_wordpress_logged_in_360d4e510beef4fe51293184b8908074=sawean%7C1480784185%7C3019debfc82b386b05c81aa8c79e5f82; user-role-smzdm=subscriber; sess=; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; from=android; v=345; s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; _dc_gtm_UA-27058866-1=1; _ga=GA1.2.1725864596.1469037084",
        }

        #声明一个CookieJar对象实例来保存cookie
        cookie = cookielib.CookieJar()
        #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler=urllib2.HTTPCookieProcessor(cookie)
        #通过handler来构建opener
        opener = urllib2.build_opener(handler)



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

    def app_checkin(self):
        user_name = self.account["username"]
        post_data = "sk=CUbJSyy13E4CYTGNoJ7tGdgGsw7l5fVfme2KIr%2BeSMU%3D&token=5782ff1812d0e756294&captcha=&f=android&s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG&weixin=1&v=345&"
        url = self.app_url
        # req = requests.post(url, data=post_data, headers=self.app_header)
        # res = req.read()
        req = urllib2.Request(url, headers=self.app_header ,data=post_data)
        res = self.opener.open(req)
        content = res.read()
        content_dict = json.loads(content)
        error_code = content_dict.get("error_code")
        error_msg = content_dict.get("error_msg")
        self.logger.error(user_name + error_msg)
        # 签到之后可以抽奖
        self.app_lottery()

    def app_lottery(self):
        #TODO 下一步，需要会构造cookies和referer。 里面多了几个参数，d=SQfD%2FfF%2FdYUUdxOjXVt6IaTReRM2p4dPiYK0KHEyuhC9HwFLwi715A%3D%3D; t=846d09defd4643747eef87eabd2f1f22; s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG;
        user_name = self.account["username"]
        app_lottery_headers = {
            "Host":" h5.smzdm.com",
            "Connection" : " keep-alive",
            "Content-Length" : " 0",
            "Accept" : " application/json",
            "Origin" : " https://h5.smzdm.com",
            "X-Requested-With":" XMLHttpRequest",
            # "User-agent" : " smzdm_android_V7.3 rv:345 (MX4 Pro;Android5.1.1;zh)smzdmapp",
            "Content-Type": "text/html; charset=utf-8",
            "User-Agent" : " Mozilla/5.0 (Linux; Android 5.1.1; MX4 Pro Build/LMY48W) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.2214.121 Mobile Safari/537.36 {smzdm_android_V7.3 rv:345 (MX4 Pro;Android5.1.1;zh)smzdmapp}",
            # "Referer" : " https://h5.smzdm.com/user/lottery/checkin?d=0WL7dk6cWYED4jY5scvN%2Bw3gerW3kVusT1fkhvqPq4P8Htic3OP1IQ%3D%3D&t=560dad0a7079a3eb483d1dbacf543979&f=android&s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG&add_point=&displaymode=0&v=345",
            # "Accept-Encoding" : " gzip, deflate",
            "Accept-Language" : " zh-CN,en-US;q=0.8",
            # "Cookie": "device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; partner_id=0; partner_name=wandoujia; smzdm_id=6718161613; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; partner_id=0; partner_name=wandoujia; smzdm_id=6718161613; smzdm_user_source=784742AE5BDB6C72DE4163C36CEF4424; PHPSESSID=3jvbg71629noknu1gc84gr0hs3; __jsluid=cfd73a528efc46019ce359b36118b4bb; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1475941209; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1476378465; user=laihongchang%7C7860525979; _ga=GA1.2.1725864596.1469037084; smzdm_wordpress_360d4e510beef4fe51293184b8908074=sawean%7C1480784350%7C6bdf1626b79407781a0160263c95e0cd; smzdm_wordpress_logged_in_360d4e510beef4fe51293184b8908074=sawean%7C1480784350%7C777115efc4f0bc33bdf581209569914f; user-role-smzdm=subscriber; sess=MTJlNzN8MTQ4MDc4NDM1MHw2NzE4MTYxNjEzfGZmNWZiMmJiMzJhZmM2Yjg4OTk2ODczMWI3ZGU3YTA3; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; from=android; v=345; d=0WL7dk6cWYED4jY5scvN%2Bw3gerW3kVusT1fkhvqPq4P8Htic3OP1IQ%3D%3D; t=560dad0a7079a3eb483d1dbacf543979; s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG"
            # "Referer" : "https://h5.smzdm.com/user/lottery/checkin?d=SQfD%2FfF%2FdYUUdxOjXVt6IaTReRM2p4dPiYK0KHEyuhC9HwFLwi715A%3D%3D&t=846d09defd4643747eef87eabd2f1f22&f=android&s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG&add_point=20&displaymode=0&v=345",
            # "Referer" : "https://h5.smzdm.com/user/lottery/checkin?d=0WL7dk6cWYED4jY5scvN%2Bw3gerW3kVusT1fkhvqPq4P8Htic3OP1IQ%3D%3D&t=560dad0a7079a3eb483d1dbacf543979&f=android&s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG&add_point=&displaymode=0&v=345",
            "Cookie" : "device_id=nKrch6wzKbD0yhjQMQZXpcILsr5rGwG; partner_id=0; partner_name=wandoujia; smzdm_id=7860525979; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; partner_id=0; partner_name=wandoujia; smzdm_id=7860525979; smzdm_user_source=784742AE5BDB6C72DE4163C36CEF4424; PHPSESSID=3jvbg71629noknu1gc84gr0hs3; __jsluid=cfd73a528efc46019ce359b36118b4bb; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1475941209; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1476378465; _ga=GA1.2.1725864596.1469037084; smzdm_wordpress_360d4e510beef4fe51293184b8908074=laihongchang%7C1480697269%7C12ec24e92b0e1c0b77f9aa1af5a6be04; smzdm_wordpress_logged_in_360d4e510beef4fe51293184b8908074=laihongchang%7C1480697269%7C5326e245e45e3d882bedc63acf5aeced; user-role-smzdm=subscriber; user=laihongchang%7C7860525979; from=android; v=345; d=SQfD%2FfF%2FdYUUdxOjXVt6IaTReRM2p4dPiYK0KHEyuhC9HwFLwi715A%3D%3D; t=846d09defd4643747eef87eabd2f1f22; s=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG; sess=; device_id=nKrwch6wzKbD0yhjQMQZXpcILsr5rGwG"
        }
        post_data = None
        lot_url = "https://h5.smzdm.com/user/lottery/ajax_draw"
        #声明一个CookieJar对象实例来保存cookie
        cookie = cookielib.CookieJar()
        #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler=urllib2.HTTPCookieProcessor(cookie)
        #通过handler来构建opener
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(lot_url, headers=app_lottery_headers, data = post_data)
        # res = self.opener.open(req)
        res = opener.open(req)
        # cookie = self.cookies
        content = res.read()
        content_dict = json.loads(content)
        error_code = content_dict.get("error_code")
        error_msg = content_dict.get("error_msg")
        self.logger.error(user_name + error_msg)

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
            self.account = account
            # self.login(account)
            # self.checkin()
            self.app_checkin()
            # self.app_lottery()
            self.is_checkin()
            self.logout()
if __name__ == '__main__':
    smzdm = Smzdm()
    smzdm.start_checkin()
