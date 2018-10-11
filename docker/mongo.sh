#!/bin/bash
# author: shaipe
# url: www.ecdata.cn

if [ "$1" == "mongo" ]
then
    echo "启动mongo"
    docker run -d -p 27017:27017 -v ~/data/mongo:/data/db mongo
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

sudo docker run --detach \
    --hostname 192.168.4.97 \
    --publish 443:443 --publish 80:80 --publish 222:22 \
    --name gitlab-ce \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:11.2.3-ce.0

sudo  docker run --detach \
--publish 22443:443 --publish 2280:80  --publish 2222:22 \
--name gitlab \
--restart always \
--volume /srv/gitlab/config:/etc/gitlab \
--volume /srv/gitlab/logs:/var/log/gitlab \
--volume /srv/gitlab/data:/var/opt/gitlab \
gitlab/gitlab-ce:latest


sudo docker run --detach \
    -p 443:443 -p 80:80 -p222:22 \
    --name gitlab-ce \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:11.2.3-ce.0

docker run --name='gitlab-ce' -d -p 11122:22 -p 80:80 --restart always --volume /srv/gitlab/config:/etc/gitlab --volume /srv/gitlab/logs:/var/log/gitlab --volume /srv/gitlab/data:/var/opt/gitlab/ gitlab/gitlab-ce:11.2.3-ce.0


gitlab-rake gitlab:backup:restore BACKUP=1539076749_2018_10_09_11.2.3_gitlab_backup.tar


# 万向轮: 8*8
# 后轮: 10 * 6
# docker run -d -p 27017:27017 -v ~/data/mongo:/data/db mongo