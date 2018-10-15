#!/bin/bash
# author: shaipe
# url: www.ecdata.cn

echo 'please input need create container name [redis,mongo,mariadb,gitlab]'
for REPOSITORY in `docker images --format "{{.Repository}}"` ;
do 
echo  'image name: ' $REPOSITORY
done

read -p "please input image name:" name

if [ "$name" == "redis" ];
then
echo 'start creating redis a container '

# curl -o redis.conf https://raw.githubusercontent.com/antirez/redis/4.0/redis.conf Mac 下载Redis的默认配置文件
# wget https://raw.githubusercontent.com/antirez/redis/4.0/redis.conf  Centos
# 端口映射 宿主机:容器
# -v ~/docker/redis/data:/data:rw 映射数据目录 rw 为读写
# -v ~/docker/redis/conf/redis.conf:/etc/redis/redis.conf挂载配置文件 :ro 为readonly
# --privileged 给与一些权限
# --name docker-redis 给容器起个名字
# -d redis redis-server /etc/redis/redis.conf deamon 运行 服务使用指定的配置文件
docker run \
-p 6379:6379 \
-v ~/docker/redis/data:/data:rw \
-v ~/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
--privileged=true \
--name docker-redis \
-d redis redis-server /etc/redis/redis.conf 

elif [ "$name" == "mongo" ];
then
echo "start creating mongo a container"
docker run \
--name mongo27017 \
-p 27017:27017 \
-v ~/docker/mongo/data:/data/db \
-d \
mongo

elif [ "$name" == "mariadb" ];
then
echo "start creating mariadb a container";
sudo docker run  --name mariadb3306 \
-p 3306:3306 \
-v ~/docker/mariadb/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=mysql.root \
-d mariadb
else
    echo "没有包含第一参数,不能执行脚本"
fi
