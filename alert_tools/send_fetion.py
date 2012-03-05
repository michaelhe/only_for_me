#!/usr/bin/env python
# encoding: utf-8

from urllib import urlencode
import urllib2,cookielib,re
import sys

class Fetion:
    
    def __init__(self,phone='*****',passwd='******'):
        self._phone = phone
        self._passwd = passwd
        self._status = False
        self._cookie_handler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        url = 'http://f.10086.cn/im/login/login.action'
        self.http_request(url)
    
    def http_request(self, url, data=None):
        opener = urllib2.build_opener(self._cookie_handler)
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Connection':'keep-alive'
        }
        request = urllib2.Request(url, data)
        response = opener.open(request)
        return response.read()

    def login(self):
        url = 'http://f.10086.cn/im/login/inputpasssubmit1.action'
        data = {'pass':self._passwd , 'loginstatus':1 , 'm':self._phone}
        postdata = urlencode(data)
        response = self.http_request(url, postdata)
        t = self._get_t_value(response)
        if t:
            self._status = True
            self._t = t
            return True
        else:
            return False

    def logout(self):
        url = "http://f.10086.cn/im/index/logoutsubmit.action?t="+self._t
        self.http_request(url)
        
    def sendMsg(self, phone, msg):
        if phone == self._phone:
            self.sendMsgToMyself(msg)
        else:
            self.sendMsgToFriend(phone, msg)

    def sendMsgToMyself(self, msg):
        url = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
        data = {'msg':msg}
        postdata = urlencode(data)
        response = self.http_request(url, postdata)
        if "发送成功" in response:
            print "send fetion succeed!"
        else:
            print "send fetion failed!"
            
    def sendMsgToFriend(self, phone, msg):
        touserid = self.get_touserid(phone)
        url = 'http://f.10086.cn/im/chat/sendMsg.action?touserid='+touserid
        data = {'backUrl':'','msg':msg,'touchTextLength':'','touchTitle':''}
        postdata = urlencode(data)
        response = self.http_request(url, postdata)
        if "发送消息成功" in response:
            print "send fetion succeed!"
        else:
            print "send fetion failed!"         
        
    
    def get_touserid(self,phone):
        url = 'http://f.10086.cn/im/index/searchOtherInfoList.action?t='+self._t
        data = {'searchText':phone}
        postdata = urlencode(data)
        response = self.http_request(url, postdata)
        return self._get_touserid(response)
    
    def _get_t_value(self, response):
        re_pattern = "ontimer=\"(.*?)\""
        string = re.findall(re_pattern,response)
        return string[0][string[0].index('t=')+2:]

    def _get_touserid(self, response):
        re_pattern = "href=\"/im/chat/(.*?)\""
        string = re.findall(re_pattern,response)
        if string:
            return string[0][string[0].index('id=')+3:string[0].index('&amp')]
        else:
            return False
        
       
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./send_fetion.py [phone] [msg]"
        sys.exit()
    else:
        tophone = sys.argv[1]
        message = sys.argv[2] 
        fetion = Fetion()
        if fetion.login():
            fetion.sendMsg(tophone, message)
        fetion.logout()
