import socket

HOST = "127.0.0.1"
PORT = 80


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"server listening on port: {PORT}")

    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        request = conn.recv(1024)

        data = request.decode("utf-8").split("\r\n")
        _, path, http_version = data[0].split(" ")
        html = ""

        response = f"{http_version} 404 Not Found\r\nConnection: close\r\n"

        if path in ("/", "/index.html/", "/index.html"):
            with open("www/index.html", "r") as fd:
                html = fd.read()
            response = (
                f"{http_version} 200 OK\r\n"
                f"Connection: close\r\n"
                f"Content-type: text/html\r\n\r\n{html}"
            )
        response = response.encode("utf-8")

        conn.sendall(response)
