#!/usr/bin/env python
# Monitoring per-process disk I/O activity

import sys, os, time, signal, re , string

class DiskIO:
    def __init__(self, pname=None, pid=None, reads=0, writes=0):
        self.pname = pname
        self.pid = pid
        self.reads = 0
        self.writes = 0

def main():
    argc = len(sys.argv)
    interatime = 0
    maxtry = 100000
    i=0
    if argc != 1 and argc !=2 and argc !=3:
        print "usage: python prethread.py"
        print "usage: python prethread.py count"
        print "usage: python prethread.py count interval"
        sys.exit(0)

    if os.getuid() != 0:
        print "must be run as root"
        sys.exit(0)
    if argc == 2:
        maxtry = string.atoi(sys.argv[1])
    if argc == 3:
        maxtry = string.atoi(sys.argv[1])
        interatime = string.atoi(sys.argv[2])

    signal.signal(signal.SIGINT, signal_handler)
    os.system('echo 1 > /proc/sys/vm/block_dump')
    print "TASK              PID       READ      WRITE"
    while i < maxtry:
        os.system('dmesg -c > /tmp/diskio.log')
        l = []
        f = open('/tmp/diskio.log', 'r')
        line = f.readline()
        while line:
            m = re.match(\
                '^(\S+)\((\d+)\): (READ|WRITE) block (\d+) on (\S+)', line)
            if m != None:
                if not l:
                    l.append(DiskIO(m.group(1), m.group(2)))
                    line = f.readline()
                    continue
                found = False
                for item in l:
                    if item.pid == m.group(2):
                        found = True
                        if m.group(3) == "READ":
                            item.reads = item.reads + 1
                        elif m.group(3) == "WRITE":
                            item.writes = item.writes + 1
                if not found:
                    l.append(DiskIO(m.group(1), m.group(2)))
            line = f.readline()
        time.sleep(1)
        for item in l:
            print "%-10s %10s %10d %10d" % \
                (item.pname, item.pid, item.reads, item.writes)
        print "-----------------------------------------------"
        if interatime >0:
            time.sleep(interatime)
        i= i+1
    os.system("rm -f  /tmp/diskio.log")

def signal_handler(signal, frame):
    os.system('echo 0 > /proc/sys/vm/block_dump')
    os.system("rm -f  /tmp/diskio.log")
    sys.exit(0)

if __name__=="__main__":
    main()
