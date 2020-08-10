import pybars

from auth import is_authorized
from template import templates


def render_index(req, packet):

    index = templates["index.html"]({})

    req.send(b"HTTP/1.1 200 OK\r\nServer: FASS\r\nContent-Length: " + bytes(str(len(index)), "utf-8") + b"\r\n\r\n")
    req.send(bytes(index, "utf-8"))


def render_admin(req, packet, err, errmsg):
    index = templates["login.html"]({"error": err, "errormsg": errmsg})

    if is_authorized(packet):

        req.send(b"HTTP/1.1 302 Found\r\nLocation: /dashboard\r\n\r\n")
        return

    else:
        req.send(b"HTTP/1.1 200 OK\r\nServer: FASS\r\nContent-Length: " + bytes(str(len(index)), "utf-8") + b"\r\n\r\n")
        req.send(bytes(index, "utf-8"))
