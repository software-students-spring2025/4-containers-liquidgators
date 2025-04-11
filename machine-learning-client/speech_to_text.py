# ignoring f-string pylint error, as line 36 cannot be an f-string
# pylint: disable=consider-using-f-string

# assuming we get a .wav or.flac or other audio file as output of getUserMedia()
import os
import speech_recognition as sr  # pylint: disable=import-error
from pymongo import MongoClient  # pylint: disable=import-error

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
sentence_collection = db["sentences"]
audio_collection = db["audio_files"]

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

CREDENTIAL_PATH = (
    "machine-learning-client/swe-project-4-liquid-gators-32c5eea1d351.json"
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

## need to test


class SpeechToText:
    """
    A machine learning client that transforms user speech input
    to text output that will be displayed on the web app, as well as
    text input to speech output.

    Uses Google Cloud Speech to Text (through Speech Recognition) and
    Google Cloud Text-to-Speech.
    """

    def initialize(self):
        """
        Initializes Google Cloud Speech Recognizer.
        """
        # create recognizer
        r = sr.Recognizer()
        return r

    def read_user_inp(self, r):
        """
        Reads in user audio as an AudioFile.
        """
        # using user's un-britishified audio
        audio_file = sentence_collection.find_one({"translated": False})

        if audio_file is not None:
            user_inp = sr.AudioFile(str(audio_file["audio"]))
            with user_inp as source:
                audio = r.record(source)  # records data into AudioData instance
        else:
            print("Could not find audio file. Please try again.")
            return None

        return audio

    def speech_recognition(self, audio, r):
        """
        Performs speech recognition and puts user text into database.
        """
        try:
            print("I think you said: " + r.recognize_google_cloud(audio))
            # r.recognize_google_cloud(audio) is the text output of the audio file
            # Store into original_sentence DB
            original_text_from_api = r.recognize_google_cloud(audio)
            sentence_collection.insert_one(
                {"original_sentence": original_text_from_api, "britishified": "NONE"}
            )
        except sr.UnknownValueError:
            print("Sorry, could you say that again?")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Cloud Speech service; {0}".format(
                    e
                )
            )


# run
sp_to_text = SpeechToText()
recognizer = sp_to_text.initialize()
user_audio = sp_to_text.read_user_inp(recognizer)
sp_to_text.speech_recognition(user_audio, recognizer)
