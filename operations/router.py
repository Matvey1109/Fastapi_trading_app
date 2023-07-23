from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    column_names = result.keys()
    data = [dict(zip(column_names, row)) for row in result]
    return data


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    # For execute transaction
    await session.commit()
    return {"status": "success"}
