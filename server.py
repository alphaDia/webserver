import logging
import socket
import time
from concurrent import futures


class Server:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((self.host, self.port))

    def listen(self):
        logging.info("Server listening on %s:%d" % (self.host, self.port))
        self.soc.listen()

    def accept(self):
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(self.handle_connection)

    def handle_connection(self):
        conn, addr = self.soc.accept()
        with conn:
            logging.info("Connection received from client")
            request = conn.recv(1024)
            data = request.decode("utf-8").split("\r\n")
            conn.sendall(self.handle_response(data))

    def handle_response(self, data):
        _, path, http_version = data[0].split(" ")
        response = f"{http_version} 404 Not Found\r\nConnection: close\r\n"
        if path in ("/", "/index.html/", "/index.html"):
            with open("www/index.html", "r") as fd:
                content = fd.read()
                response = (
                    f"{http_version} 200 OK\r\n"
                    f"Connection: close\r\n"
                    f"Content-type: text/html\r\n\r\n{content}"
                )
        response = response.encode("utf-8")

        return response


def blocked_print(id):
    print("print %d" % id)
    time.sleep(3)


if __name__ == "__main__":
    fmt = "%(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt="%H:%M:%S")
    server = Server("127.0.0.1", 80)
    server.listen()
    server.accept()
