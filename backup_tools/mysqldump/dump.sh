#!/bin/bash
#The script is used to backup databases
#It's used for importing databases base on tables

function usage() {
    echo "Usage:`basename $0` -t [databases] or [tables]"
    echo "`basename $0` -t databases: backup base on databases"
    echo "`basename $0` -t tabless: backup base on tables"
    exit 1
}

if [ $# -ne 2 ];then
    usage
fi

scriptPath=$(cd "$(dirname "$0")"; pwd)
date=`date +%Y%m%d`

echo 'Step 1, import functions'
if [ ! -f ${scriptPath}/lib/function ];then
    echo "${scriptPath}/lib/function not found ..."
    exit 1
fi
. ${scriptPath}/lib/function

echo 'Step 2, Check backup baktmp fold and make it empty'
if [ -d ${scriptPath}/baktmp ];then
    rm ${scriptPath}/baktmp/* -rf
else
    mkdir ${scriptPath}/baktmp
fi

echo 'Step 3, Check mysql command'
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

echo 'Step 4, Check mysqldump command'
if [ -f "/usr/bin/mysqldump" ];then
    mysqldump_exec="/usr/bin/mysqldump"
elif [ -f "/usr/local/bin/mysqldump" ];then
    mysqldump_exec="/usr/local/bin/mysqldump"
elif [ -f "/usr/local/services/mysql/bin/mysqldump" ];then
    mysqldump_exec="/usr/local/services/mysql/bin/mysqldump"
else
    echo 'Mysqldump command not found, please check it ...'
    exit 1
fi

echo 'Step 5, Start to backup databases'
CheckFile ${scriptPath}/conf/cluster.conf
CheckClusterFormat "${scriptPath}"
CheckExcludeFormat "${scriptPath}"

while getopts :t:v OPTION
do
    case $OPTION in
    t)base=$OPTARG
      if [ "$base" = "databases" ];then
        echo "Back it up will base on databases..."
        FindHostAndDB_And_BuildBakList "$mysql_exec" "${scriptPath}"
        StartBakBaseDB "${mysqldump_exec}" "${scriptPath}"
      elif [ "$base" = "tables" ];then
        echo "Back it up will base on tables..."
        FindHostAndDBAndTable_And_BuildBakList "$mysql_exec" "${scriptPath}"
        StartBakBaseTable "${mysqldump_exec}" "${scriptPath}"

      else
          usage
      fi
      ;;
     v)usage
      ;;
     *)usage
      ;;
    esac
done

#FindHostAndDBAndTable_And_BuildBakList "$mysql_exec" "${scriptPath}"
#StartBakBaseTable "${mysqldump_exec}" "${scriptPath}"

echo 'Step 6, use tar tool to package SQL files'
if [ ! -d ${scriptPath}/db_backup ];then
    mkdir ${scriptPath}/db_backup
fi
cd ${scriptPath}
tar cjf ./db_backup/${date}.tar.bz2 ./baktmp/*

echo 'Step 7, Remove backup files ten days ago and keep ten parts backup files at least!'
CheckBackup "${scriptPath}" "db_backup"

echo 'Well done...'
