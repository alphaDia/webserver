import logging
import os
import subprocess

from .utils import read_html_file, read_image_file, set_cgi_environ


class HttpResponse:
    def _makeCgiResponse(self, parsed_request):
        query_string = parsed_request.get("query_string")
        request_method = parsed_request.get("request_method")
        version = parsed_request.get("version")
        path = parsed_request.get("path")
        body = parsed_request.get("body")

        set_cgi_environ(request_method, query_string, body)

        if not os.path.isfile(f".{path}"):
            return (
                f"{version} 404 Not Found\r\n"
                "Connection: close\r\n\r\n<h1>404 Not Found</h1>"
            )

        py_process = subprocess.run(
            ["python3", f"./{path}"],
            input=body,
            check=True,
            text=True,
            capture_output=True,
        )

        logging.info(f"STDOUT: {py_process.stdout}")

        if py_process.returncode != 0:
            return (
                f"{version} 500 Server Side Error\r\n"
                "Connection: close\r\n\r\n<h1>500 Server Error</h1>"
            )

        return (
            f"{version} 200 OK\r\n"
            f"Content-length:{len(py_process.stdout.encode())}\r\n"
            f"Content-type: text/html; charset='utf8'\r\n\r\n{py_process.stdout}"
        )

    def _makeHtmlResponse(self, path, version):
        logging.info(f"path: {path}")
        response_body = read_html_file(path)
        return (
            (
                f"{version} 200 OK\r\n"
                f"Content-length:{len(response_body.encode())}\r\n"
                f"Content-type: text/html; charset='utf8'\r\n\r\n{response_body}"
            )
            if response_body
            else (
                f"{version} 404 Not Found\r\n"
                "Connection: close\r\n\r\n<h1>404 Not Found</h1>"
            )
        )

    def _makeImageResponse(self, path, version):
        extension = path.rsplit(".", 1)[1]
        image = read_image_file(path)

        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-length:" + str(len(image)).encode() + b"\r\n"
            b"Content-type: image/" + f"{extension}".encode() + b"\r\n\r\n"
        ) + image

        return (
            response
            if image
            else (
                f"{version} 404 Not Found\r\n"
                "Connection: close\r\n\r\n<h1>404 Not Found</h1>"
            )
        )

    def sendResponse(self, parsed_request):
        path = parsed_request.get("path")
        version = parsed_request.get("version")

        if path.split("/")[1] == "cgi_bin":
            return self._makeCgiResponse(parsed_request).encode()

        if path.split("/")[1] == "image":
            logging.info("Read image")
            return self._makeImageResponse(path, version)

        return self._makeHtmlResponse(path, version).encode()


class HttpRequest:
    def parse(self, request):
        method, path, version = request[0].split(" ")
        body = request[-1]
        query_string = path.split("?")[1] if "?" in path else ""
        return {
            "request_method": method,
            "query_string": query_string,
            "version": version,
            "path": path,
            "body": body,
        }
