
class HttpResponse:
    def __init__(self, plain_response):
        self._parse(plain_response)

    def _parse(self, plain_response):
        head, self.body = plain_response.split("\r\n\r\n")

        head_lines = head.split("\r\n")

        self.header = {}
        for line in head_lines:
            tmp = line.split(':')

            if len(tmp) == 2:
                self.header[tmp[0]] = tmp[1].strip(" \t")
            else:
                if tmp[0].startswith("HTTP/"):
                    status_tmp = tmp[0].split(" ")
                    self.header['http_ver'] = status_tmp[0]
                    self.header['code'] = int(status_tmp[1])
                    self.header['code_des'] = " ".join(status_tmp[2:])

        int_type_keys = ['Content-Length']
        for key in int_type_keys:
            if key in self.header:
                self.header[key] = int(self.header[key])

