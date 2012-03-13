#!/usr/bin/env python
# encoding: utf-8
import time
import sys
import signal
import urllib
import pycurl
import StringIO
import threading
from Queue import Queue

cdn_prefix = 'http://imgcache.my.com/flash'
version_file = 'flash_vc_version.list'

def get_http_code(url):
    doc = urllib.urlopen(url)
    return doc.code

def producer(queue):
    fp = open(version_file, 'r')
    for line in fp:
        filename = line.split(":")[0].strip()
        version = line.split(":")[1].strip()
        queue.put((filename,version))
    fp.close()
    print "put url ok!"

class Checker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.q = queue

    def run(self):
        while not ThreadCtrl.thread_flag:
            if self.q.empty():
                print "going to be done! less than 25"
                self.stop()
                break
            (filename,version) = self.q.get()
            url = cdn_prefix+'/'+version+'/'+filename
            code = get_http_code(url)
            if code == 200:
                print "detecting %s(%s) \033[0;32;1mSuccess...\033[0m" % (filename, version)
            else:
                print "\033[0;31;1m***********************  WARNINIG  *****************************\033[0m"
                print "\033[0;31;1mdetecting %s(%s) ... HTTP CODE is %s\033[0m" % (filename, version, code)
                self.stop()
            self.q.task_done()

    def stop(self):
        ThreadCtrl.thread_flag = True

class ThreadCtrl:
    thread_flag = False

if __name__ == "__main__":
    queue = Queue()
    producer(queue)
    threads = []
    for i in range(25):
        checker = Checker(queue)
        #checker.setDaemon(True)
        threads.append(checker)
        checker.start()
    print "checking cdn url started..."
    while len(threads) > 0:
        try:
            for t in threads:
                if t is not None and t.isAlive():
                    t.join(1)
                elif not t.isAlive():
                    threads.remove(t)
            #threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print "Crtl-c received! kill to thread..."
            for t in threads:
                t.stop()
    #time.sleep(5)
    #ThreadCtrl.stop_thread()
    #queue.join()
    print "Done!"    

