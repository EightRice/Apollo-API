from uvicorn import run
from dynaconf import settings
from api.v1 import create_api
from config.db import interactions
from config.db import users
from config.db import uids
from requests import get
from requests import post
import pandas as pd
from service.entities.user import User
import json
import time
import _thread
server = create_api()

"""
1. Setup logger
2. Setup workers
3. Instantiate DB
4. Instantiate service (glue between worker API and DB)
5. Create server with reference to the service
6. Run server
"""


def heartbeat():
    global uids
    global users
    # retrieve users from firebase
    first = False
    while(True):
        print("Heartbeat activated")
        if first == False:
            response = get(
                "https://us-central1-viratrace-284223.cloudfunctions.net/getUsers")
            geison = json.loads(response.text)
            for i in geison:
                if i['uid'] not in uids:
                    u = User(uid=i['uid'], last_location=None)
                    uids.append(i['uid'])
                    u.risk = int(i['risk'])
                    users.append(u)
            else:
                u = next((x for x in users if x.uid == i['uid']), None)
                u.risk = int(i['risk'])

            # infection model
            for u in users:
                u.risk = u.risk+99

            # push updated risks back to firebase
            ordered_uids = []
            ordered_risks = []
            for u in users:
                ordered_uids.append(u.uid)
                ordered_risks.append(str(u.risk))
            pload = {"users": ordered_uids, "risks": ordered_risks}
            response = post(
                "https://us-central1-viratrace-284223.cloudfunctions.net/updateRisks", data=pload)
            print(response.text, response.status_code)
        print("Sleepy time")
        first = True
        time.sleep(1800)


if __name__ == "__main__":
    _thread.start_new_thread(heartbeat, ())
    print("starting server")
    host = settings.get("server_host")
    port = settings.get("server_port")
    run("main:server", host=host, port=port, log_level="info")
