import logging
import socketserver
import threading

from http_package import HttpRequest, HttpResponse


class HttpRequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        self.reqParser = HttpRequest()
        self.response = HttpResponse()

    def handle(self) -> None:
        logging.info(f"{threading.current_thread().name}: handling request")
        self.data = self.request.recv(1024).strip().decode().split("\r\n")
        self.request.sendall(
            self.response.sendResponse(self.reqParser.parse(self.data))
        )
        logging.info(f"{threading.current_thread().name}: sent response back")


class MyThreadingTCPServer(socketserver.ThreadingTCPServer):
    def server_activate(self) -> None:
        super().server_activate()
        ip, port = self.server_address
        logging.info(f"server is running on {ip}:{port}")


if __name__ == "__main__":
    fmt = "%(asctime)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt="%H:%M:%S")

    server = MyThreadingTCPServer(("127.0.0.1", 3000), HttpRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    logging.info(f"server loop running in thread: {server_thread.name}")
    server_thread.join()
