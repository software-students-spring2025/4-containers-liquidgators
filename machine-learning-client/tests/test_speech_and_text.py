"""
Unit testing file using pytest for ML client.
"""

import os
import re
from unittest import mock
from unittest.mock import patch, MagicMock
import pytest
from pymongo.collection import Collection
# import speech_to_text
import speech_recognition as sr  # pylint: disable=import-error
from speech_and_text import process_audio
from speech_and_text import audio_inner

#import speech_and_text  # pylint: disable=unused-import

mongo_uri = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("MONGO_DB")

# CREDENTIAL_PATH = """swe-project-4-liquid-gators-32c5eea1d351.json"""
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

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
    test_path = os.path.join(os.path.dirname(__file__), test_audio_file)
    r = sr.Recognizer()
    # using user's un-britishified audio
    user_inp = sr.AudioFile(test_path)
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


# Test with nothing
def test_process_audio_no_audio():
    """Test with no audio"""
    mock_audio_collection = mock.Mock(spec=Collection)
    mock_sentence_collection = mock.Mock(spec=Collection)
    recognizer = sr.Recognizer()

    mock_audio_collection.find_one.return_value = None

    process_audio(mock_audio_collection, mock_sentence_collection, recognizer)

    mock_sentence_collection.insert_one.assert_not_called()
    mock_audio_collection.update_one.assert_not_called()


@mock.patch(
    "speech_recognition.Recognizer.recognize_google_cloud",
    side_effect=sr.RequestError("API unreachable"),
)
def test_mocked_request_error(mock_recognize):  # pylint: disable=unused-argument
    """Test for request err"""
    r = sr.Recognizer()
    audio = mock.Mock()
    with pytest.raises(sr.RequestError):
        r.recognize_google_cloud(audio)


@pytest.mark.parametrize("test_audio_file", ["Silent.wav"])
def test_unknown_value_error(test_audio_file):
    """Test for unknown val err"""
    r = sr.Recognizer()
    with sr.AudioFile(test_audio_file) as source:
        audio = r.record(source)  # records data into AudioData instance

    with pytest.raises(sr.UnknownValueError):
        r.recognize_google_cloud(audio)


@pytest.mark.parametrize("test_audio_file", ["OSR_us_000_0011_8k.wav"])
def test_process_audio_print(test_audio_file):
    """Test audio print"""
    r = sr.Recognizer()
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance

    mock_audio_collection = MagicMock()

    mock_audio_collection.find_one.return_value = {"audio": audio, "translated": False}

    mock_audio_doc = {"_id": "fake_id_for_test", "audio": audio, "translated": False}
    mock_audio_collection.find_one.return_value = mock_audio_doc

    audio_inner(audio, mock_audio_doc)


@pytest.mark.parametrize("test_audio_file", ["Silent.wav"])
@patch("builtins.print")
@patch("speech_recognition.Recognizer.recognize_google_cloud")
def test_process_audio_print_unknown(
    mock_recognize_google_cloud, mock_print, test_audio_file
):
    """Test audio print with no transcription"""
    r = sr.Recognizer()
    user_inp = sr.AudioFile(test_audio_file)
    with user_inp as source:
        audio = r.record(source)  # records data into AudioData instance

    mock_recognize_google_cloud.side_effect = sr.UnknownValueError()

    mock_audio_doc = {"_id": "fake_id_for_test", "audio": audio, "translated": False}

    audio_inner(audio, mock_audio_doc)

    mock_print.assert_any_call("Sorry, could you say that again?")


@pytest.mark.parametrize("test_audio_file", ["tests/OSR_us_000_0011_8k.wav"])
def test_process_process_audio(test_audio_file):
    """Test process audio"""
    r = sr.Recognizer()
    mock_audio_collection = MagicMock()
    mock_sentence_collection = MagicMock()

    with open(test_audio_file, "rb") as f:
        audio_bytes = f.read()

    mock_audio_collection.find_one.return_value = {
        "_id": "some_id",
        "audio": audio_bytes,
        "translated": False,
    }

    process_audio(mock_audio_collection, mock_sentence_collection, r)
