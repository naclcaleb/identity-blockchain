from Block import Block
from Transaction import Transaction
from Node import Node
import hashlib
import json
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.transaction_queue = []
        self.chain = []
        self.proof_difficulty = 4
        self.nodes = set()
        self.add_block(proof=100, previous_hash=1)

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
        guess = "{}{}".format(previous_proof, num).encode('utf-8')
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:self.proof_difficulty] == "0" * self.proof_difficulty


    def prove(self):
        last_block = self.chain[-1]
        last_proof = last_block.proof

        num = 0
        while self.is_valid_proof(last_proof, num) is False:
            num += 1

        return num

    def full_chain_str(self):
        chain_list = [block.to_json() for block in self.chain]
        print(chain_list)
        return json.dumps({
            "chain": chain_list,
            "length": len(self.chain)
        })

    def load_chain(self, chain):
        new_chain = []
        for item in chain:
            new_block = Block(0, 0)
            new_chain.append( new_block.from_json(item) )
        return new_chain

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add( Node(parsed_url.netloc) )


    def is_valid_chain(self, chain):
        previous_hash = 1
        for block in chain:
            if block.previous_hash != previous_hash:
                return False
            if self.is_valid_proof(block.proof) is False:
                return False

        return True

    def resolve_chain(self):
        neighbours = self.nodes
        new_chain = self.chain

        max_len = len(self.chain)

        for node in neighbours:
            requests.get("http://{}/chain".format(node.address))

            if response.status.code == 200:
                length = response.json()['length']

                if length > max_len:
                    possible_chain = self.load_chain(response.json()['chain'])
                    if self.is_valid_chain(possible_chain):
                        max_len = length
                        new_chain = possible_chain

        self.chain = new_chain
    
    


        

     

