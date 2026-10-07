import random

from flask import Flask, render_template, request

app = Flask(__name__)

song_names = ["Rolling Loud", "STARGAZING", "Fancy", "Neon Kitchen"]
song_links = ["https://i.scdn.co/image/ab67616d0000b2739382b279fa552e0fae460a85", "https://media.pitchfork.com/photos/5b60c32dc50e6c2e339b99fe/1:1/w_800,h_800,c_limit/Travis%20Scott_Astroworld.jpg",
              "https://upload.wikimedia.org/wikipedia/en/9/9c/Drake_-_Thank_Me_Later_cover.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original", "https://f4.bcbits.com/img/a4025637069_16.jpg"]

wins = {}

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rank", methods=["GET", "POST"])
def rank():
    idx = random.randint(0, len(song_names) - 1)
    song1 = song_names[idx]
    song1_link = song_links[idx]
    idx = random.randint(0, len(song_names) - 1)
    song2 = song_names[idx]
    song2_link = song_links[idx]

    if request.method == "POST":
        action = request.form.get("action")
        if action == song1:
            wins[song1] = wins.get(song1, 0) + 1
        elif action == song2:
            wins[song2] = wins.get(song2, 0) + 1
    print(wins)
    
    return render_template("rank.html", song1=song1, song1_link=song1_link, song2=song2, song2_link=song2_link)

@app.route("/results")
def results():
    sorted_songs = sorted(wins.items(), key=lambda x: x[1], reverse=True)
    top_songs = [song for song, _ in sorted_songs[:4]]
    while len(top_songs) < 4:
        top_songs.append(None)
    return render_template("results.html", song1=top_songs[0], song2=top_songs[1], song3=top_songs[2], song4=top_songs[3])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8888", debug=True)