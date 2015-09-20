import os
from flask import Flask
from flask import render_template
from flask import jsonify

PORT = int(os.getenv('VCAP_APP_PORT', '8000'))

#Handler = http.server.SimpleHTTPRequestHandler

#httpd = socketserver.TCPServer(("", PORT), Handler)

#print("serving at port", PORT)
#httpd.serve_forever()


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('personality.html')


@app.route("/chat")
def chat():
    return render_template('chat.html')


if __name__ == '__main__':
    app.run()
