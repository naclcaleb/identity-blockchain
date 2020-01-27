import datetime
import Helpers

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
    def from_json(json_obj):
        self.person = json_obj["person"]
        self.document = json_obj["document"]
        self.timestamp = Helpers.datetime_from_iso(json_obj["timestamp"])
        return self