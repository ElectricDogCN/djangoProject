# openbot-web
用途
--------------------
通过django+自建socket服务，控制openbot项目中车的移动，并可以通过webtrc协议，观看车的实时画面。

部署环境
--------------------
Linux：
````
git clone https://github.com/ElectricDogCN/openbot-web.git && cd openbot-web && pip install -r requirements.txt
````

配置前请确认系统内有Python(3.6+)与git
````
$ python --version
Python 3.8.8
$ git --version
git version 2.25.1
````
推荐使用虚拟环境配置环境 例如Conda：
````
conda create -n openbot_web_control python=3.9
conda activate openbot_web_control
````
Miniconda 安装(清华源)：
````
# https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/?C=M&O=A
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 777 Miniconda3-latest-Linux-x86_64.sh
# 根据安装指引完成安装，可以初始化conda [yes]
./Miniconda3-latest-Linux-x86_64.sh
# 重新打开Terminal
conda info
````
Docker 安装（清华源）：
````
[清华镜像站安装指南](https://mirrors4.tuna.tsinghua.edu.cn/help/docker-ce/)
````
部署Srs rtmp-rtc：
````
#替换你的服务器公网ip
CANDIDATE=1.2.3.4
#启动srs
docker run --rm --env CANDIDATE=$CANDIDATE -d -p 1935:1935 -p 8080:8080 -p 1985:1985 -p 8000:8000/udp ossrs/srs:4 objs/srs -c /rtmp2rtc.conf
````
启动Django
------------------
如果已经在openbot-web文件夹内，中则不需要执行第一行`cd openbot-web/`
````
cd openbot-web/
python manage.py runserver 0.0.0.0:8001
````
后台启动
````
cd openbot-web/
#启动程序并输入到指定日志：
nohup python manage.py runserver 0.0.0.0:8001 &

#查看log
cd openbot-web/
tail -f -n 30 ./nohup.out

#查看后台某个进程的pid：
ps -ef|grep "Application Name"

#杀死进程：
kill {pid}
````

使用
-----------------
#### 浏览器访问

##### 本地访问
````
http://0.0.0.0:8001
````
##### 公网/局域网访问 （请自行修改启动端口,并替换公网域名或Ip）
````
http://www.example.cn:8001
````
