from http_fw import Response


def not_found(request, response):
    response.set_status(Response.HTTP_NOT_FOUND)
    response.add_header('Content-Type', 'text/html')
    response.set_body('<h1>404 Not found</h1>')


def internal_server_error(request, response):
    response.set_status(Response.HTTP_INTERNAL_SERVER_ERROR)
    response.add_header('Content-Type', 'text/html')
    response.set_body('<h1>Oops, something went wrong...</h1>')
