from flask import Flask, Response, jsonify
import requests, os, time

app = Flask(__name__)

# Fichier où BUTT enverra le flux (tu pourras le configurer)
STREAM_FILE = "stream.mp3"

# Dernier morceau connu (pour ne pas répéter)
current_track = {"title": "Aucune musique", "artist": "DJ Benzer", "cover": ""}

# 🔍 Fonction pour chercher une image de pochette sur Internet (iTunes API)
def search_cover(query):
    try:
        r = requests.get(f"https://itunes.apple.com/search?term={query}&entity=song&limit=1")
        data = r.json()
        if data["resultCount"] > 0:
            return data["results"][0]["artworkUrl100"].replace("100x100", "600x600")
    except:
        pass
    return "https://cdn.pixabay.com/photo/2016/11/29/04/17/black-1869588_960_720.jpg"

@app.route("/nowplaying", methods=["GET"])
def now_playing():
    return jsonify(current_track)

# 🔊 Route pour diffuser ton flux audio (BUTT enverra ici)
@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        with open(STREAM_FILE, "rb") as f:
            while chunk := f.read(1024):
                yield chunk
    return Response(generate(), mimetype="audio/mpeg")

# 🧠 Simulation de la mise à jour du titre (plus tard on reliera à BUTT)
@app.route("/update/<artist>/<title>", methods=["GET"])
def update_track(artist, title):
    global current_track
    query = f"{artist} {title}"
    cover = search_cover(query)
    current_track = {"artist": artist, "title": title, "cover": cover}
    return jsonify({"status": "ok", "cover": cover})

if __name__ == "__main__":
    print("🚀 Serveur radio en ligne sur http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
