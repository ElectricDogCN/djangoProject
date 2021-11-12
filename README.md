# OpenBot-web

用途
--------------------

#### 通过django+自建socket服务，控制OpenBot项目中车的移动，并可以通过webrtc协议，观看车的实时画面。

部署环境
--------------------

### **Linux**：

### 配置前请确认系统内有Python(3.6+)与git(2.10+)

#### 查看Python版本

````
python --version
````

#### 查看Git版本

````
git --version
````

#### 如果git本过低或没有安装：

````
apt update
apt install git
````

非root用户使用sudo：

````
sudo apt update
sudo apt-get install git
````

### Miniconda 安装(清华源,已安装请忽略)

###### 清华源：https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/?C=M&O=A

##### 下载Miniconda：

````
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
````

##### 授予安装脚本执行权限：

````
chmod 777 Miniconda3-latest-Linux-x86_64.sh
````

##### 执行脚本(根据安装指引完成安装，可以初始化conda [yes])：

````
./Miniconda3-latest-Linux-x86_64.sh
````

##### 重新打开Terminal，然后验证Conda命令：

````
conda info
````

#### 使用虚拟环境配置环境 Conda：

###### 创建新虚拟环境,已存在请忽略

````
conda create -n openbot_web_control python=3.9
````

##### 激活虚拟环境：

````
conda activate openbot_web_control
````

### 下载OpenBot-web项目(已下载请忽略)：

#### Github：

````
git clone https://github.com/ElectricDogCN/openbot-web.git
````

#### Gitee：

````
git clone https://gitee.com/ElectricDog/openbot-web.git
````

### 更新项目：
````
git pull
````

### 配置Python依赖：

#### 激活Conda虚拟环境(已激活请忽略)：

````
conda activate openbot_web_control
````

#### 进入OpenBot-web工作目录(已进入请忽略)：

````
cd openbot-web
````

#### 安装依赖：

````
pip install -r requirements.txt
````

### Docker安装（清华源,已安装请忽略）：

````
[清华镜像站安装指南](https://mirrors4.tuna.tsinghua.edu.cn/help/docker-ce/)
````

启动SRS(rtmp-rtc):
------------------

### `1.2.3.4`**替换为服务器公网IP**

````
CANDIDATE=1.2.3.4
````

#### 启动srs

````
docker run --rm --env CANDIDATE=$CANDIDATE -d -p 1935:1935 -p 8080:8080 -p 1985:1985 -p 8000:8000/udp ossrs/srs:4 objs/srs -c conf/rtmp2rtc.conf
````

启动Django
------------------

#### 激活Conda虚拟环境(已激活请忽略)：

````
conda activate openbot_web_control
````

### 进入OpenBot-web工作目录(已进入请忽略)：

````
cd openbot-web
````

#### 前台启动Django：

````
python manage.py runserver 0.0.0.0:8001
````

#### 后台启动并输入到指定日志文件：

````
nohup python manage.py runserver 0.0.0.0:8001 &
````

#### 查看log

````
tail -f -n 30 ./nohup.out
````

#### 查看后台某个进程的pid 替换`"Application Name"`：

````
ps -ef|grep "Application Name"
````

#### 杀死进程：

````
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
https://www.example.cn:8001
````
