from fastapi import APIRouter

router = APIRouter()

@router.get("/contacts")
async def get_contacts():
    return {"hello": "world"}


@router.post("/contacts")
async def post_contacts():
    return {"hello": "world"}
