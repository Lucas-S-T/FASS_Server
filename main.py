import asyncio
import signal
import sys

import process_fass
from socket_fass import start_socket_fass
import args
from template import load_templates


async def main():

    await start_socket_fass()


def disconnect(sig, frame):

    print("Disconnecting Disk Servers...")
    process_fass.disconnect_everyone()
    sys.exit(0)


signal.signal(signal.SIGINT, disconnect)
load_templates()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
