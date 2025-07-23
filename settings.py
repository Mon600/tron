import os

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


load_dotenv()


def get_db_url():
    return (f'postgresql+asyncpg://'
            f'{os.getenv("DB_USER")}:'
            f'{os.getenv("DB_PASSWORD")}@'
            f'{os.getenv("DB_HOST")}:'
            f'{os.getenv("DB_PORT")}/'
            f'{os.getenv("DB_NAME")}')



def get_api_key():
    return os.getenv('API_KEY')


engine = create_async_engine(
    url=get_db_url()
)


async_session = async_sessionmaker(engine, expire_on_commit=False)