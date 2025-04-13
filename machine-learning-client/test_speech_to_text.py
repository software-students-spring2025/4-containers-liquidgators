"""
Unit testing file using pytest for ML client.
"""
import pytest
#import speech_to_text
import os
import speech_recognition as sr  # pylint: disable=import-error
from pymongo import MongoClient  # pylint: disable=import-error

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
sentence_collection = db["sentences"]
audio_collection = db["audio_files"]

def test_initialize():
    """
    Tests initialization of Google Cloud Speech Recognizer.
    """
    # create recognizer
    r = sr.Recognizer()
    assert isinstance(r, sr.Recognizer), "Current recognizer is not an instance of sr.Recognizer."

@pytest.mark.parametrize("test_audio_file", ["OSR_us_000_0011_8k.wav"])
def test_read_user_inp(test_audio_file, r):
    """
    Tests reading in of user audio as an AudioFile.
    """
    # using user's un-britishified audio
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance
    assert audio is not None, "AudioData instance cannot be None."

@pytest.mark.parametrize("test_audio_file", ["OSR_us_000_0011_8k.wav"])
def test_speech_recognition(self, test_audio_file, r):
    """
    Tests if Google Cloud speech recognizer performs at baseline levels.
    """
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance
    user_text = r.recognize_google_cloud(audio)
    assert user_text.lower() == "the boy was there when the sun rose a rod is used to catch pink salmon the source of the huge river is the Clear Spring kick the ball straight and follow through help the women get back to her feet the pot of tea helps to pass the evening Smoky fires lack flame and Heat the soft cushion broke the man's fault the salt Breeze came across the sea the girl at the booth sold 50 bonds".lower(), "Google Cloud speech recognizer is not working at baseline levels."
