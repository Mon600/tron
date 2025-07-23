from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from db.models import HistoryModel
from db.repository import Repository


@pytest.mark.asyncio
async def test_repository_save_success(mock_async_session):
    repository = Repository(session=mock_async_session)
    address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"

    result = await repository.save(address)

    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_called_once()
    assert result is True


@pytest.mark.asyncio
async def test_repository_save_failure_rollback(mock_async_session):
    mock_async_session.commit.side_effect = SQLAlchemyError("Database write failed")
    repository = Repository(session=mock_async_session)
    address = "TR7NHqjeConjfnaFqLgHhP8G7uA4g9rTcN"

    with pytest.raises(ValueError, match="Database save error: Database write failed"):
        await repository.save(address)

    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_called_once()
    mock_async_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_repository_get_history_success(mock_async_session):
    mock_records = [
        HistoryModel(id=1, address="TXYZ123"),
        HistoryModel(id=2, address="TABC456")
    ]
    mock_session_result = MagicMock()
    mock_session_result.scalars.return_value.all.return_value = mock_records
    mock_async_session.execute.return_value = mock_session_result

    repository = Repository(session=mock_async_session)
    limit = 2

    history = await repository.get_history(limit)

    mock_async_session.execute.assert_called_once()
    assert len(history) == 2
    assert history[0].address == "TXYZ123"
    assert history[1].address == "TABC456"


@pytest.mark.asyncio
async def test_repository_get_history_failure(mock_async_session):
    mock_async_session.execute.side_effect = SQLAlchemyError("Database read failed")
    repository = Repository(session=mock_async_session)
    limit = 10

    with pytest.raises(ValueError, match="Database query error: Database read failed"):
        await repository.get_history(limit)

    mock_async_session.execute.assert_called_once()
