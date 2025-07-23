import pytest
from unittest.mock import AsyncMock, MagicMock

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import AsyncTron

from main import app
from api.dependencies.dependencies import get_session, get_client, get_repository, get_service
from db.repository import Repository
from services.service import Service
from db.models import HistoryModel


@pytest.fixture
async def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    yield session


@pytest.fixture
async def mock_async_tron_client():
    client = AsyncMock(spec=AsyncTron)

    client.get_account_balance.return_value = 1000
    client.get_bandwidth.return_value = 500
    client.get_account_resource.return_value = {"EnergyLimit": 200}
    client.close = AsyncMock()
    yield client


@pytest.fixture
def mock_repository(mock_async_session):
    repo = AsyncMock(spec=Repository)

    repo.get_history.return_value = [
        MagicMock(spec=HistoryModel, address="TXYZ_mock_hist_1", id=1),
        MagicMock(spec=HistoryModel, address="TABC_mock_hist_2", id=2)
    ]
    return repo


@pytest.fixture
def mock_service(mock_repository, mock_async_tron_client):
    svc = AsyncMock(spec=Service)
    svc.get_info.return_value = MagicMock(
        address="TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN",
        balance=1000,
        bandwidth=500,
        energy=200
    )
    svc.get_history.return_value = [
        MagicMock(address="TXYZ_mock_hist_1", id=1),
        MagicMock(address="TABC_mock_hist_2", id=2)
    ]
    return svc


@pytest.fixture(autouse=True)
def override_fastapi_dependencies(
    mock_async_session,
    mock_async_tron_client,
    mock_repository,
    mock_service
):
    app.dependency_overrides[get_session] = lambda: mock_async_session
    app.dependency_overrides[get_client] = lambda: mock_async_tron_client
    app.dependency_overrides[get_repository] = lambda: mock_repository
    app.dependency_overrides[get_service] = lambda: mock_service
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
async def client():
    BASE_URL = "http://test"
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BASE_URL
    ) as client:
        yield client