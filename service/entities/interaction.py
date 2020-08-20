from config.db import users
from config.db import ongoing_interactions
from config.db import interactions


class Interaction:
    def __init__(self, user1, user2):
        self.id = len(interactions)
        interactions.append(self)
        ongoing_interactions.append(self)
        user1.ongoing_interactions.append((user2.uid, self.id))
        user2.ongoing_interactions.append((user1.uid, self.id))
        self.ongoing = True
        self.uids = [user1.uid, user2.uid]
        self.start_time = user1.last_location.time
        self.end_time = 0
        self.outdoor = True
        self.distance = 1
        self.updates = {}
        self.user1 = user1
        self.user2 = user2

    def end(self):
        print("se sterge")
        self.ongoing = False
        self.user1.ongoing_interactions.remove((self.user2.uid, self.id))
        self.user2.ongoing_interactions.remove((self.user1.uid, self.id))
        self.user1.past_interactions.append((self.user2.uid, self.id))
        self.user2.past_interactions.append((self.user1.uid, self.id))
        ongoing_interactions.remove(self)

        # def get_risks(self, uid1, uid2):
        #     for user in users:
        #         if user.uid == uid1 or user.uid == uid2:
        #             if not found1:
        #                 self.user1 = user
        #                 found1 = True
        #             else:
        #                 self.user2 = user
        #             user.ongoing_interactions.append(self)
        #     self.persons = [self.user1, self.user2]
        #     for p in self.persons:
        #         totalNonRisk = 1
        #         for m in self.persons:
        #             if p == m:
        #                 continue
        #     nonrisk = 1-m.risk*self.distance
        #     totalNonRisk = totalNonRisk*nonrisk
        #     self.risks[p] = 1-(totalNonRisk*(1-p.risk))
        #     p.interactions.append(self)
        #     for p in self.persons:
        #         p.risk = self.risks[p]
