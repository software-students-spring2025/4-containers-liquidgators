"""Main app implementation"""

import os
from flask import Flask, render_template as rt # pylint: disable=import-error
from flask_pymongo import PyMongo # pylint: disable=import-error
from dotenv import load_dotenv # pylint: disable=import-error


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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
