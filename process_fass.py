import json
import socket
import ssl
import time

import static
from args import args
from disk_server import DiskServer
from static import disk_servers

server_token = "1535cc8207de4b32bfec79679a2246c1"


def process_fass(req, addr, obj):

    if obj["op"] == 3:
        fass_identify(req, addr, obj)
        req.close()
        return

    if obj["op"] == 1:
        fass_beat(req, addr, obj)
        req.close()
        return

    if obj["op"] == 12:
        fass_bye(req, addr, obj)
        req.close()
        return


def fass_bye(req, addr, obj):

    for d in disk_servers:

        if disk_servers[d].addr == addr[0]:
            disk_servers[d].disconnect()
            break

    j = {"op": 12}
    req.send(b"FASS"+bytes(json.dumps(j), "utf-8"))


def fass_beat(req, addr, obj):

    found = False

    for d in disk_servers:

        if disk_servers[d].addr == addr[0]:

            disk_servers[d].last_hb = int(round(time.time() * 1000))
            js = {"op": 2}
            req.send(b"FASS" + bytes(json.dumps(js), "utf-8"))
            found = True
            return

    if not found:

        js = {"op": 5}
        req.send(b"FASS" + bytes(json.dumps(js), "utf-8"))
        return


def fass_identify(req, addr, obj):
    def register():
        disk_servers[obj["data"]["id"]] = DiskServer(id=obj["data"]["id"], token=obj["data"]["my_token"], addr=addr[0],
                                                     port=obj["data"]["my_port"])
        js = {"op": 4, "data": {"heartbeat": 4500}}
        req.send(b"FASS" + bytes(json.dumps(js), "utf-8"))

        disk_servers[obj["data"]["id"]].update_disk_info()

        return

    if obj["data"]["token"] == args.token:

        if not obj["data"]["id"] in disk_servers:
            print("New connection", addr[0])
            register()
            return

        else:

            if disk_servers[obj["data"]["id"]].addr == addr[0] or not disk_servers[obj["data"]["id"]].connected:
                disk_servers[obj["data"]["id"]].disconnect()
                print("Disk reconnected in", addr[0])
                register()
                return

            js = {"op": 9, "data": {"error": "Another Disk Server with same ID is already connected."}}
            req.send(b"FASS" + bytes(json.dumps(js), "utf-8"))
            return

    else:

        js = {"op": 5}
        req.send(b"FASS" + bytes(json.dumps(js), "utf-8"))
        return


def disconnect_everyone():

    context = ssl.SSLContext()

    indexes = []

    for sv in static.disk_servers:
        indexes.append(sv)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            sv = static.disk_servers[sv]

            s.connect((sv.addr, sv.port))

            req = context.wrap_socket(s, server_side=False)

            j = {"op": 12}

            req.send(b'FASS'+bytes(json.dumps(j), "utf-8"))

            dt = json.loads(str(req.recv(1024), "utf-8")[4:])

            if dt["op"] == 12:
                pass
            else:
                print("Disk Server refuse do disconnect")

    for s in indexes:

        static.disk_servers[s].disconnect()
