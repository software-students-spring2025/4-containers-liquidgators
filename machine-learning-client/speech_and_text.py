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
import speech_recognition as sr  # pylint: disable=import-error
from google.cloud import texttospeech  # pylint: disable=import-error

CREDENTIAL_PATH = "swe-project-4-liquid-gators-32c5eea1d351.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH


class Speech_and_Text:
    def initialize(self):
        # create recognizer
        r = sr.Recognizer()
        return r

    def read_user_inp(self, audio_file_name, recognizer):
        # using example audio file for now
        user_inp = sr.AudioFile(audio_file_name)
        with user_inp as source:
            audio = recognizer.record(source)  # records data into AudioData instance

        return audio

    def speech_recognition(self, audio):
        try:
            user_text = r.recognize_google_cloud(audio)
            print("I think you said: " + user_text)
        except sr.UnknownValueError:
            print("Sorry, could you say that again?")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Cloud Speech service; {0}".format(
                    e
                )
            )

        return user_text


# run
sp_to_text = Speech_and_Text()
r = sp_to_text.initialize()

# assign user audio file name
user_audio_file_str = "machine-learning-client/OSR_us_000_0011_8k.wav"
user_audio = sp_to_text.read_user_inp(user_audio_file_str, r)
user_text = sp_to_text.speech_recognition(user_audio)


