"""
A machine learning client that transforms user speech input
to text output that will be displayed on the web app, as well as
text input to speech output.

Uses Google Cloud Speech to Text (through Speech Recognition) and
Google Cloud Text-to-Speech.
"""

# ignoring f-string pylint error, as line 36 cannot be an f-string

# pylint: disable=consider-using-f-string

# assuming we get a .wav or.flac or other audio file as output of getUserMedia()
import os
import io
import tempfile
import speech_recognition as sr

# from google.cloud import texttospeech
from pymongo import MongoClient
from pydub import AudioSegment

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client["project4_liquidgators_1"]
sentence_collection = db["sentences"]
audio_collection = db["audioFiles"]

# DB formatted like this:
# {
#  id: blah_blah,
#  original_sentence: "mom",
#  britishified: "mum"
# }

# {
#  id: blah_blah,
#  audio: "audio.mp3",
#  translated: False
# }

# CREDENTIAL_PATH = "swe-project-4-liquid-gators-32c5eea1d351.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

# create recognizer
r = sr.Recognizer()


def process_audio(
    audio_collection, sentence_collection, recognizer
):  # pylint: disable=redefined-outer-name disable=unused-argument
    """Func to process audio"""
    audio_file = audio_collection.find_one({"translated": False})

    if audio_file:
        # checkForAudio = True
        audio_data = audio_file["audio"]  # records data into AudioData instance
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_segment.export(tmp, format="wav")
            wav_path = tmp.name

        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)

        audio_inner(audio, audio_file, sentence_collection, audio_collection)


def audio_inner(audio, audio_file, sentence_collection, audio_collection):
    """Func to return transcription"""
    try:
        print("I think you said: " + r.recognize_google_cloud(audio))
        # r.recognize_google_cloud(audio) is the text output of the audio file
        # Store into original_sentence DB
        sentence_collection.insert_one(
            {
                "original_sentence": r.recognize_google_cloud(audio),
                "britishified": "NONE",
            }
        )

        audio_collection.update_one(
            {"_id": audio_file["_id"]}, {"$set": {"translated": True}}
        )
    except sr.UnknownValueError:
        print("Sorry, could you say that again?")


def main():
    """main func"""
    while True:
        process_audio(audio_collection, sentence_collection, r)


if __name__ == "__main__":
    main()
