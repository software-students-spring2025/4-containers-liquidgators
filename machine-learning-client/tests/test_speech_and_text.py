"""
Unit testing file using pytest for ML client.
"""

import os
import re
import pytest

# import speech_to_text
import speech_recognition as sr  # pylint: disable=import-error

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

CREDENTIAL_PATH = """swe-project-4-liquid-gators-32c5eea1d351.json"""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

"""client = MongoClient(mongo_uri)
db = client.get_database()
sentence_collection = db["sentences"]
audio_collection = db["audio_files"]"""


@pytest.fixture(scope="module")
def test_initialize():
    """
    Tests initialization of Google Cloud Speech Recognizer.
    """
    # create recognizer
    r = sr.Recognizer()
    assert isinstance(
        r, sr.Recognizer
    ), "Current recognizer is not an instance of sr.Recognizer."


@pytest.mark.parametrize("test_audio_file", ["OSR_us_000_0011_8k.wav"])
def test_read_user_inp(test_audio_file):
    """
    Tests reading in of user audio as an AudioFile.
    """
    r = sr.Recognizer()
    # using user's un-britishified audio
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance
    assert audio is not None, "AudioData instance cannot be None."


@pytest.mark.parametrize("test_audio_file", ["OSR_us_000_0011_8k.wav"])
def test_speech_recognition(test_audio_file):
    """
    Tests if Google Cloud speech recognizer performs at baseline levels.
    """
    r = sr.Recognizer()
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance
    user_text = r.recognize_google_cloud(audio)

    def normalize(text):
        return re.sub(r"\s+", " ", text.strip().lower())

    expected_text = """
    the boy was there when the sun rose a rod is used to catch
    pink salmon the source of the huge river is the clear spring kick 
    the ball straight and follow through help the women get back to her feet
    the pot of tea helps to pass the evening smoky fires lack flame and
    heat the soft cushion broke the man's fault the salt breeze came across 
    the sea the girl at the booth sold 50 bonds
    """

    assert normalize(user_text) == normalize(
        expected_text
    ), f"""Google Cloud speech recognizer is not working at baseline levels.
    Expected: {normalize(expected_text)}
    Got: {normalize(user_text)}"""
