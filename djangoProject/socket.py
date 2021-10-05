import socket
import threading


class SocketServer:
    MSGLEN = 512

    def __init__(self, sock=None):
        self.last_data = None

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

    def accept_thread(self):
        print("start control socket server")
        t = threading.Thread(target=self.accept)
        t.start()

    def receive_thread_fun(self):
        while True:
            self.last_data = self.receive()
            print(f'Received: {self.last_data}\r')

    def receive_thread(self):
        t = threading.Thread(target=self.receive_thread_fun())
        t.start()

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
        print(f"socket connect ip:{self.server_socket}")
        try:
            #     self.sock.close()
            self.server_socket.close()
        except:
            print("Could not close all sockets")
        pass


s_server = SocketServer()
