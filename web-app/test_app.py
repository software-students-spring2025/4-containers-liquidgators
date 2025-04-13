import pytest
from . import create_app
from . import britishify
from .. import output

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
    sence = create_app.britishify.NEW_SENTENCE.__contains__(britishify.britishConv.keys())
    assert sence == False
