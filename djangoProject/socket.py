import json
import socket
import threading

# I know that the thread pool needs to be used here, but it only needs No problem if it runs successfully.....
import time


class SocketServer:
    MSGLEN = 512

    def __init__(self, sock=None):
        self.last_data = None
        self.info = {"voltage": "", "rpm": "", "sonar": "", "net": "", "s2c_delay": -1, "s2ob_delay": -1}

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", 19400))
            self.sock.listen()
        else:
            self.sock = sock

    def accept(self):
        while True:
            (conn, addr) = self.sock.accept()
            print(f"socket connect ip:{addr}")
            self.server_socket = conn
            self.receive_thread()

    def accept_thread(self):
        print("start control socket server")
        t = threading.Thread(target=self.accept)
        t.start()

    def receive_thread_fun(self):
        while True:
            if self.receive() == "":
                print(f'Received is null, close this client')
                self.server_socket.close()
                s_server.accept_thread()
                break
            received_msg = {}
            try:
                received_msg = json.loads(self.receive())
            except:
                print(f'Received: {received_msg}\r')
            if "status" in received_msg:
                if received_msg["status"] == "info":
                    self.info["voltage"] = received_msg["voltage"]
                    self.info["rpm"] = received_msg["rpm"]
                    self.info["sonar"] = received_msg["sonar"]
                    self.info["net"] = received_msg["net"]
                    self.info["s2ob_delay"] = int(round(time.time() * 1000)) - int(received_msg["s_time"])
                else:
                    self.last_data = self.receive()

            print(f'Received: {received_msg}\r')

    def receive_thread(self):
        t = threading.Thread(target=self.receive_thread_fun())
        t.start()

    def send(self, msg):
        sent = self.server_socket.send(msg.encode('utf-8'))

    def receive(self):
        chunks = []
        while True:
            # OK, I know, we are not going for efficiency here...
            try:
                chunk = self.server_socket.recv(1)
            except ConnectionResetError:
                break
            chunks.append(chunk)
            if chunk == b'\n' or chunk == b'':
                break
        return b''.join(chunks).decode('utf-8')

    def close(self):
        print(f"socket connect ip:{self.server_socket}")
        try:
            #     self.sock.close()
            self.server_socket.close()
        except:
            print("Could not close all sockets")
        pass


s_server = SocketServer()
