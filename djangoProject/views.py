import math
import time

from djangoProject import socket as ss

from django.shortcuts import render, HttpResponse
from dwebsocket.decorators import accept_websocket
from apscheduler.schedulers.background import BackgroundScheduler

import uuid
import json

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
clients = {}  # 创建客户端列表，存储所有在线客户端


def my_job(param1, param2):  # 任务
    print(param1, param2)


# 允许接受ws请求
@accept_websocket
def link(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid1())
        # 判断是否有客户端发来消息，若有则进行处理，若发来“test”表示客户端与服务器建立链接成功
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                client = request.websocket
                msg = {}
                try:
                    msg = json.loads(str(message, encoding="utf-8"))
                except:
                    client.send(('{"msg":"Unknown Data ,' + userid + '"}').encode("utf-8"))
                    request.close()
                    break

                if "code" in msg:
                    # code  == 0  Client onOpen
                    if msg["code"] == 0:
                        reply = {"code": 0, "msg": "Server onopen.", "uid": userid,
                                 "s_time": int(round(time.time() * 1000)), "data": ""}
                        client.send(json.dumps(reply).encode("utf-8"))

                    elif msg["code"] == 1:
                        pass
                    elif msg["code"] == 2:
                        pass
                    elif msg["code"] == 100:
                        submit('{command}\n'.format(command=msg["data"]))
                    # 收到101是控制指令，返回控制状态101成功 1001失败
                    elif msg["code"] == 101:
                        try:
                            x, y = msg["data"]["l"] * 100, msg["data"]["r"] * 100
                            distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 100
                            distance = round(distance, 2) if math.fabs(distance) > 0.2 else 0.0
                            angle = calculation_angle([0, 0, x, y], [0, 0, math.fabs(x), 0])
                            print(angle, distance)
                            # Right
                            left, right = 0, 0
                            if angle > 315 or angle < 45:
                                left = distance
                                right = -distance
                            # Left
                            elif 135 < angle < 225:
                                left = -distance
                                right = distance
                            # forward
                            elif 45 < angle < 135:
                                left = distance
                                right = distance
                            # backward
                            elif 225 < angle < 315:
                                left = -distance
                                right = -distance
                            submit_control(left, right)
                            ws_format_send(msg["uid"], 101, "send successful",
                                           [left, right, round(msg["data"]["l"], 2), round(msg["data"]["r"], 2)])
                        except:
                            ss.s_server.last_data = None
                            ws_format_send(msg["uid"], 1001, "wait connect", "")
                    # 102 获取服务器时间 返回102成功
                    elif msg["code"] == 102:
                        try:
                            submit('{{command: {command},s_time:{s_time} }}\n'.format(
                                command="CalculationDelay",
                                s_time=str(int(round(time.time() * 1000)))))
                        except:
                            ss.s_server.info["s2ob_delay"] = -1
                        ws_format_send(msg["uid"], 102, "server time", "")
                    # 103 计算时延并返回车辆信息 控制端发送102中获取的时间戳，返回103计算成功
                    elif msg["code"] == 103:
                        s2c_delay = int(round(time.time() * 1000)) - int(msg["s_time"]) + 1
                        ss.s_server.info["s2c_delay"] = s2c_delay
                        ws_format_send(msg["uid"], 103, "Calculation delay & get info", ss.s_server.info)

                    else:
                        print("msg:" + json.dumps(msg))
                else:
                    client.send(('{"msg":"Unknown Data ,' + userid + '"}').encode("utf-8"))
                    break

                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                clients[userid] = client


def send(request):
    # 获取消息
    msg = request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    for client in clients:
        clients[client].send(msg.encode('utf-8'))
    return HttpResponse({"msg": "success"})


def index(request):
    return render(request, "control.html")


def as_views(request):
    left = request.GET.get("l", "0")
    right = request.GET.get("r", "0")
    try:
        submit_control(left, right)
    except:
        ss.s_server.last_data = None
        return HttpResponse("wait connect")
    return HttpResponse(ss.s_server.last_data)


last_left, last_right = -1, -1


def submit_control(left, right):
    global last_left, last_right
    cmd = '{{driveCmd: {{l:{l}, r:{r} }} }}\n'.format(l=left, r=right)
    if last_left != left or last_right != right:
        submit(cmd)
        last_left, last_right = left, right


def submit(cmd):
    if ss.s_server.last_data is None:
        ss.s_server.last_data = ""
        ss.s_server.receive_thread()
    ss.s_server.send(cmd)


def ws_format_send(uid: str, code: int, msg: str, data):
    if uid in clients:
        return ws_format_send_client(clients[uid], uid, code, msg, data)
    return False


def ws_format_send_client(client, uid: str, code: int, msg: str, data):
    msg = {"code": code, "uid": uid, "msg": msg, "s_time": int(round(time.time() * 1000)), "data": data}
    client.send(json.dumps(msg).encode("utf-8"))
    return True


def calculation_angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)
    if angle1 * angle2 >= 0:
        included_angle = abs(angle1 - angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    if angle1 < 0:
        included_angle = 360 - included_angle
    return included_angle
