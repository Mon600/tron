from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron, AsyncTron
from tronpy.providers import AsyncHTTPProvider

from db.repository import Repository
from services.service import Service
from settings import async_session, get_api_key


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            raise e
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_client() -> Tron:
    async with AsyncTron(AsyncHTTPProvider(
            "https://api.trongrid.io",
            api_key=get_api_key())) as client:
        try:
            yield client
        except Exception as e:
            raise e
        finally:
            await client.close()


ClientDep = Annotated[AsyncTron, Depends(get_client)]


async def get_repository(session: SessionDep):
    return Repository(session)

RepositoryDep = Annotated[Repository, Depends(get_repository)]


async def get_service(repository: RepositoryDep,client: ClientDep):
    return Service(repository, client)

ServiceDep = Annotated[Service, Depends(get_service)]
