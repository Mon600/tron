from tronpy import AsyncTron

from db.repository import Repository
from pydentic_schemas.schemas import InfoSchema, HistorySchema


class Service:
    def __init__(self, repoistory: Repository, client: AsyncTron):
        self.repository = repoistory
        self.client = client

    async def get_info(self, address: str) -> InfoSchema:
        try:
            balance = await self.client.get_account_balance(addr=address)
            bandwidth = await self.client.get_bandwidth(addr=address)
            energy = await self.client.get_account_resource(addr=address)
            await self.repository.save(address)

            return InfoSchema(
                address=address,
                balance=balance,
                bandwidth=bandwidth,
                energy=energy.get("EnergyLimit", 0)
            )
        except Exception as e:
            # Вместо возврата False бросаем исключение
            raise ValueError(f"Error getting info: {str(e)}")

    async def get_history(self, limit: int = 10) -> list[HistorySchema]:
        try:
            res = await self.repository.get_history(limit)
            return [HistorySchema.model_validate(item) for item in res]
        except Exception as e:
            raise ValueError(f"Error getting history: {str(e)}")