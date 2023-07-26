import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


# expired - how many seconds data will be stored in Redis (cache)
@router.get("/long_operation")
@cache(expire=30)
def get_long_op(x: int):
    time.sleep(2)
    return x


@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        column_names = result.keys()
        data = [dict(zip(column_names, row)) for row in result]
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_specific_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    # For execute transaction
    await session.commit()
    return {"status": "success"}


@router.delete("")
async def del_specific_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(operation).where(operation.c.id == operation_id)
    result = await session.execute(stmt)
    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status": "error",
            "data": None,
            "details": "Operation not found"
        })
    await session.commit()
    return {"status": "success"}
