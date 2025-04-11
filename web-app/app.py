"""Main app implementation"""

import os
from flask import (
    Flask,
    request,
    jsonify,
    render_template as rt,
)  # pylint: disable=import-error
from flask_pymongo import PyMongo  # pylint: disable=import-error
from dotenv import load_dotenv  # pylint: disable=import-error
from pymongo import MongoClient  # pylint: disable=import-error

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
sentence_collection = db["sentences"]
audio_collection = db["audio_files"]

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
    audio = request.data
    audio_collection.insert_one({
        "audio" : audio,
        "translated" : False
    })

    # get back text
    transcribed = False
    while not transcribed:
        sentence_collection.find_one()


    transcription = "insert Transcription"
    return jsonify({"transcription": transcription})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
