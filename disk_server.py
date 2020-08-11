import json
import socket
import ssl
import threading
import time
from static import disk_servers


class FileCache:

    def __init__(self, size, expire, data, path):
        self.size = size
        self.expire = expire
        self.data = data
        self.path = path


class DiskServer:

    def process_hb(self):
        while self.run_hb_check:

            if int(round(time.time() * 1000)) - self.last_hb >= 6500 and self.connected:
                print(self.addr, "disconnected: Heartbeat not sent. Preserving cache...")
                self.addr = ""
                self.connected = False

            time.sleep(1)

        pass

    def process_cache(self):
        while self.run_hb_check:
            deletes = []
            for c in self.cache:
                if self.cache[c].expire <= int(round(time.time() * 1000)) and self.connected:
                    deletes.append(c)

            for d in deletes:
                del self.cache[d]
            time.sleep(5)

        pass

    def disconnect(self):
        self.run_hb_check = False
        deletes = []
        for c in self.cache:
            deletes.append(c)

        for d in deletes:
            del self.cache[d]
        del disk_servers[self.id]

    def __init__(self, id, token, addr, port):

        self.id = id
        self.token = token
        self.addr = addr
        self.port = port
        self.last_hb = int(round(time.time() * 1000))
        self.run_hb_check = True
        self.cache = {}
        self.connected = True

        self.disk_free = 0
        self.disk_total = 0
        self.disk_used = 0

        threading.Thread(target=self.process_hb).start()
        threading.Thread(target=self.process_cache).start()

    def update_disk_info(self):

        context = ssl.SSLContext()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.addr, self.port))
            req = context.wrap_socket(s, server_side=False)

            jr = {"op": 13}
            req.send(b"FASS"+bytes(json.dumps(jr), "utf-8"))

            recv = req.recv(1024)

            obj = json.loads(str(recv[4:], "utf-8"))

            self.disk_free = obj["data"]["free"]
            self.disk_used = obj["data"]["used"]
            self.disk_total = obj["data"]["total"]

    def get_file_list(self, path):

        context = ssl.SSLContext()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.addr, self.port))
            req = context.wrap_socket(s, server_side=False)

            jr = {"op": 10, "data": {"path": path}}
            req.send(b"FASS" + bytes(json.dumps(jr), "utf-8"))

            buff = bytearray()

            while True:
                b = req.recv(4096)
                if len(b) > 0:
                    buff += b
                else:
                    break

            obj = json.loads(str(buff[4:], "utf-8"))

            return obj["data"]["files"], obj["data"]["dirs"]
