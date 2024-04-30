import html
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mimetypes
import os
import posixpath
import re
import urllib


class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/"):
            client_ip = self.client_address[0]
            r = f"""
<!DOCTYPE html>
<html>
<head>
    <title>I am GitHub Action</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
</head>
<style>
    body {{
        margin: 40px;
    }}
</style>
<body>
<h1> Hello, I am github action </h1>
<h3>And you are {client_ip}</h3>
<br>
"""
            # add directory listing below
            r += "<h2>Directory Listing</h2>"

            #
            r += "<hr>\n<ul>"
            cur_dir = os.path.join(self.directory, self.path[1:])
            for name in sorted(os.listdir(cur_dir)):
                fullname = os.path.join(cur_dir, name)
                displayname = linkname = name
                if os.path.isdir(fullname):
                    displayname = name + "/"
                    linkname = name + "/"
                if os.path.islink(fullname):
                    displayname = name + "@"
                    # Note: a link to a directory displays with @ and links with /
                r += '<li><a href="%s">%s</a></li>' % (
                    urllib.parse.quote(linkname, errors="surrogatepass"),
                    html.escape(displayname, quote=False),
                )
            r += "</ul>\n<hr>\n</body>\n</html>\n"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(r.encode("utf-8"))

        else:
            super().do_GET()

    def guess_type(self, path):
        guess = super().guess_type(path)
        if guess == "application/octet-stream":
            try:
                with open(path, "r") as f:
                    content = f.read(1024)
                if content and isinstance(content, str):
                    return "text/plain"
            except UnicodeDecodeError:
                pass

        return guess


def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server starting on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run(port=8000)
