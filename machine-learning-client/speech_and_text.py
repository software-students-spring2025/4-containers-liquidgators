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
import speech_recognition as sr  

# from google.cloud import texttospeech  
from pymongo import MongoClient  
from pydub import AudioSegment
import tempfile

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
sentence_collection = db.sentences
audio_collection = db.audioFiles

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

CREDENTIAL_PATH = "swe-project-4-liquid-gators-32c5eea1d351.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

# create recognizer
r = sr.Recognizer()

# testing speech recognition with Google Cloud Speech Recognition + example audio file
# find audio from mongoDB
while True:
    audio_file = audio_collection.find_one({"translated": False})

    if audio_file:
        audio_data = audio_file["audio"]  # records data into AudioData instance
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio_segment.export(tmp, format="wav")
                wav_path = tmp.name

        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)

        try:
            print("I think you said: " + r.recognize_google_cloud(audio))
            # r.recognize_google_cloud(audio) is the text output of the audio file
            # Store into original_sentence DB
            original_text_from_API = r.recognize_google_cloud(audio)
            sentence_collection.insert_one(
                {
                    "original_sentence": r.recognize_google_cloud(audio),
                    "britishified": "NONE",
                }
            )

            audio_collection.update_one({
                 "id" : audio_file["id"],
                 "$set": {"translated": True}
            })
        except sr.UnknownValueError:
            print("Sorry, could you say that again?")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Cloud Speech service; {0}".format(
                    e
                )
            )

# ### british-ifying user input will happen here

# # testing text to speech with Google Cloud TTS + example input

# client = texttospeech.TextToSpeechClient()
# SAMPLE_TEXT = (
#     "I love crumpets, black tea, the Queen, and all other things British. Aluminium."
# )

# # set text input
# synthesis_input = texttospeech.SynthesisInput(text=SAMPLE_TEXT)

# # select parameters for British-accented voice (accent, gender)
# voice = texttospeech.VoiceSelectionParams(
#     language_code="en-GB", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
# )

# # config audio output file
# audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# # perform the text-to-speech request
# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )

# with open("output.mp3", "wb") as out:
#     # writes to output file, stored in app repo
#     out.write(response.audio_content)
