from fastapi import APIRouter

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.get("/")
async def get_operations():
    return {"message": "check"}
