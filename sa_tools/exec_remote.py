#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import subprocess,sys,time
from list_servers import List_servers
 
if len(sys.argv) != 3:
    print "[Usage] ./exec_on_remote.py [type] [command]"
    print "exit ..."
    sys.exit()
else:
    type = sys.argv[1] 
    command = sys.argv[2]
 
servers_dict = List_servers.gen_dict(type) 
if not servers_dict:
    print "Sorry, I can not know your type, sir ! exit..."
    sys.exit()
#print servers_dict
 
proc_list = []
# 添加进要处理的子进程
for name in servers_dict.keys():
    p = subprocess.Popen("ssh -n -q -p36000 user_00@%s %s" % (servers_dict[name], command),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
    proc_list.append((name,p))
# 用poll的方式来检测
while True:
    if len(proc_list) == 0:
        break
    for proc in proc_list:
        name = proc[0]
        #print "processing %s...poll is %s" % (name, proc[1].poll())
        #p.wait()
        if proc[1].poll() != None:
            result = proc[1].stdout.read().strip()
            if proc[1].returncode != 0:
                print "exec %s(%s) failed, return code is %s!" % (name, servers_dict[name], proc[1].returncode)
                print "%s >>> %s" % (name,result)
            else:
                print "%s >>> %s" % (name,result)
            #print "remove %s" % name
            proc_list.remove((proc[0],proc[1]))
        else:
            #print "%s is running" % name
            pass
    time.sleep(0.2)
#用阻塞的方式来输出，保证了输出的一致性！
for proc in proc_list:
    name = proc[0]
    #print "processing %s...poll is %s" % (name, proc[1].poll())
    proc[1].wait()
    result = proc[1].stdout.read().strip()
    if proc[1].returncode != 0:
        print "exec %s(%s) failed, return code is %s!" % (name, servers_dict[name], proc[1].returncode)
        print "%s >>> %s" % (name,result)
    else:
        print "%s >>> %s" % (name,result)
print "Done!"
