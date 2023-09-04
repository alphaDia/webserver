import unittest
from concurrent import futures

import requests


class WebServerTest(unittest.TestCase):
    """Before running the test case please make sure the server is running.

    You can run the server by typing python3 server.py in your terminal if you're
    on linux or python.exe server.py if you're on windows
    """

    def setUp(self) -> None:
        self.url = "http://127.0.0.1:3000"

    def test_get_index_page_without_full_file_name(self):
        # sourcery skip: class-extract-method
        url = f"{self.url}/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_index_page_with_full_file_name(self):
        url = f"{self.url}/index.html"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_data_to_cgi_script(self):
        url = f"{self.url}/cgi_bin/handle_form.py"
        body = {
            "first_name": "Mamadou Alpha",
            "last_name": "Diallo",
            "email": "alphadiallo@gmail.com",
            "birth_date": "1997-05-07",
        }
        response = requests.post(url, data=body)
        self.assertEqual(response.status_code, 200)

    def test_get_image_stored_on_the_server(self):
        url = f"{self.url}/image/image1.jpg"
        with open("www/image/image1.jpg", "rb") as fd:
            image = fd.read()
            byte_length = str(len(image))
        response = requests.get(url)
        content_length = response.headers["content-length"]
        self.assertEqual(content_length, byte_length)

    def test_get_invalid_path(self):
        url = f"{self.url}/invalid.html"
        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_send_multiple_request_to_server(self):
        urls = [f"{self.url}/detail/detail.html"] * 10

        with futures.ThreadPoolExecutor() as executor:
            responses = list(executor.map(requests.get, urls))

        self.assertEqual(responses[0].status_code, 200)
        self.assertEqual(responses[1].status_code, 200)
        self.assertEqual(responses[2].status_code, 200)
        self.assertEqual(responses[3].status_code, 200)
        self.assertEqual(responses[4].status_code, 200)
        self.assertEqual(responses[5].status_code, 200)
        self.assertEqual(responses[6].status_code, 200)
        self.assertEqual(responses[7].status_code, 200)
        self.assertEqual(responses[8].status_code, 200)
        self.assertEqual(responses[9].status_code, 200)


if __name__ == "__main__":
    unittest.main()
