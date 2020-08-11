from auth import redirect_unauthorized
from dbreder import render_dashboard, render_server_files_page
from static import disk_servers


def process_db_router(req, packet):

    if redirect_unauthorized(req, packet):
        return

    if packet.path == "/dashboard":
        process_dashboard(req, packet)

    if packet.path.startswith("/dashboard/server/"):
        process_server_page(req, packet)


def process_dashboard(req, packet):

    render_dashboard(req, packet)


def process_server_page(req, packet):

    path = packet.path.split("/")
    server = path[3]

    if server not in disk_servers or len(path) <4:
        req.send(b"HTTP/1.1 302 Found\r\nServer: FASS\r\nLocation: /dashboard\r\n\r\n")
        return

    if path[4] == "files":

        render_server_files_page(req, packet)
        return

    req.send(b"HTTP/1.1 302 Found\r\nServer: FASS\r\nLocation: /dashboard\r\n\r\n")
