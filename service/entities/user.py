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
