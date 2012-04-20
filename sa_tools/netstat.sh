#!/bin/bash
echo "=============================="
echo "ip number"
echo "=============================="
netstat -antlp|grep "211.103.153.248:80"|grep -v "listen"|awk '{print $5}'|awk -F: '{print $1}'|sort -t. -k1 -k2 -k3 -k4|uniq -c|sort -r|grep -v "*"|sort
netstat -anlp|grep 80|grep tcp|awk '{print $5}'|awk -F: '{print $1}'|sort|uniq -c|sort -nr
echo "=============================="

echo "ssh link"
echo "=============================="
netstat -antlp|awk '{print $5}'|awk -F: '{print $4}'|grep -v "^$"|sort -t. -k1 -k2 -k3 -k4|uniq -c|sort -r|grep -v "*"|sort

echo "============================="
echo "the link status"
echo "+++++++++++++++++++++++++++++"
netstat -n | awk '/^tcp/ {++state[$NF]} END {for(key in state) print key,"\t",state[key]}'
