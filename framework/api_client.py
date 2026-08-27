import logging
from typing import Any

import requests

from config.settings import settings
from framework.retry import transient_retry

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str = settings.api_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    @transient_retry(settings.retries + 1)
    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.info("%s %s", method.upper(), url)
        response = self.session.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        return response

    def get_rooms(self) -> dict[str, Any]:
        return self.request("GET", "/api/room").json()

    def get_room(self, room_id: str) -> dict[str, Any]:
        return self.request("GET", f"/api/room/{room_id}").json()

