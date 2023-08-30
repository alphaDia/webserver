import logging
import socket
from concurrent import futures

from http_package import HttpRequest, HttpResponse


class WebServer(socket.socket):
    def __init__(self, host: str, port: int) -> None:
        super(WebServer, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))
        self.listen(1)
        logging.info("Server listening on %s:%d" % (host, port))

    def handle_request(
        self, thread_id: int, req: HttpRequest, rsp: HttpResponse
    ) -> None:
        conn, addr = self.accept()
        logging.info("Thread(%d) start" % thread_id)
        logging.info("Thread(%d): handle request" % thread_id)
        with conn:
            request = conn.recv(1024).decode().split("\r\n")
            conn.sendall(rsp.sendResponse(req.parse(request)))
        logging.info("Thread(%d): sent response" % thread_id)
        logging.info("Thread(%d) terminate" % thread_id)

    def __del__(self):
        self.close()
        logging.info("socket closed")


if __name__ == "__main__":
    worker_threads = 20
    fmt = "%(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt="%H:%M:%S")
    server = WebServer("127.0.0.1", 3000)
    with futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
        for i in range(worker_threads):
            executor.submit(
                server.handle_request, i, HttpRequest(), HttpResponse()
            )
