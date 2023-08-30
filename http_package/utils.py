import logging
import os


def read_html_file(path: str, base="www"):
    logging.info(f"the path is {path}")
    path = (
        f"{base}/index.html" if path in {"/", "/index.html/"} else base + path
    )

    try:
        with open(path, "r") as fd:
            return fd.read()
    except OSError:
        logging.info(f"No file with the name {path} was found")


def read_image_file(path: str, base="www"):
    try:
        with open(f"{base}/{path}", "rb") as fd:
            return fd.read()
    except OSError:
        logging.info(f"No file with the name {path} was found")


def set_cgi_environ(request_method, query_string, body):
    os.environ["REQUEST_METHOD"] = request_method
    os.environ["QUERY_STRING"] = query_string
    os.environ["CONTENT_TYPE"] = "text/html"
    os.environ["CONTENT_LENGTH"] = f"{len(body.encode())}"
