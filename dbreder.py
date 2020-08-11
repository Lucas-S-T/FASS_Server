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


def render_server_files_page(req, packet):

    path = packet.path.split("/")
    server = path[3]

    filespath = "/".join(path[5:])
    filespath = filespath.replace("%20", " ")

    (files, dirs) = disk_servers[server].get_file_list(filespath)

    helpers = {'list': list}

    dirobj = []
    fileobj = []

    for f in dirs:
        path = "dashboard/server/"+server+"/files/"+filespath+"/"+f
        if filespath == "":
            path = "dashboard/server/"+server+"/files/"+f
        dirobj.append({"dname": f[:10], "name": f, "path": path})

    for f in files:
        path = "server/"+server+"/"+filespath+"/"+f
        if filespath == "":
            path = "server/"+server+"/"+f

        icon = "/local/icon/document.png"
        if f.endswith("png") or f.endswith("jpg"):
            icon = "/"+path

        fileobj.append({"dname": f[:10], "name": f, "path": path, "icon": icon})

    sv = templates["server.html"]({"files": fileobj, "dirs": dirobj}, helpers=helpers)

    req.send(b"HTTP/1.1 200 OK\r\nServer: FASS\r\nContent-Length: " + bytes(str(len(sv)), "utf-8") + b"\r\n\r\n")
    req.send(bytes(sv, "utf-8"))

