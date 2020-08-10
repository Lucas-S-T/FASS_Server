import os
import socket
import ssl
import time

from args import args
from disk_server import FileCache
from render import render_index
from static import disk_servers

ipf = open("template/invalidpath.html", "rb").read()
isf = open("template/invalidserver.html", "rb").read()
index = open("template/index.html", "rb").read()


def process_file(req, pack):
    if pack.path.startswith("/"):
        pack.path = pack.path[1:]

    paths = pack.path.split("/")

    if len(paths) < 3:
        req.send(b"HTTP/1.1 400 Invalid Path\r\nServer: FASS\r\nContent-Length: "+bytes(str(len(ipf)), "utf-8")+b"\r\n\r\n")
        req.send(ipf)
        return

    if pack.path.startswith("local/"):
        get_from_local(req, pack, paths)
        req.close()
        return

    if pack.path.startswith("server/"):
        get_from_disk(req, pack, paths)
        req.close()


def get_from_local(req, pack, paths):

    paths = "/".join(paths[1:])
    if not os.path.isfile("local/"+paths):
        req.send(b'HTTP/1.1 404 Not Found\r\nServer: FASS\r\n\r\n')
        return

    f = open("local/"+paths, "rb")
    req.send(b'HTTP/1.1 200 OK\r\nServer: FASS\r\nContent-Length: '+bytes(str(os.path.getsize("local/"+paths)), "utf-8")+b"\r\n\r\n")
    buf = f.read(4096)
    while len(buf) > 0:
        req.send(buf)
        buf = f.read(4096)


def get_from_disk(req, pack, paths):

    server = paths[1]

    if not server in disk_servers:
        req.send(b"HTTP/1.1 404 Server Not Found\r\nServer: FASS\r\nContent-Length: "+bytes(str(len(isf)), "utf-8")+b"\r\n\r\n")
        req.send(isf)
        return

    realpath = paths[2:]
    paths = "/".join(realpath)

    sv = disk_servers[server]

    if paths in sv.cache:
        sv.cache[paths].expire = int(round(time.time() * 1000)) + (args.cachettl * 1000 * 60)
        req.send(sv.cache[paths].data)

        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((sv.addr, sv.port))
        context = ssl.SSLContext()
        reqd = context.wrap_socket(s)

        if "Range" in pack.headers:

            reqb = b"GET /" + bytes(paths, "utf-8") + b" HTTP/1.1\r\nToken: " + bytes(sv.token, "utf-8") + b"\r\nRange: " + bytes(pack.headers["Range"], "utf-8") + b"\r\n\r\n"

        else:
            reqb = b"GET /" + bytes(paths, "utf-8") + b" HTTP/1.1\r\nToken: " + bytes(sv.token, "utf-8") + b"\r\n\r\n"

        reqd.send(reqb)

        r = reqd.recv(1024)

        hr = r.split(b'\r\n\r\n')

        size = 0

        head = str(hr[0], "utf-8").split("\r\n")

        if head[0].split(" ")[1] == "404":
            req.send(b"HTTP/1.1 400 Invalid Path\r\nServer: FASS\r\nContent-Length: " + bytes(str(len(ipf)), "utf-8") + b"\r\n\r\n")
            req.send(ipf)
            req.close()
            return

        for v in head:
            kv = v.replace(": ", ":").split(":")
            if kv[0] == "Content-Length":
                size = int(kv[1])

        cache = bytearray()
        record = False
        if size != 0 and size <= args.maxcache*1024*1024:
            record = True

        while len(r) > 0:

            if record:
                cache += r

            req.send(r)
            r = reqd.recv(4096)

        if record:
            disk_servers[server].cache[paths] = FileCache(size=size,
                                                          expire=int(round(time.time() * 1000)) + (args.cachettl * 1000 * 60),
                                                          path=paths, data=cache)
