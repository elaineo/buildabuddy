from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('personality.html')


@app.route("/chat")
def chat():
    return render_template('chat.html')


@app.route("/meet")
def meet():
    return render_template('meet.html')


if __name__ == "__main__":
    app.run()
