import logging
import socket
from concurrent import futures


class HttpResponse:
    def read(self, path, version, base="www"):
        if path in ("/", "/index.html/", "/index.html"):
            path = f"{base}/index.html"
        else:
            path = base + path

        try:
            with open(path, "r") as fd:
                content = fd.read()
                return (
                    f"{version} 200 OK\r\n"
                    f"Connection: close\r\n"
                    f"Content-type: text/html\r\n\r\n{content}"
                )
        except OSError:
            logging.info(f"No file with the name {path} was found")

    def response(self, data):
        _, path, http_version = data[0].split(" ")
        http_response = self.read(path, http_version) or (
            f"{http_version} 404 Not Found\r\nConnection: close\r\n"
        )
        return http_response.encode("utf-8")


class WebServer(socket.socket):
    def __init__(self, host: str, port: int) -> None:
        super(WebServer, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((host, port))
        logging.info("Server listening on %s:%d" % (host, port))
        self.listen()

    def handle_request(self, thread_id: int, response: HttpResponse) -> None:
        conn, addr = self.accept()
        logging.info("Thread(%d) start" % thread_id)
        logging.info("Thread %d: handle request" % thread_id)
        with conn:
            request = conn.recv(1024).decode("utf-8").split("\r\n")
            conn.sendall(response.response(request))
        logging.info("Thread %d: sent response" % thread_id)
        logging.info("Thread(%d) terminate" % thread_id)

    def __del__(self):
        logging.info("closing socket")
        self.close()
        logging.info("socket closed")


if __name__ == "__main__":
    fmt = "%(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt="%H:%M:%S")
    server = WebServer("127.0.0.1", 3000)
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(7):
            executor.submit(server.handle_request, i, HttpResponse())
