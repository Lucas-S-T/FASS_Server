import uuid

tokens = []


def auth_user(req):

    tk = uuid.uuid4().hex
    tokens.append(tk)

    req.send(b"HTTP/1.1 302 Found\r\nSet-Cookie: token="+bytes(tk, "utf-8")+b"; Path=/; Max-Age=2592000\r\nLocation: /dashboard\r\n\r\n")
    req.close()


def is_authorized(packet):

    if "token" in packet.cookies:
        if packet.cookies["token"] in tokens:
            return 1
    return 0


def redirect_unauthorized(req, packet):

    if is_authorized(packet):
        return 0
    else:
        req.send(b"HTTP/1.1 302 Found\r\nLocation: /admin\r\n\r\n")
        return 1
