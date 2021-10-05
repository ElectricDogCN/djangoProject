# djangoProject (会改名的....)
用途
--------------------
通过django+自建socket服务，控制openbot项目中小车的移动，并可以通过webtrc协议，观看车的实时画面。

部署环境
--------------------
Linux：
````
git clone https://github.com/ElectricDogCN/djangoProject.git && cd djangoProject && pip install -r requirements.txt
````

配置前请确认系统内有python(3.6+)与git
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

启动Django
------------------
如果已经在djangoProject文件夹内，中则不需要执行第一行cd djangoProject/
````
cd djangoProject/
python manage.py runserver 0.0.0.0:8001
````
后台启动
````
cd djangoProject/
#启动程序并输入到指定日志：
nohup python manage.py runserver 0.0.0.0:8001 > ./openbot-web.log 2&>1 &

#查看log
cd djangoProject/
tail -f -n 30 ./openbot-web.log

#查看后台某个进程的pid：
ps -ef|grep "Application Name"

#杀死进程：
kill -9 {pid}
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
