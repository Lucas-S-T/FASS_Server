import http
import json
import ssl

from args import args
from process_file import process_file
from router import process_route


def handler_connection(conn, addr, ssli):

    if ssli:
        req = ssl.wrap_socket(conn, keyfile=args.certkey, certfile=args.certfile, server_side=True, ca_certs=args.certca)
    else:
        req = conn

    v = req.recv(4096)
    if len(v) > 0:
        if v.startswith(b"FASS"):

            obj = json.loads(v[4:])
            from process_fass import process_fass
            process_fass(req, addr, obj)

        else:

            packet = http.HttpPacket().parseRequest(reqstr=v.decode("utf-8"), sock=req)
            process_route(req, packet)

    conn.close()

