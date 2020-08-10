from static import disk_servers
from template import templates
from helpers import list


def render_dashboard(req, packet):

    def calc_hr(v):
        if v > 1000*1000*1000:
            return str(round(v/1000/1000/1000, 1))+" GB"
        if v > 1000 * 1000:
            return str(round(v / 1000 / 1000, 1)) + " MB"
        if v > 1000:
            return str(round(v / 1000, 1)) + " KB"

        return str(v, "utf=8") + " B"

    helpers = {'list': list}

    servers = []

    for s in disk_servers:
        s = disk_servers[s]
        s.update_disk_info()

        hr_used = calc_hr(int(s.disk_used))
        hr_total = calc_hr(int(s.disk_total))

        percent = round(s.disk_used * 100.0 / s.disk_total, 2)

        servers.append({"id": s.id, "total": hr_total, "used": hr_used, "percent": percent})

    db = templates["dashboard.html"]({"servers": servers}, helpers=helpers)

    req.send(b"HTTP/1.1 200 OK\r\nServer: FASS\r\nContent-Length: " + bytes(str(len(db)), "utf-8") + b"\r\n\r\n")
    req.send(bytes(db, "utf-8"))
