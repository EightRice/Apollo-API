from typing import Dict, List
from fastapi import APIRouter
from pydantic import BaseModel
from config.db import positions
from config.db import users
from geopy.distance import geodesic
from multiprocessing import Process
from geopy import distance
import time
import pandas as pd
router = APIRouter()

class User:
    def __init__(self,uid):
        self.uid=name
        self.risk=0
        self.last_location=(0,0,0)
    def to_dict(self):
        return {
            'name': self.name,
            'risk':self.risk,
            'last_location':self.last_location
        }
class Loc:
    def __init__(self,latitude,longitude,time):
        self.latitude=latitude
        self.longitude=longitude
        self.time=time
    def toople(self):
        return (self.latitude,self.longitude,self.time)

class Position(BaseModel):
    id: str
    location: Dict
    networks: List
    

def deal_with_it(position):
    loc=Loc(position.location['latitude'],position.location['longitude'],position.location['time'])
    gasit=False
    for user in users:
        if position.id==user.id:
            gasit=True
            user.last_location=loc.toople()
    if not gasit:
        users.append(User(uid=position.id,last_location=loc.toople()))
    

@router.get("/positions")
async def get_contacts():
    return {"data": positions, "error": None}

@router.post("/positions")
async def post_contacts(pos:Position):
    print("Position received from ",pos.id, ", at time (ms): ", pos.location['longitude']," ", pos.location['latitude'])
    aloneOrNot=deal_with_it(pos)
    return {"data": {"message": aloneOrNot}, "error": None}

