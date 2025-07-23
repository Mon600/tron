import pytest
import httpx
from main import app
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_api_get_info_success(client: httpx.AsyncClient, mock_service: AsyncMock):
    test_address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"
    response = await client.post("/get-info", json={"address": test_address})

    assert response.status_code == 200
    data = response.json()
    assert data["address"] == test_address
    assert data["balance"] == 1000
    assert data["bandwidth"] == 500
    assert data["energy"] == 200

    mock_service.get_info.assert_called_once_with(test_address)


@pytest.mark.asyncio
async def test_api_get_info_invalid_address_validation_error(client: httpx.AsyncClient):
    response = await client.post("/get-info", json={"address": "invalid_format"})

    assert response.status_code == 422
    assert "value_error" in response.json()["detail"][0]["type"]


@pytest.mark.asyncio
async def test_api_get_history_success(client: httpx.AsyncClient, mock_service: AsyncMock):
    mock_service.get_history.return_value = [
        MagicMock(address="TXYZ123_hist", id=1),
        MagicMock(address="TABC456_hist", id=2)
    ]

    response = await client.get("/get-history?records=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["address"] == "TXYZ123_hist"
    assert data[1]["address"] == "TABC456_hist"

    mock_service.get_history.assert_called_once_with(2)


@pytest.mark.asyncio
async def test_api_get_history_default_limit(client: httpx.AsyncClient, mock_service: AsyncMock):
    mock_service.get_history.return_value = [
        MagicMock(address=f"addr_{i}", id=i) for i in range(10)
    ]

    response = await client.get("/get-history")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    mock_service.get_history.assert_called_once_with(10)

