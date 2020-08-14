from typing import Dict, List
from fastapi import APIRouter
from pydantic import BaseModel
from config.db import connection

router = APIRouter()

class Interaction(BaseModel):
    id: int
    location: Dict
    networks: List


@router.get("/interactions")
async def get_contacts():
    return {"data": connection, "error": None}


@router.post("/interactions")
async def post_contacts(interactions: Interaction):
    connection.append(interactions)
    return {"data": {"message": "ultima data era asa"}, "error": None}
