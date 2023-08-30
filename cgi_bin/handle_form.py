import os
import sys
from datetime import datetime
from urllib.parse import parse_qs

content_length = os.environ["CONTENT_LENGTH"]
method = os.environ["REQUEST_METHOD"]
query_string = os.environ["QUERY_STRING"]

if method == "POST":
    data = parse_qs(sys.stdin.read(int(content_length)))

    first_name = data.get("first_name")[0]
    last_name = data.get("last_name")[0]
    email = data.get("email")[0]
    birth_date = data.get("birth_date")[0]

    # compute age base
    today = datetime.now().date()
    delta = today - datetime.strptime(birth_date, "%Y-%m-%d").date()
    age = delta.days // 365

    print("<!DOCTYPE html>")
    print("<html lang='en'>")
    print("<head>")
    print("<meta charset='utf-8'>")
    print(
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    )
    print("<title>Simple web page</title>")
    print("</head>")
    print("<body>")
    print(f"<h1>Welcome to your dashboard {first_name} {last_name}</h1>")
    print(f"<h3>Email: {email}</h3>")
    print(f"<h3>Age: {age}</h3>")
    print("</body>")
    print("</html>")
