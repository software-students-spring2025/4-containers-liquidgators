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

load_dotenv()
mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client["project4_liquidgators_1"]
sentence_collection = db["sentences"]
audio_collection = db["audioFiles"]

# Where our main app will go
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


mongo = PyMongo(app)

britishConv = {
    "apartment": "flat",
    "bangs": "fringe",
    "candy": "sweets",
    "chips": "crisps",
    "closet": "wardrobe",
    "cookie": "biscuit",
    "crib": "cot",
    "diaper": "nappy",
    "drugstore": "chemist",
    "eggplant": "aubergine",
    "elevator": "lift",
    "highway": "motorway",
    "french fries": "chips",
    "gas": "petrol",
    "jumprope": "skipping rope",
    "mailbox": "postbox",
    "pacifier": "dummy",
    "pants": "trouser",
    "robe": "dressing gown",
    "sidewalk": "pavement",
    "sled": "sledge",
    "soccer": "football",
    "sprinkles": "hundreds and thousands",
    "stroller": "pushchair",
    "subway": "underground",
    "suspenders": "braces",
    "takeout": "takeaway",
    "thumbtack": "drawing pin",
    "trunk": "boot",
    "undershirt": "vest",
    "vacation": "holiday",
    "washcloth": "flannel",
    "zip code": "postcode",
    "zucchini": "courgette",
    "humans": "homosapiens",
    "dude": "bloke",
    "bro": "bloke",
    "tired": "knacked",
    "very": "bloody",
    "thanks": "cheers",
    "friends": "mate",
    "angry": "pissed",
    "cup of tea": "cuppa",
    "food": "grub",
    "sandwich": "sarnie",
    "disrespectful": "cheeky",
    "math": "maths",
    "silly": "daft",
    "stupid": "daft",
    "illegal": "dodgy",
    "shocked": "gobsmacked",
    "annoyed": "miffed",
    "terrible": "rubbish",
    "money": "dosh",
    "dollars": "pounds",
    "like": "quite enjoy",
    "bathroom": "loo",
    "disappointed": "gutted",
    "wow": "blimey",
    "vocabulary": "lexicon",
    "big": "massive",
    "perfect": "impeccable",
    "went": "travelled to",
    "color": "colour",
    "favorite": "favourite",
    "flavor": "flavour",
    "aluminum": "aluminium",
    "buck": "quid",
    "slowpoke": "slowcoach",
    "roadtrip": "car journey",
    "camper": "caravan",
    "truck": "lorry",
    "wrench": "spanner",
    "windshield": "windscreen",
    "armor": "armour",
    "apologize": "apologise",
    "fantasize": "fantasise",
    "paralyze": "paralyse",
    "defense": "defence",
    "dialog": "dialogue",
    "meter": "metre",
    "person": "individual",
    "brother": "bruv",
    "skull": "cranium",
    "coffin": "casket",
    "ghost": "ghoul",
    "graveyard": "cemetary",
    "spider": "arachnid",
    "beautiful": "wonderously elegant",
    "hurt": "harmed",
    "detailed": "intricate",
    "tasty": "decadent",
    "classy": "refined",
    "joke": "jest",
    "bought": "purchased",
    "good": "splendid",
    "bad": "inadequate",
    "boring": "monotonous and tedious",
    "think": "suspect",
    "videogame": "electronic game",
    "behavior": "behaviour",
}


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
    sentences = sentence_collection.find_one({"britishified": {"$ne": "NONE"}})
    return rt("history.html", sentences=sentences)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    """returns transcription"""

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


@app.route("/britishify", methods=["POST"])
def britishify():
    """returns britishified sentence"""

    britishify = False
    while not britishify:
        to_british_sentence = sentence_collection.find_one({"britishified": "NONE"})
        if to_british_sentence is not None:
            britishify = True
            og_words = str(to_british_sentence["original_sentence"]).split()
            new_sentence = []

            for word in og_words:
                if word in britishConv:
                    new_sentence.append(britishConv[word])
                else:
                    new_sentence.append(word)

            NEW_SENTENCE = " ".join(new_sentence)

            # Now save new britishified sentence to DB
            sentence_collection.update_one(
                {"_id": to_british_sentence["_id"]},
                {"$set": {"britishified": NEW_SENTENCE}},
            )
    return jsonify({"britishify": NEW_SENTENCE})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
