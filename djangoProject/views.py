from djangoProject import socket as ss

from django.shortcuts import render, HttpResponse
from dwebsocket.decorators import accept_websocket

import uuid
import json

clients = {}  # 创建客户端列表，存储所有在线客户端


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
                        reply = {"code": 0, "msg": "Server onopen.", "uid": userid, "data": ""}
                        client.send(json.dumps(reply).encode("utf-8"))
                    elif msg["code"] == 1:
                        pass
                    elif msg["code"] == 2:
                        pass
                    elif msg["code"] == 101:
                        try:
                            submit_control(msg["data"]["l"], msg["data"]["r"])
                        except:
                            ss.s_server.last_data = None
                            ws_format_send(msg["uid"], 101, "wait connect", "")
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


def submit_control(left, right):
    cmd = '{{driveCmd: {{l:{l}, r:{r} }} }}\n'.format(l=left, r=right)
    if ss.s_server.last_data is None:
        ss.s_server.last_data = ""
        ss.s_server.receive_thread()
    ss.s_server.send(cmd)


def ws_format_send(uid: str, code: int, msg: str, data):
    if uid in clients:
        return ws_format_send_client(clients[uid], uid, code, msg, data)
    return False


def ws_format_send_client(client, uid: str, code: int, msg: str, data):
    msg = {"code": code, "uid": uid, "msg": msg, "data": data}
    client.send(json.dumps(msg).encode("utf-8"))
    return True
