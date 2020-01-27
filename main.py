from Blockchain import Blockchain
from flask import Flask, request, jsonify
import Helpers

app = Flask(__name__)

port = 5000

server_config = Helpers.json_from_file('server_config.json')

port = server_config.get('port') or port

blockchain = Blockchain()

@app.route('/chain', methods=["GET"])
def get_chain():
    return blockchain.full_chain_str()

@app.route('/transactions/new', methods=["POST"])
def new_transaction():
    required = ['person', 'document']
    if not all(k in request.form for k in required):
        return '{ "status": 0, "error": "Missing transaction details" }'
    blockchain.add_transaction(request.form['person'], request.form['document'])

    return '{ "status": 1}'

@app.route('/mine', methods=["GET"])
def mine():
    proof = blockchain.prove()
    new_block = blockchain.add_block(proof)
    return new_block.to_hashable_string()

@app.route('/nodes/register', methods=["POST"])
def register():
    nodes = request.form.get('nodes')
    if nodes is None:
        return '{ "status": 0, "error": "No nodes provided" }'

    for node in nodes:
        blockchain.add_node(node)

    return '{ "status": 1 }'

@app.route('/nodes/resolve', methods=["GET"])
def resolve():
    blockchain.resolve_chain()
    return blockchain.full_chain_str()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)