import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, Mock

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app, fetch_users
client = TestClient(app)

mock_api_response = {
    "results": [
        {
            "gender": "female",
            "name": {"first": "Jane", "last": "Doe"},
            "phone": "123-456-7890",
            "email": "jane.doe@example.com",
            "location": {"city": "Springfield", "country": "USA"},
            "picture": {"thumbnail": "http://example.com/image.jpg"}
        }
    ]
}

@pytest.mark.asyncio
@patch("services.httpx.AsyncClient.get")
async def test_fetch_users(mock_get):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    # Здесь .json() — простой Mock, возвращает словарь сразу
    mock_response.json = Mock(return_value=mock_api_response)

    mock_get.return_value = mock_response

    users = await fetch_users(1)
    assert len(users) == 1
    user = users[0]
    assert user.first_name == "Jane"
    assert user.last_name == "Doe"
    assert user.city == "Springfield"


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Random Users" in response.text

def test_random_user_detail_page_structure():
    response = client.get("/random")
    assert response.status_code == 200
    html = response.text

    # Проверяем, что шаблон корректно отработал и выдал ключевые поля
    assert "<h1>User Detail</h1>" in html
    assert '<div class="user-card">' in html
    assert "<strong>Name:</strong>" in html
    assert "<strong>Gender:</strong>" in html
    assert "<strong>Phone:</strong>" in html
    assert "<strong>Email:</strong>" in html
    assert "<strong>Location:</strong>" in html
    assert '<img src="' in html
    assert 'alt="User Photo"' in html
    assert '<a href="/">Back to list</a>' in html



def test_user_detail_not_found():
    response = client.get("/999999")
    assert response.status_code == 404
