import datetime

class Transaction:
    def __init__(self, person, document):
        self.person = person
        self.document = document
        self.timestamp = datetime.datetime.now()

    def summary(self):
        return {
            "person": self.person,
            "document": self.document,
            "timestamp": self.timestamp.isoformat()
        }