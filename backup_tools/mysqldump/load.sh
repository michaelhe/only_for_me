#!/bin/bash
#The script is used for loading database
#
if [ $# -ne 2 ];then
    echo "Parameter error!"
    usage
fi

if [ "$1" != "-t" ];then
    echo "Parameter error!"
    usage
    exit 1
fi

scriptPath=$(cd "$(dirname "$0")"; pwd)

function usage() {
    echo "Usage:`basename $0` -t [databases] or [tables]"
    echo "`basename $0` -t databases: load base on databases"
    echo "`basename $0` -t tabless: load base on tables"
    exit 1
}

function LoadBaseDB() {
#   $1 means ${scriptPath}
#   $2 means ${mysql_exec}
while read dbhostname dbip dbport dbusername dbpassword dbname
do
    ${2} $dbip $dbport $dbusername $dbpassword $dbname < ${1}/baktmp/${dbhostname}/${dbname}.sql    
done < ${1}/baktmp/BakBaseDB.list
}

function LoadBaseTable() {
#   $1 means ${scriptPath}
#   $2 means ${mysql_exec}
while read dbhostname dbip dbport dbusername dbpassword dbname dbtable
do
    ${2} $dbip $dbport $dbusername $dbpassword $dbname < ${1}/baktmp/${dbhostname}/${dbname}/${dbtable}.sql
done < ${1}/baktmp/BakBaseTable.list
}





echo 'Step 1, Check mysql command'
if [ -f "/usr/bin/mysql" ];then
    mysql_exec="/usr/bin/mysql"
elif [ -f "/usr/local/bin/mysql" ];then
    mysql_exec="/usr/local/bin/mysql"
elif [ -f "/usr/local/services/mysql/bin/mysql" ];then
    mysql_exec="/usr/local/services/mysql/bin/mysql"
else
    echo 'Mysql command not found, please check it ...'
    exit 1
fi


echo 'Step 2, Start loading databases......'
if [ "$2" = "databases" ];then
    echo "It will loading base database..."
    LoadBaseDB "${scriptPath}" "${mysql_exec}"
elif [ "$2" = "tables" ];then
    echo "It will loading base table..."
    LoadBaseTable "${scriptPath}" "${mysql_exec}"
else
    echo "Parameter error!"
    usage
fi


echo 'Load well done!!!'
