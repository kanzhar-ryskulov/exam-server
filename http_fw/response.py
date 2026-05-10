from os import fstat


class Response:
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_FOUND = 302
    HTTP_INTERNAL_SERVER_ERROR = 500

    MESSAGES = {
        HTTP_OK: 'OK',
        HTTP_BAD_REQUEST: 'Bad Request',
        HTTP_NOT_FOUND: 'Not Found',
        HTTP_FOUND: 'Found',
        HTTP_INTERNAL_SERVER_ERROR: 'Internal Server Error'
    }
    PROTOCOL = 'HTTP/1.1'

    def __init__(self, wfile):
        self.wfile = wfile
        self.status = self.HTTP_OK
        self.headers = {}
        self.body = None
        self.file_body = None

    def set_status(self, status):
        self.status = status

    def get_status_line(self):
        return f"{self.PROTOCOL} {self.status} {self.MESSAGES[self.status]}\r\n"

    def add_header(self, header_key, value):
        self.headers[header_key] = value

    def get_headers(self):
        headers = [f"{header_key}: {self.headers[header_key]}" for header_key in self.headers]
        return "\r\n".join(headers) + "\r\n\r\n"

    def set_body(self, body):
        self.body = body.encode()
        self.add_header("Content-Length", len(self.body))

    def set_file_body(self, file):
        self.file_body = file
        file_len = fstat(self.file_body.fileno()).st_size
        self.add_header("Content-Length", file_len)

    def send(self):
        response = self.get_status_line()
        response += self.get_headers()
        self.wfile.write(response.encode())

        if self.body:
            self.wfile.write(self.body)

        if self.file_body:
            while True:
                body = self.file_body.read(1024)

                if not body:
                    break
                self.wfile.write(body)
