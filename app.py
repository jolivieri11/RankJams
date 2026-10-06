from flask import Flask, render_template

app = Flask(__name__)


# Routes
@app.route("/")
def home():
    return render_template("hardcode.html")

@app.route("/rank")
def rank():
    return ...

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8888", debug=True)