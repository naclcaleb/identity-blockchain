import datetime
import hashlib
import json
from Transaction import Transaction

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
        block_dict_summary = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.export_transactions(),
            "timestamp": self.timestamp.isoformat(),
            "proof": self.proof
        }

        return json.dumps(block_dict_summary, sort_keys=True)

    def hash(self):
        block_str = self.to_hashable_string()
        return hashlib.sha256(block_str).hexdigest()
        
