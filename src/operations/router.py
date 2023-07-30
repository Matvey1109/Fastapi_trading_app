import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.operations.models import Operation
from src.operations.schemas import OperationCreate
from src.auth.models import User
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


@router.get("/get_all_users")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User)
        result = await session.execute(query)
        column_names = result.keys()
        users = [dict(zip(column_names, row)) for row in result]
        data = [{f"user №{str(us['id'])}": us} for us in users]
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


@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
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
    stmt = insert(Operation).values(**new_operation.model_dump())
    await session.execute(stmt)
    # For execute transaction
    await session.commit()
    return {"status": "success"}


@router.delete("")
async def del_specific_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Operation).where(Operation.id == operation_id)
    result = await session.execute(stmt)
    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "status": "error",
            "data": None,
            "details": "Operation not found"
        })
    await session.commit()
    return {"status": "success"}
