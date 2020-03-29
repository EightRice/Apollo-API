from fastapi import APIRouter

router = APIRouter()


@router.get("/interactions")
async def get_contacts():
    return {"data": {"message": "interactions"}, "error": None}


@router.post("/interactions")
async def post_contacts():
    return {"data": {"message": "Interactions stored successfully"}, "error": None}
