import os
import http.server
import socketserver

PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()