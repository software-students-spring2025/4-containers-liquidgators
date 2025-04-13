"""
Tests for the Web App
"""

import pytest
from app import app  # pylint: disable=import-error
import pytest
#from app import create_app
#from britishify import return_british_dict, return_final_sentence
#from .. import output

@pytest.fixture
def client():  # pylint: disable=redefined-outer-name
    """Fixture for making test app."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index(client):  # pylint: disable=redefined-outer-name
    "Test that root leads to the index"
    response = client.get("/")
    assert response.status_code == 200


def test_history_exists(client):  # pylint: disable=redefined-outer-name
    "Test that history page exists"
    response = client.get("/history")
    assert response.status_code == 200


def test_converter_exists(client):  # pylint: disable=redefined-outer-name
    "Test that converter page exists"
    response = client.get("/converter")
    assert response.status_code == 200

# # these are mostly tests for audio!
# @pytest.fixture # fixed tests, single params

# # Make sure output is a string
# def transcription_output_test(create_app):
#     result = output.transcribe()
#     assert isinstance(result, str)

# # Use output.mp3 and check if output is correctly turned into a string
# def transcription_audio_input_test(create_app):
#     assert (str(create_app.transcribe(output))).lower == "i love crumpets, black tea, the queen, and all other things british. aluminium"
    
# # make sure no AMERICAN words make it out 🔫
# def sentence_test(create_app):
#     sence = return_final_sentence().__contains__(return_british_dict().keys())
#     assert sence == False
