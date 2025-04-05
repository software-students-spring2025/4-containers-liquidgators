from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from models.britishified import Britishified
from models.original_sentence import OriginalSentence


# Where our main app will go
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)