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
<h3>And you are:</h3>
<ul>
{''.join([
    "<li>" + content + "</li>"
    for content in split_user_agent(self.headers.get("User-Agent", ""))
])}
</ul>
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


def split_user_agent(input_string):
    paren_level = 0
    split_positions = []
    for i, char in enumerate(input_string):
        if char == "(":
            paren_level += 1
        elif char == ")":
            paren_level -= 1
        elif (
            char.isupper()
            and paren_level == 0
            and i != 0
            and (input_string[i - 1] == " " or input_string[i - 1] in ".,;/")
        ):
            split_positions.append(i)

    parts = []
    last_pos = 0
    for pos in split_positions:
        parts.append(input_string[last_pos:pos].strip())
        last_pos = pos
    parts.append(input_string[last_pos:].strip())

    return parts


def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server starting on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run(port=8000)
