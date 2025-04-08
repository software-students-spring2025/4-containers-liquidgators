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

# create recognizer
r = sr.Recognizer()

# testing speech recognition with Google Cloud Speech Recognition + example audio file
user_inp = sr.AudioFile("machine-learning-client/OSR_us_000_0011_8k.wav")

with user_inp as source:
    audio = r.record(source)  # records data into AudioData instance

try:
    print("I think you said: " + r.recognize_google_cloud(audio))
except sr.UnknownValueError:
    print("Sorry, could you say that again?")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))


### british-ifying user input will happen here

# testing text to speech with Google Cloud TTS + example input

client = texttospeech.TextToSpeechClient()
SAMPLE_TEXT = (
    "I love crumpets, black tea, the Queen, and all other things British. Aluminium."
)

# set text input
synthesis_input = texttospeech.SynthesisInput(text=SAMPLE_TEXT)

# select parameters for British-accented voice (accent, gender)
voice = texttospeech.VoiceSelectionParams(
    language_code="en-GB", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# config audio output file
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# perform the text-to-speech request
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("output.mp3", "wb") as out:
    # writes to output file, stored in app repo
    out.write(response.audio_content)
