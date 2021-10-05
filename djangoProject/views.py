from django.http import HttpResponse
import json
import socket
import threading

from django.shortcuts import render

from djangoProject import socket as ss


class ServerSocket:
    MSGLEN = 512

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", 19400))
            self.sock.listen()

        else:
            self.sock = sock

    def accept(self):
        (conn, addr) = self.sock.accept()
        self.server_socket = conn

    def send(self, msg):
        sent = self.server_socket.send(msg.encode('utf-8'))

    def receive(self):
        chunks = []
        while True:
            # OK, I know, we are not going for efficiency here...
            chunk = self.server_socket.recv(1)

            chunks.append(chunk)
            if chunk == b'\n' or chunk == b'':
                break
        return b''.join(chunks).decode('utf-8')

    def close(self):
        # try:
        #     self.sock.close()
        #     self.server_socket.close()
        # except:
        #     print("Could not close all sockets")
        pass


s_server: ServerSocket = None


def run_receiver():
    print("start control socket server")
    global s_server
    s_server = ServerSocket()
    s_server.accept()
    while True:
        data = s_server.receive()
        print(f'Received: {data}\r')

        if data in ["", None]:
            return


def index(request):
    return render(request, "control.html")


def as_views(request):
    left = request.GET.get("l", "0")
    right = request.GET.get("r", "0")
    cmd = '{{driveCmd: {{l:{l}, r:{r} }} }}\n'.format(l=left, r=right)
    try:
        if ss.s_server.last_data is None:
            ss.s_server.last_data = ""
            ss.s_server.receive_thread()
        ss.s_server.send(cmd)
    except:
        ss.s_server.last_data = None
        return HttpResponse("wait connect")
    return HttpResponse(ss.s_server.last_data)
