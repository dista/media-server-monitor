from exception import *

class Uri:
    def __init__(self, uri_str):
        self.uri = uri_str
        self.schemal, self.host, self.port, self.path = self._parse(uri_str)

    def _parse(self, url):
        try:
            tmp = url.strip(" \r\n\t")
            schemal = "http"

            schemal_start = tmp.find('://')

            if schemal_start != -1:
                schemal = tmp[0:schemal_start]
                tmp = tmp[schemal_start + 3 : ]

            host = tmp
            path = "/"

            path_start = tmp.find('/')

            if path_start != -1:
                host = tmp[0: path_start]
                path = tmp[path_start:]

            port = 80

            port_start = host.find(":")

            if port_start != -1:
                port = int(host[port_start + 1 : ])
                host = host[:port_start]

            return (schemal, host, port, path)
        except Exception, e:
            raise URIError(e) 
