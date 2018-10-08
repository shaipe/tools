#!/bin/bash
# author: shaipe
# url: www.ecdata.cn

if [ "$1" == "mongo" ]
then
    echo "启动mongo"
    mongod -f /etc/mongodb.conf
elif [ "$1" == "mysql" ]
then
    echo "启动mysql"
    cd /usr/local/cellar/mariadb/10.2.12/bin
    ./mysql.server stop
    ./mysql.server start
elif [ "$1" == "postgre" ]
then
    echo "启动postgre"
    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
else
    echo "没有包含第一参数,不能执行脚本"
fi

# docker run -d -p 27017:27017 -v ~/data/mongo:/data/db mongo