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
    u = None
    for user in users:
        if position.id == user.uid:
            found = True
            user.last_location = loc
            u = user
            proximity = detect_proximity(u)
            if proximity[0] == True:
                uids = []
                for user in proximity[1]:
                    uids.append(user.uid)
                    detect_interaction(u, user)
                for toople in u.ongoing_interactions:
                    if toople[0] not in uids:
                        print("suntem aproape sa stergem interactiunea")
                        ongoing_interactions[toople[1]].end()
            else:
                print("found user with no proximity")
                for i in ongoing_interactions:
                    if u.uid in i.uids:
                        i.end()
    if not found:
        u = User(uid=position.id, last_location=loc)
        users.append(u)
        proximity = detect_proximity(u)
        if proximity[0] == True:
            for user in proximity[1]:
                detect_interaction(u, user)


def detect_proximity(u):
    proximities = []
    for user in users:
        if user.uid == u.uid:
            continue
        if distance.distance(u.last_location.toople(), user.last_location.toople()).m < 5.0:
            proximities.append(user)
    if len(proximities) > 0:
        return True, proximities
    return False, False


def detect_interaction(user1, user2):
    for i in ongoing_interactions:
        if collections.Counter(i.uids) == collections.Counter([user1.uid, user2.uid]):
            i.updates[str(user1.uid)] = user1.last_location.time
            return
    i = Interaction(user1, user2)


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
    deal_with_it(pos)
    return {"data": {"message": "position registered"}, "error": None}


@ router.post("/start099441271933")
async def start_model():
    while True:
        print("Din start suntem ", len(users))
        time.sleep(10)
