from http_fw import not_found, internal_server_error


class Router:
    def __init__(self):
        self.routes = {
            "get": {},
            "post": {}
        }

    def add(self, request_method, uri, controller_class, controller_method):
        self.routes[request_method.lower()][uri] = {
            "controller": controller_class,
            "method": controller_method
        }

    def get(self, uri, controller_class, controller_method):
        self.add("GET", uri, controller_class, controller_method)

    def post(self, uri, controller_class, controller_method):
        self.add("POST", uri, controller_class, controller_method)

    def run(self, request, response):
        if not request.method:
            return

        method_data = self.routes[request.method.lower()]
        uri_path = request.uri.split('?')[0]
        uri_data = method_data.get(uri_path)

        try:
            if uri_data:
                controller_class = uri_data["controller"]
                controller_method = uri_data["method"]
                controller = controller_class(request, response)
                getattr(controller, controller_method)()
            else:
                not_found(request, response)
        except Exception as e:
            print(str(e))
            internal_server_error(request, response)
