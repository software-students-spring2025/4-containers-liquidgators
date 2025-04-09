# Use speech to text API to get text from speech (Sam)
# Store the original text to the original text DB (Jasmine/ Tadelin)
# Parse the original text -> britishified version (Jasmine/ Tadelin)
# ^ (this file should do that, or we just shove it all into app.py)
# Save the britishified version into britishified DB (Jasmine/ Tadelin)

"""This file contains the algorithm to change from american to british"""
from pymongo import MongoClient
import os

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
sentence_collection = db["sentences"]

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
}

# Assumes user doesn't input audio that fast & ML doesn't process audio that fast!!!
# Potential bugs with this kind of implementation
og_sentence = sentence_collection.find_one({"britishified": "NONE"})
og_words = str(og_sentence["original_sentence"]).split()
new_sentence = []

for word in og_words:
    if word in britishConv:
        new_sentence.append(britishConv[word])
    else:
        new_sentence.append(word)

NEW_SENTENCE = " ".join(new_sentence)

# Now save new britishified sentence to DB
sentence_collection.update_one(
    {"_id": og_sentence["_id"]}, {"$set": {"britishified": NEW_SENTENCE}}
)
