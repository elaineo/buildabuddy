from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('starter.html')

if __name__ == "__main__":
    app.run()
