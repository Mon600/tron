import pytest
from unittest.mock import AsyncMock, MagicMock
from services.service import Service
from pydentic_schemas.schemas import InfoSchema, HistorySchema



@pytest.mark.asyncio
async def test_service_get_info_success(mock_repository, mock_async_tron_client):

    address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"

    mock_async_tron_client.get_account_balance.return_value = 100
    mock_async_tron_client.get_bandwidth.return_value = 500
    mock_async_tron_client.get_account_resource.return_value = {"EnergyLimit": 200}
    mock_repository.save.return_value = True # save возвращает True при успехе

    service = Service(repoistory=mock_repository, client=mock_async_tron_client)
    info = await service.get_info(address)
    mock_async_tron_client.get_account_balance.assert_called_once_with(addr=address)
    mock_async_tron_client.get_bandwidth.assert_called_once_with(addr=address)
    mock_async_tron_client.get_account_resource.assert_called_once_with(addr=address)
    mock_repository.save.assert_called_once_with(address)

    assert isinstance(info, InfoSchema)
    assert info.address == address
    assert info.balance == 100
    assert info.bandwidth == 500
    assert info.energy == 200


@pytest.mark.asyncio
async def test_service_get_info_tron_client_error(mock_repository, mock_async_tron_client):
    mock_async_tron_client.get_account_balance.side_effect = Exception("Tron API connectivity issue")
    address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"

    service = Service(repoistory=mock_repository, client=mock_async_tron_client)

    with pytest.raises(ValueError, match="Error getting info: Tron API connectivity issue"):
        await service.get_info(address)

    mock_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_service_get_info_repository_save_error(mock_repository, mock_async_tron_client):
    mock_repository.save.side_effect = ValueError("Database save failed during info retrieval")
    address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"

    service = Service(repoistory=mock_repository, client=mock_async_tron_client)

    with pytest.raises(ValueError, match="Error getting info: Database save failed during info retrieval"):
        await service.get_info(address)

    mock_repository.save.assert_called_once_with(address) # Вызывается, но выбрасывает ошибку


@pytest.mark.asyncio
async def test_service_get_history_success(mock_repository, mock_async_tron_client):
    mock_repository.get_history.return_value = [
        MagicMock(address="TXYZ789"),
        MagicMock(address="TABC012")
    ]
    service = Service(repoistory=mock_repository, client=mock_async_tron_client)
    limit = 2

    history_list = await service.get_history(limit)

    mock_repository.get_history.assert_called_once_with(limit)
    assert len(history_list) == 2
    assert isinstance(history_list[0], HistorySchema)
    assert history_list[0].address == "TXYZ789"
    assert history_list[1].address == "TABC012"


@pytest.mark.asyncio
async def test_service_get_history_repository_error(mock_repository, mock_async_tron_client):
    mock_repository.get_history.side_effect = ValueError("Repository query error")
    service = Service(repoistory=mock_repository, client=mock_async_tron_client)
    limit = 5

    with pytest.raises(ValueError, match="Error getting history: Repository query error"):
        await service.get_history(limit)

    mock_repository.get_history.assert_called_once_with(limit)