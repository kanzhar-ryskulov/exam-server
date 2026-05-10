from urllib.parse import parse_qs


class Request:
    def __init__(self, rfile):
        self.rfile = rfile
        self.method = ""
        self.uri = ""
        self.protocol = ""
        self.headers = {}
        self.body = None

        self.get_request_main_line()
        self.parse_headers()
        self.parse_body()

    def read_line(self):
        return self.rfile.readline().decode().strip()
    
    def get_request_main_line(self):
        line = self.read_line()
        if not line:
            return
        parts = line.split()
        if len(parts) == 3:
            self.method, self.uri, self.protocol = parts

    def parse_headers(self):
        while True:
            header = self.read_line()

            if not header:
                break
            header_name, header_value = header.split(": ")
            self.headers[header_name.lower()] = header_value

    def parse_body(self):
        if 'content-length' in self.headers:
            content_length = int(self.headers['content-length'])
            self.body = self.rfile.read(content_length).decode()
            self._parse_specific_body()

    def _parse_specific_body(self):
        if 'content-type' in self.headers:
            if self.headers['content-type'] == 'application/x-www-form-urlencoded':
                self.body = parse_qs(self.body)

    @property
    def query_params(self):
        if '?' not in self.uri:
            return {}

        query_string = self.uri.split('?')[1]
        print(query_string)
        params = parse_qs(query_string)

        return {k: v[0] if v else '' for k, v in params.items()}
