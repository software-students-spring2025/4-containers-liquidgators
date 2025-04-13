import pytest
from __init__ import create_app
import britishify
from britishify import return_british_dict, return_final_sentence
from .. import output;

# these are mostly tests for audio!
@pytest.fixture # fixed tests, single params

# Make sure output is a string
def transcription_output_test(create_app):
    assert create_app.transcribe() == type.__str__

# Use output.mp3 and check if output is correctly turned into a string
def transcription_audio_input_test(create_app):
    assert (str(create_app.transcribe(output))).lower == "i love crumpets, black tea, the queen, and all other things british. aluminium"
    
# make sure no AMERICAN words make it out 🔫
def sentence_test(create_app):
    sence = return_final_sentence().__contains__(return_british_dict().keys())
    assert sence == False
