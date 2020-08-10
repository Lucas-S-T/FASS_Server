from auth import redirect_unauthorized
from dbreder import render_dashboard


def process_db_router(req, packet):

    if redirect_unauthorized(req, packet):
        return

    if packet.path == "/dashboard":
        process_dashboard(req, packet)


def process_dashboard(req, packet):

    render_dashboard(req, packet)
