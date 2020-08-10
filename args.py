import argparse

parser = argparse.ArgumentParser(description="FASS Data Server")
parser.add_argument("httpport", type=int, help="FASS Data HTTP Server Port")
parser.add_argument("httpsport", type=int, help="FASS Data HTTPS Server Port")
parser.add_argument("certfile", type=str, help="Certificate file")
parser.add_argument("certkey", type=str, help="Certificate Key file")
parser.add_argument("certca", type=str, help="Certificate CA file")
parser.add_argument("token", type=str, help="FASS Data Server Token")
parser.add_argument("maxcache", type=int, help="Max file size to store on cache in MB")
parser.add_argument("cachettl", type=int, help="Cache TTL in minutes")

args = parser.parse_args()
