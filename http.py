class PostUrlEncodedParameters:

    def __init__(self):
        self.parameters = {}

    def parseParameters(self, str):
        param = str.split("&")

        for p in param:
            kv = p.split("=")
            if len(kv) >1:
                self.parameters[kv[0]] = kv[1]
        pass


class HttpPacket:

    def __init__(self):
        self.allBytes = ""
        self.headerStr = ""
        self.method = ""
        self.remainBytes = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.paramsBytes = ""
        self.postUrlEncodedParameters = PostUrlEncodedParameters()
        self.cookies = {}

    def parseRequest(self, reqstr, sock):

        self.allBytes = reqstr

        rd = reqstr.split("\r\n\r\n")

        self.headerStr = rd[0]
        self.remainBytes = rd[1]

        hr = rd[0].split("\r\n")

        fl = hr[0].split(" ")

        ptpr = fl[1].split("?")

        self.method = fl[0]
        self.path = ptpr[0]
        if len(ptpr) >1:
            self.paramsBytes = ptpr[1]
        self.version = fl[2]

        for h in hr[1:]:
            kv = h.replace(": ", ":").split(":")
            self.headers[kv[0]] = kv[1]

        if "Content-Type" in self.headers:

            if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
                size = int(self.headers["Content-Length"])
                if len(self.remainBytes) < size:
                    self.remainBytes += str(sock.read(size - len(self.remainBytes)), "utf-8")
                self.postUrlEncodedParameters.parseParameters(self.remainBytes)

        if "Cookie" in self.headers:

            ck = self.headers["Cookie"].split("; ")
            for c in ck:
                kv = c.split("=")
                self.cookies[kv[0]] = kv[1]

        return self


