#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# needed python 2.7.2
# author : michael <michaelhe@vanchu.net>
# date   : 2011-11-10
# modified : michael <michaelhe@vanchu.net> @ 2012-02-21

"this is a module for sending emails"
import os
import sys
import smtplib
import time
from email.Message import Message
from email.MIMEMultipart import MIMEMultipart  
from email.MIMEBase import MIMEBase  
from email.MIMEText import MIMEText 
from email.Header import Header 
from email import Encoders


class Send_emails:
    """define smtp server infomation"""
    def __init__(self):
        self._mail_host = 'smtp.qq.com'
        self._mail_user = '******@qq.com'
        self._mail_pass = '******'
        self.message = MIMEMultipart()

    def set_receiver(self, receivers):
        user_list = receivers.strip().split(',')
        self._mail_list = []
        self._to_list = []
        for name in user_list:
            self._mail_list.append(name+'@vanchu.net')
            self._to_list.append(self.encode_str(name) + '<' + name + '@vanchu.net>')

    
    def set_subject(self, subject):
        self.message['subject'] = self.encode_str(subject)
        self.message['from'] = self.encode_str('凡趣监控') + '<' + self._mail_user + '>'        
        self.message['to'] = ";".join(self._to_list)

    def add_text(self, text):
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))

    def add_attachment(self, filename):
        part = MIMEBase('application', "octet-stream") 
        att_file = open(filename, 'rb')
        part.set_payload( att_file.read() ) 
        att_file.close()
        Encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % self.encode_str(os.path.basename(filename)))
        self.message.attach(part) 
        
    def send(self):
        try:
            s = smtplib.SMTP(self._mail_host)
            #s = smtplib.SMTP_SSL(self._mail_host)
            #s.ehlo()
            #s.starttls()
            s.login(self._mail_user, self._mail_pass)
            s.sendmail(self._mail_user, self._mail_list, self.message.as_string())
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False

    def encode_str(self, string):
        return Header(string, 'utf-8').encode()

if __name__ == '__main__':
    mail = Send_emails()
    mail.set_receiver( 'michaelhe' )
    mail.set_subject( '[凡趣监控]' + time.strftime('%F,%T') )
    mail.add_text('你好，世界@！@')
    mail.add_attachment( './class_email.py' )
    print mail.send()
    #print mail.message
