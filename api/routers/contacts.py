from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_contacts():
    pass


@router.post("/")
async def post_contacts():
    pass
