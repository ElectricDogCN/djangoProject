import json
import socket
import threading

# I know that the thread pool needs to be used here, but it only needs No problem if it runs successfully.....
import time


class SocketServer:
    MSGLEN = 512

    def __init__(self, sock=None):
        self.last_data = None
        self.info = {"voltage": "-1", "rpm": "-1", "sonar": "-1", "net": "-1", "s2c_delay": -1, "s2ob_delay": -1}

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
            received_raw = self.receive()
            if received_raw == "":
                print(f'Received is null, close this client')
                self.server_socket.close()
                s_server.accept_thread()
                break
            received_msg = {}
            try:
                received_msg = json.loads(self.receive())
            except:
                print(f'Received1: {received_raw}\r')
                continue
            if "status" in received_msg:
                if received_msg["status"] == "info":
                    try:
                        battery = round((float(received_msg["voltage"].split(" ")[0]) - 9) / 3.4, 3)
                        battery = 1.0 if battery > 1.0 else battery
                        battery = 0.0 if battery < 0 else battery
                        self.info["voltage"] = str(battery * 100)
                    except:
                        self.info["voltage"] = "-1"

                    TIRE_RADIUS = 7
                    try:
                        rpm = received_msg["rpm"]
                        speed = (float(rpm.split(",")[0]) / 60.0 + float(rpm.split(",")[1]) / 60.0) / 2 * TIRE_RADIUS
                        self.info["rpm"] = str(round(speed, 2))
                    except:
                        self.info["rpm"] = "-1"

                    self.info["sonar"] = received_msg["sonar"]
                    self.info["net"] = received_msg["net"]
                    self.info["s2ob_delay"] = int(round(time.time() * 1000)) - int(received_msg["s_time"])
                else:
                    self.last_data = received_raw

            print(f'Received2: {received_raw}\r')

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
                self.info = {"voltage": "-1", "rpm": "-1,-1", "sonar": "-1", "net": "-1", "s2c_delay": -1,
                             "s2ob_delay": -1}
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
