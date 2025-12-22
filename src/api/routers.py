from fastapi import APIRouter

router = APIRouter(tags=["test"])


@router.get("/examples")
async def get_examples():
    return {200: "ok"}
