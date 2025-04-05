from flask import Flask
from flask_pymongo import PyMongo
import os
from models.britishified import Britishified
from models.original_sentence import Original_Sentence


# Where our main app will go