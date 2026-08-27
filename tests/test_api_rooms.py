import allure
import pytest

from test_framework.api_client import ApiClient


@pytest.mark.api
@pytest.mark.smoke
@allure.title("Rooms API returns room collection")
def test_rooms_api_returns_expected_shape():
    payload = ApiClient().get_rooms()
    assert isinstance(payload.get("rooms"), list)


@pytest.mark.api
@allure.title("Room API returns a known room")
def test_room_api_returns_room_details(rooms_data):
    rooms = ApiClient().get_rooms()["rooms"]
    assert rooms
    assert set(rooms_data["expected_room_keys"]).issubset(rooms[0])


@pytest.mark.api
@allure.title("Rooms API returns at least one room")
def test_rooms_api_is_not_empty():
    assert ApiClient().get_rooms()["rooms"]


@pytest.mark.api
@allure.title("Rooms API returns named rooms")
def test_rooms_api_rooms_have_names():
    rooms = ApiClient().get_rooms()["rooms"]
    assert all(room.get("roomName") for room in rooms)


@pytest.mark.api
@allure.title("Rooms API returns positive room prices")
def test_rooms_api_prices_are_positive():
    rooms = ApiClient().get_rooms()["rooms"]
    assert all(room.get("roomPrice", 0) > 0 for room in rooms)
