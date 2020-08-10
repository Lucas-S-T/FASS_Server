import socket
import threading

from args import args
from handler_connection import handler_connection


async def start_socket_fass():

    threading.Thread(target=start_socket_fass_no_ssl).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", args.httpsport))
        s.listen(5)

        while True:
            (conn, addr) = s.accept()

            threading.Thread(target=handler_connection, args=(conn, addr, True)).start()

            pass


def start_socket_fass_no_ssl():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", args.httpport))
        s.listen(5)

        while True:
            (conn, addr) = s.accept()

            threading.Thread(target=handler_connection, args=(conn, addr, False)).start()

            pass


