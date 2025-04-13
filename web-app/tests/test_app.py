"""
Tests for the Web App
"""

import pytest
from dotenv import load_dotenv

# from britishify import return_final_sentence, return_british_dict
from app import app  # pylint: disable=import-error
from unittest.mock import patch, MagicMock

load_dotenv()


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

@patch("app.audio_collection.insert_one")
@patch("app.sentence_collection.find_one")
def test_transcribe_route(mock_find_one, mock_insert_one, client):
    mock_find_one.return_value = {"original_sentence": "hello world", "britishified": "NONE"}
    response = client.post("/transcribe", data=b"fake_audio")
    assert response.status_code == 200
    assert response.json["transcription"] == "hello world"
    mock_insert_one.assert_called_once()

@patch("app.sentence_collection.find_one")
@patch("app.sentence_collection.update_one")
def test_britishify_route(mock_update_one, mock_find_one, client):
    mock_find_one.return_value = {
        "_id": "some_id",
        "original_sentence": "That dude is angry his drugstore eggplant is silly",
        "britishified": "NONE",
    }
    response = client.post("/britishify")
    assert response.status_code == 200
    assert "bloke" in response.json["britishify"]
    assert "pissed" in response.json["britishify"]
    assert "aubergine" in response.json["britishify"]
    assert "chemist" in response.json["britishify"]
    assert "daft" in response.json["britishify"]
    mock_update_one.assert_called_once()


# # these are mostly tests for audio!
# @pytest.fixture  # fixed tests, single params

# # Make sure output is a string
# def transcription_output_test(create_app):
#     result = output.transcribe()
#     assert isinstance(result, str)


# # Use output.mp3 and check if output is correctly turned into a string
# def transcription_audio_input_test(create_app):
#     assert (
#         (str(create_app.transcribe(output))).lower
#         == "i love crumpets, black tea, the queen, and all other things british. aluminium"
#     )

# # make sure no AMERICAN words make it out 🔫
# def sentence_test(create_app):
#     sence = return_final_sentence().__contains__(return_british_dict().keys())
#     assert sence == False
