import allure
import pytest

from framework.api_client import ApiClient


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
