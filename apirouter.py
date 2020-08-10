from args import args
from auth import auth_user, redirect_unauthorized
from render import render_admin


def process_api_router(req, packet):

    if packet.path == "/api/auth":
        process_auth(req, packet)
        req.close()
        return

    if redirect_unauthorized(packet):
        req.close()
        return


def process_auth(req, packet):

    token = packet.postUrlEncodedParameters.parameters["token"]

    if token == args.token:
        auth_user(req)
    else:
        render_admin(req, packet, True, "Token Incorreto")

