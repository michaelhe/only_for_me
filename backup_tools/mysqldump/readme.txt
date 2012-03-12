The project is used to backup databases base on tables!!!!


Backup script file:

                   dump.sh -> execute the shell script to backup databases
                              Usage:
                              ./dump.sh -t [databases] or [tables]
                              ./dump.sh -t databases: backup base on databases
                              ./dump.sh -t tabless: backup base on tables

Restore script file:

                   load.sh -> execute the shell script to restore databases
                              Usage:
                              ./load.sh -t [databases] or [tables]
                              ./load.sh -t databases: restore base on databases
                              ./load.sh -t tabless: restore base on tables
                              if you point "-t databases", the script will read 
                              the file "./baktmp/BakBaseDB.list" to restore;
                              if you point "-t tables", the script will read 
                              the file "./baktmp/BakBaseTable.list" to restore.
        


Include folds as follow:

                    baktmp -> backup databases's location last time

                 db_backup -> package all backup databases folds

                      conf -> include configuration files:cluster.conf, exclude.conf

                       lib -> include function file




Then fold was named conf include files as follow:

              ./conf/cluster.conf -> mysql servers's hostname,ip,port,username,password and database-prefix
                              usage:
                              hostname ip port username password database-prefix[ database-prefix ...] 

       ./conf/exclude.conf -> please write databases or tables to this file which you don't want to backup,
                              one table a line.
                              usage:
                              dbhostname dbname                                               ->means  exclude full database
                              dbhostname dbname tablename01[ tablename02 tablename03 ...]     ->means  exclude some specific tables belong to database

                  ./lib/function -> this file include some functions
