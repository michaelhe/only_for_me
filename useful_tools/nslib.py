#!/usr/bin/env python
# encoding: utf-8

import datetime
import urllib2,cookielib
from urllib import urlencode
from BeautifulSoup import BeautifulStoneSoup

class SpiderRequest:

    def __init__(self):
        #_proxy = urllib2.ProxyHandler({'http':'http://192.168.1.59:8087'})
        #self._opener = urllib2.build_opener(_cookie,urllib2.HTTPHandler)
        self.cookie = cookielib.CookieJar()
        _cookie = urllib2.HTTPCookieProcessor(self.cookie)
        _opener = urllib2.build_opener(_cookie,urllib2.HTTPHandler)
        urllib2.install_opener(_opener)
        
    def request(self, url, data=None):
        if data:
            postdata = urlencode(data)
            req = urllib2.Request(url, data = postdata)
        else:
            req = urllib2.Request(url)
        return urllib2.urlopen(req).read().strip()

class NsLib(SpiderRequest):
    
    def login(self, sn, pwd):
        url = 'http://opac.nslib.cn/MyLibrary/readerLogin.jsp'
        url_params = urlencode({"username":sn, "password":pwd})
        final_url = url + "?" + url_params
        #print final_url
        response = self.request(final_url)
        xmldoc = BeautifulStoneSoup(response)
        if xmldoc.find('message').text == 'OK':
            return True
        else:
            return False

    def logout(self):
        url = 'http://opac.nslib.cn/MyLibrary/GetOutLib.jsp'
        self.request(url)

    def get_readerno(self):
        return self.cookie._cookies['opac.nslib.cn']['/']['recordno'].value
    
    def get_list(self):
        url = 'http://opac.nslib.cn/MyLibrary/getloanlist.jsp?readerno=%s' % self.get_readerno()
        xmlstring =  self.request(url)
        xmldoc = BeautifulStoneSoup(xmlstring)
        for item in  xmldoc.findAll('meta'):
            timestr = item.find('returndate').text
            year = timestr[0:4]
            month = timestr[4:6]
            day = timestr[6:8]
            print "%s-%s-%s" % (year, month, day)
            returndate = datetime.date(year, month, day)

if __name__ == '__main__':
    nslib = NsLib()
    print nslib.login('0440061025408','19880406')
    nslib.get_list()
    nslib.logout()

    nslib2 = NsLib()
    print nslib2.login('0440061027527','19860505')
    nslib2.get_list()
    nslib2.logout()
    
