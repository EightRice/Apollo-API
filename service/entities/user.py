class User:
    def __init__(self, uid, last_location):
        self.uid = uid
        self.risk = 0
        self.last_location = last_location
        self.ongoing_interactions = []
        self.past_interactions = []

    def to_dict(self):
        return {
            'name': self.uid,
            'risk': self.risk,
            'last_location': self.last_location
        }

    def test(self, result):
        if result == True:
            self.risk = 100
        else:
            self.risk = 0.0001

    def __str__(self):
        return str(str(self.uid))

    def update(self):
        totalNonRisk = 1
        for c in self.past_interactions:
            totalNonRisk = totalNonRisk*(1-c.risk)
            oldrisk = self.risk
            if oldrisk != 1-totalNonRisk:
                self.risk = 1-totalNonRisk
                print(self.uid, "'s risk changed to ",
                      self.uid, " from ", oldrisk)
                c.update()
            else:
                print(" no change to", self.uid, "'s risk ")
