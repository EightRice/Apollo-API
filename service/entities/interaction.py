from config.db import users


class Interaction:
    def __init__(self, uid1, uid2, start_time):
        self.ongoing = True
        self.uids = [uid1, uid2]
        self.start_time = start_time
        self.end_time = 0
        self.outdoor = True
        self.found1 = False
        self.distance = 1
        self.risks = {}

    def get_risks(self, uid1, uid2):
        for user in users:
            if user.uid == uid1 or user.uid == uid2:
                if not found1:
                    self.user1 = user
                    found1 = True
                else:
                    self.user2 = user
                user.ongoing_interactions.append(self)
        self.persons = [self.user1, self.user2]
        for p in self.persons:
            totalNonRisk = 1
            for m in self.persons:
                if p == m:
                    continue
        nonrisk = 1-m.risk*self.distance
        totalNonRisk = totalNonRisk*nonrisk
        self.risks[p] = 1-(totalNonRisk*(1-p.risk))
        p.interactions.append(self)
        for p in self.persons:
            p.risk = self.risks[p]
