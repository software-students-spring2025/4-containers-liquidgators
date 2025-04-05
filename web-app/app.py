from flask import Flask
from flask_pymongo import PyMongo
import os
from models.britishified import Britishified
from models.originalSentence import OriginalSentence


# Where our main app will go