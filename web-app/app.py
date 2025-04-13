"""Main app implementation"""

import os
from flask import (
    Flask,
    request,
    jsonify,
    render_template as rt,
)
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from pymongo import MongoClient

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client["project4_liquidgators"]
sentence_collection = db.sentences
audio_collection = db.audioFiles

# Where our main app will go
load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


mongo = PyMongo(app)


@app.route("/")
def home():
    """Returns home webpage"""
    return rt("index.html")


@app.route("/converter")
def converter():
    """Returns converter webpage"""
    return rt("converter.html")


@app.route("/history")
def history():
    """Returns history webpage"""
    return rt("history.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """returns trancription"""
    print(request.headers.get("Content-Type"))
    audio = request.data
    # console log request
    audio_collection.insert_one({"audio": audio, "translated": False})

    # get back text
    transcribed = False
    original_sentence_transcribed = None
    # infinite loop? not finding transcription
    while not transcribed:
        original_sentence_transcribed = sentence_collection.find_one(
            {"britishified": "NONE"}
        )
        if original_sentence_transcribed is not None:
            transcribed = True

    transcription = original_sentence_transcribed["original_sentence"]
    return jsonify({"transcription": transcription})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
