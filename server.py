from http.server import SimpleHTTPRequestHandler, HTTPServer

host = "0.0.0.0"
port = 8000

httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
print(f"Serving HTTP on {host} port {port}...")
httpd.serve_forever()
