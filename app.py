from flask import Flask, abort, redirect, render_template, request, url_for

import db

app = Flask(__name__)
db.init_app(app)

# Routes
@app.route("/")
def index():
    return render_template("index.html", songs=db.random_songs(6))

@app.route("/rank", methods=["GET", "POST"])
def rank():
    if request.method == "POST":
        winner_id = request.form.get("winner")
        loser_id = request.form.get("loser")
        if not db.song_exists(winner_id) or not db.song_exists(loser_id) or winner_id == loser_id:
            abort(400)
        db.record_comparison(winner_id, loser_id)
        return redirect(url_for('rank'))

    song1, song2 = db.random_songs(2)
    return render_template("rank.html", song1=song1, song2=song2)

@app.route("/results")
def results():
    return render_template("results.html", songs=db.top_songs(3))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888, debug=True)