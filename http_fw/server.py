from socketserver import StreamRequestHandler, ThreadingMixIn, TCPServer

from http_fw import Request, Response, StaticResponder


def run(router, config):
    class HelloServerTCPHandler(StreamRequestHandler):
        def handle(self):
            request = Request(self.rfile)
            response = Response(self.wfile)

            static_responder = StaticResponder(request, response, config.get("static_dir"))
            if static_responder.file:
                static_responder.prepare_response()
            else:
                router.run(request, response)
            response.send()

    class ThreadedTCPServer(ThreadingMixIn, TCPServer):
        pass

    HOST = config.get("host", "localhost")
    PORT = config.get("port", 8001) 
    TCPServer.allow_reuse_address = True

    with ThreadedTCPServer((HOST, PORT), HelloServerTCPHandler) as server:
        server.serve_forever()
