from Blockchain import Blockchain
from flask import Flask, request, jsonify, send_file
import Helpers
import sys
import uuid
import bcrypt
from simplecrypt import encrypt, decrypt
import json
import io


app = Flask(__name__)

port = 5000

server_config = Helpers.json_from_file('server_config.json')

port = server_config.get('port') or port
encryption_key = server_config.get('encryption_key') or str(uuid.uuid1())

port = sys.argv[1] if len(sys.argv) > 1 else port

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



@app.route('/document/upload', methods=["POST"])
def upload_document():
    #The identity token is required to create a transaction.
    #The identity token is just a way to identify a specific person.
    #For now, we can just use names, but in the future this could be 
    #information represented by a fingerprint or other biometric data
    identity_token = request.form.get('identity_token')
    if identity_token == None:
        return '{ "status": 0, "error": "requires-identity-token" }'
    file = request.files.get('file')
    if file == None:
        return '{ "status": 0, "error": "no-file-provided" }'

    file_data = file.read()

    document_id = str(uuid.uuid1())

    encrypted = encrypt(encryption_key, file_data)

    with open('./encrypted_documents/' + document_id + '.txt', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    document_hash = bcrypt.hashpw(str(encrypted).encode('utf-8'), bcrypt.gensalt())

    blockchain.add_transaction(identity_token, document_hash.decode('utf-8'))
    proof = blockchain.prove()
    blockchain.add_block(proof)

    return json.dumps({
        "status": 1,
        "document_id": document_id
    })

@app.route('/document/retrieve', methods=["GET"])
def retrieve_document():
    identity_token = request.args.get('identity_token')
    document_id = request.args.get('document_id')
    
    #First, we verify that the document exists
    encrypted_data = None
    try:
        with open('./encrypted_documents/' + document_id + '.txt', 'rb') as file:
            encrypted_data = file.read()
    except:
        return '{ "status": 0, "error": "document-not-found" }'
    
    #Now, check the blockchain for a record of that person uploading the document
    is_valid = False
    for block in blockchain.chain:
        for transaction in block.transactions:
            print("=================")
            print("Person: {}, Compared: {}".format(transaction.person, identity_token))
            if transaction.person == identity_token and bcrypt.checkpw(str(encrypted_data).encode('utf-8'), transaction.document.encode('utf-8')):
                is_valid = True
    
    if not is_valid:
        return '{ "status": 0, "error": "not-authorized" }'
    
    decrypted_file = decrypt(encryption_key, encrypted_data)
    
    return send_file(
    io.BytesIO(decrypted_file),
    mimetype='image/jpeg',
    as_attachment=True,
    attachment_filename='img.jpg')


@app.route('/', methods=["GET"])
def frontend():
    frontend = ""
    with open('index.html', 'r') as file:
        frontend = file.read()

    return frontend


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)