from apirouter import process_api_router
from dbrouter import process_db_router
from process_file import process_file
from render import render_index, render_admin


def process_route(req, packet):

    if packet.path.endswith("/"):
        packet.path = packet.path[:len(packet.path)-1]

    if packet.method == "GET":

        if packet.path.startswith("/server") | packet.path.startswith("/local"):
            process_file(req, packet)
            return

        if packet.path == "":
            render_index(req, packet)
            return

        if packet.path == "/admin":
            render_admin(req, packet, False, "")
            return

        if packet.path.startswith("/dashboard"):
            process_db_router(req, packet)
            return

    if packet.path.startswith("/api"):
        process_api_router(req, packet)
