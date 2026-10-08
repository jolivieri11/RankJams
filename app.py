from os import name
import random

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

songs = [
    {"id": "rolling-loud", "name": "Rolling Loud", "image": "https://i.scdn.co/image/ab67616d0000b2739382b279fa552e0fae460a85"},
    {"id": "stargazing", "name": "STARGAZING", "image": "https://media.pitchfork.com/photos/5b60c32dc50e6c2e339b99fe/1:1/w_800,h_800,c_limit/Travis%20Scott_Astroworld.jpg"},
    {"id": "fancy", "name": "Fancy", "image": "https://upload.wikimedia.org/wikipedia/en/9/9c/Drake_-_Thank_Me_Later_cover.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
    {"id": "neon-kitchen", "name": "Neon Kitchen", "image": "https://f4.bcbits.com/img/a4025637069_16.jpg"},
    {"id": "new-sky", "name": "New Sky", "image": "https://thumb.wikimedia.org/wikipedia/en/thumb/7/72/SiRChasingSummer.jpg/250px-SiRChasingSummer.jpg?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail"},
    {"id": "mom", "name": "M.O.M", "image": "https://i.scdn.co/image/ab67616d0000b273f595e5f39c4050805de5caf5"},
    {"id": "cosmo-freestyle", "name": "Cosmo Freestyle", "image": "https://upload.wikimedia.org/wikipedia/en/0/01/You_Only_Die_1nce_album_cover.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
    {"id": "self-control", "name": "Self Control", "image": "https://upload.wikimedia.org/wikipedia/en/a/a0/Blonde_-_Frank_Ocean.jpeg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"},
    {"id": "be-like-a-woman", "name": "Be Like a Woman", "image": "https://i5.walmartimages.com/seo/White-Trails-CD_e6059b49-5a72-4e35-99ad-b1b2f65cad9d.50054e2aa7a3df88245f55353a32858d.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF"},
    {"id": "cinderella", "name": "Cinderella", "image": "https://upload.wikimedia.org/wikipedia/en/9/93/Mac_Miller_-_The_Divine_Feminine.png?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original"}
]
songs_by_id = {song["id"]: song for song in songs}

wins = {}

# Routes
@app.route("/")
def index():
    chosen = random.sample(songs, 6)
    return render_template("index.html", songs=chosen)

@app.route("/rank", methods=["GET", "POST"])
def rank():
    if request.method == "POST":
        winner_id = request.form.get("winner")
        loser_id = request.form.get("loser")
        if winner_id not in songs_by_id or loser_id not in songs_by_id or winner_id == loser_id:
            abort(400)
        wins[winner_id] = wins.get(winner_id, 0) + 1
        return redirect(url_for('rank'))

    song1, song2 = random.sample(songs, 2)
    return render_template("rank.html", song1=song1, song2=song2)

@app.route("/results")
def results():
    sorted_songs = sorted(wins.items(), key=lambda x: x[1], reverse=True)
    entrys = {songs_by_id[id]["name"]: wins.get(id, 0) for id, _ in sorted_songs[:3]}
    return render_template("results.html", top_wins=entrys)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888, debug=True)