from fastapi import APIRouter, HTTPException

from api.dependencies.dependencies import ServiceDep
from pydentic_schemas.schemas import AddressRequest, InfoSchema, HistorySchema

router = APIRouter()

@router.post('/get-info')
async def get_info(address: AddressRequest, service: ServiceDep) -> InfoSchema:
    res = await service.get_info(address.address)
    return res

@router.get('/get-history')
async def get_history(service: ServiceDep, records: int = 10) -> list[HistorySchema]:
    result = await service.get_history(records)
    return result
