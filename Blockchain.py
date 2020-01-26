from Block import Block
from Transaction import Transaction
import hashlib

class Blockchain:
    def __init__(self):
        self.transaction_queue = []
        self.chain = []
        self.proof_difficulty = 4

    def add_block(self, proof, previous_hash=None):
        new_block = Block(
            len(self.chain), #Index = current length of chain (zero-based)
            proof, #Proof passed to function
            previous_hash=previous_hash or self.chain[-1].hash() #Use either the provided hash or the hash of the last block on the current chain
        )

        new_block.add_transactions(self.transaction_queue)

        self.chain.append(new_block)

        self.transaction_queue = []

        return new_block
    
    def add_transaction(self, person, document):
        new_transaction = Transaction(person, document)
        self.transaction_queue.append(new_transaction)

    def is_valid_proof(self, previous_proof, num):
        guess = "{}{}".format(previous_proof, num).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:self.proof_difficulty] == "0" * self.proof_difficulty


    def prove(self):
        last_block = chain[-1]
        last_proof = last_block.proof

        num = 0
        while self.is_valid_proof(last_proof, num) is False:
            num += 1

        return num


     

