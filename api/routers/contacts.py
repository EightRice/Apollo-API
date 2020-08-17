from typing import Dict, List
from fastapi import APIRouter
from pydantic import BaseModel
from config.db import positions
from config.db import users
from config.db import interactions
from config.db import ongoing_interactions
from geopy.distance import geodesic
from multiprocessing import Process
from geopy import distance
import time
import pandas as pd
from service.entities.user import User
from service.entities.interaction import Interaction
import collections
router = APIRouter()


class Loc:
    def __init__(self, latitude, longitude, time, uid):
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.uid = uid

    def get_user(self, uid):
        for user in users:
            if user.uid == self.uid:
                return user

    def toople(self):
        return (self.latitude, self.longitude)


class Position(BaseModel):
    id: str
    location: Dict
    networks: List


def deal_with_it(position):
    loc = Loc(position.location['latitude'],
              position.location['longitude'], position.location['time'], position.id)
    found = False
    for user in users:
        if position.id == user.uid:
            found = True
            user.last_location = loc
            return "Old user " + detect_proximity(loc)
    if not found:
        users.append(User(uid=position.id, last_location=loc))
        return "new user " + detect_proximity(loc)


def detect_proximity(loc):
    for user in users:
        if user.uid == loc.uid:
            continue
        if distance.distance(loc.toople(), user.last_location.toople()).m < 5.0:
            return " proximity FOUND "+detect_interaction(loc.uid, user.uid, loc.time)
    return "no proximity"


def detect_interaction(uid1, uid2, start_time):
    for i in ongoing_interactions:
        if collections.Counter(i.uids) == collections.Counter([uid1, uid2]):

            return " ongoing interaction "
    ongoing_interactions.append(Interaction(uid1, uid2, start_time))
    return " new interaction "


@ router.get("/users")
async def get_users():
    return {"data": users, "error": None}


@ router.get("/ongoing")
async def get_ongoing():
    return {"data": ongoing_interactions, "error": None}


@ router.get("/interactions")
async def get_interactions():
    return {"data": interactions, "error": None}


@ router.post("/positions")
async def post_contacts(pos: Position):
    print("Position from ", pos.id, ", at time (ms): ",
          pos.location['time'], ":", pos.location['longitude'], " ", pos.location['latitude'])
    aloneOrNot = deal_with_it(pos)
    return {"data": {"message": aloneOrNot}, "error": None}
