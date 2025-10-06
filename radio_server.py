from flask import Flask, request, Response, jsonify
import os
from datetime import datetime

app = Flask(__name__)

AUDIO_FILE = "live.mp3"
NOW_PLAYING_FILE = "nowplaying.txt"

# 📥 Réception du flux envoyé par BUTT
@app.route("/upload", methods=["POST"])
def upload():
    auth_header = request.headers.get("Authorization", "")
    # Autorise n’importe quel mot de passe ou celui défini ici :
    if "benzer123" not in auth_header and auth_header != "":
        return "Unauthorized", 401

    with open(AUDIO_FILE, "wb") as f:
        while True:
            chunk = request.stream.read(1024)
            if not chunk:
                break
            f.write(chunk)
    print("🎧 Flux reçu depuis BUTT")
    return "Flux reçu", 200


# 🔊 Diffusion du flux en temps réel
@app.route("/stream")
def stream():
    def generate():
        try:
            with open(AUDIO_FILE, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    yield chunk
        except FileNotFoundError:
            yield b""
    return Response(generate(), mimetype="audio/mpeg")


# 🎵 Données du morceau en cours
@app.route("/nowplaying")
def now_playing():
    if os.path.exists(NOW_PLAYING_FILE):
        with open(NOW_PLAYING_FILE, "r") as f:
            line = f.readline().strip()
            if "-" in line:
                artist, title = [s.strip() for s in line.split("-", 1)]
            else:
                artist, title = "DJ Benzer", line
    else:
        artist, title = "DJ Benzer", "Live Session"

    return jsonify({
        "artist": artist,
        "title": title,
        "cover": "https://cdn.pixabay.com/photo/2016/11/29/04/17/black-1869588_960_720.jpg",
        "updated": datetime.now().isoformat()
    })


# 🏁 Lancer le serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, threaded=True)
