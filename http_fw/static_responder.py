import os
import mimetypes

from glob import glob
from pathlib import Path


class StaticResponder:
    def __init__(self, request, response, static_dir, templates_dir="templates"):
        self.request = request
        self.response = response
        self.static_dir = static_dir
        self.templates_dir = templates_dir
        self.file = None
        self._check_file()

    def _check_file(self):
        file_uri = self.request.uri.replace('..', '')
        path = f"{Path().absolute()}/{self.static_dir}{file_uri}"

        if file_uri.endswith(".html"):
            path = f"{Path().absolute()}/{self.static_dir}/{self.templates_dir}{file_uri}"
        files = glob(path)

        if len(files) > 0 and os.path.isfile(files[0]):
            self.file = files[0]
            self.response.add_header("Content-Type", self.get_response_mimetype(path))

    def prepare_response(self):
        if self.file:
            file = open(self.file, 'rb')
            self.response.set_file_body(file)

    @staticmethod
    def get_response_mimetype(uri_path):
        mimetype, _ = mimetypes.guess_type(uri_path)
        return mimetype

