import datetime
import hashlib
import json
from Transaction import Transaction
import Helpers

def gt(dt_str):
        dt, _, us= dt_str.partition(".")
        dt= datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us= int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)

class Block:
    def __init__(self, index, proof, previous_hash="0000"):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = []
        self.timestamp = datetime.datetime.now()
        self.proof = proof

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def add_transactions(self, transactions):
        for transaction in transactions:
            self.add_transaction(transaction)

    def export_transactions(self):
        exported = []
        for transaction in self.transactions:
            exported.append( transaction.summary() )

        return exported

    def to_hashable_string(self):
        return json.dumps(self.to_json(), sort_keys=True)

    def to_json(self):
        block_dict_summary = {
            "index": self.index,
            "previous_hash": str(self.previous_hash),
            "transactions": self.export_transactions(),
            "timestamp": self.timestamp.isoformat(),
            "proof": self.proof
        }
        return block_dict_summary

    def from_json(self, json_dict):
        self.index = json_dict["index"]
        self.previous_hash = json_dict["previous_hash"]
        self.transactions = []
        for transaction in json_dict["transactions"]:
            new_transaction = Transaction("", "")
            self.transactions.append(new_transaction.from_json(transaction))
        self.timestamp = Helpers.datetime_from_iso(json_dict["timestamp"])
        self.proof = int(json_dict["proof"])
        return self

    def hash(self):
        block_str = self.to_hashable_string()
        return hashlib.sha256(block_str.encode('utf-8')).hexdigest()
        
