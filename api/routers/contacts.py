from typing import Dict
from fastapi import APIRouter
from pydantic import BaseModel
from config.db import connection

router = APIRouter()


class Interaction(BaseModel):
    location: Dict
    networks: Dict


@router.get("/interactions")
async def get_contacts():
    return {"data": {"message": "interactions"}, "error": None}


@router.post("/interactions")
async def post_contacts(interactions: Interaction):
    # connection.insert_many()
    print(interactions)
    return {"data": {"message": "Interactions stored successfully"}, "error": None}
