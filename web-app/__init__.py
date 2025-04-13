# pylint: skip-file

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


def create_app():
    mongo_uri = os.environ.get("MONGO_URI")
    mongo_db = os.environ.get("MONGO_DB")

    client = MongoClient(mongo_uri)
    db = client["project4_liquidgators"]
    sentence_collection = db.sentences
    audio_collection = db.audioFiles

    load_dotenv()
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

    mongo = PyMongo(app)

    return app
