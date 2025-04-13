"""
Tests for the Web App
"""

import pytest
from app import create_app  # pylint: disable=import-error


@pytest.fixture
def client():  # pylint: disable=redefined-outer-name
    """Fixture for making test app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        yield client


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
