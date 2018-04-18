import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from pymongo import MongoClient
import urllib.request,json
from bson import json_util
from flask_cors import CORS


import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

#cors = CORS(app, resources={r"/transactions/*": {"origins": "*"}})




@app.route('/check', methods=['GET'])
def mine():
    response = {
        'message': "inside mine, working",
    }
    return jsonify(response), 200


# @app.route('/transactions/new', methods=['POST'])
# def new_transaction():
#     values = request.get_json()
#     # Check that the required fields are in the POST'ed data
#     required = ['sender', 'recipient', 'amount']
#     if not all(k in values for k in required):
#         return 'Missing values', 400
#     # Create a new Transaction
#     index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

#     response = {'message': f'Transaction will be added to Block {index}'}
#     return jsonify(response), 201


# @app.route('/login', methods=['POST'])
# def login():
#     values = request.get_json()
#     # Check that the required fields are in the POST'ed data
#     required = ['email', 'password']
#     if not all(k in values for k in required):
#         return 'Missing values', 400
#     # Create a new Transaction
#     client = MongoClient()
#     db = client['blockchain']
#     collection = db['blockchain']
#     loginstatus = db.collection.find({ "email" : values['email'],"password" : values['password'] }).count()
#     if (loginstatus>=1):
#         response = {'message': f'True'}
#         return jsonify(response), 201
#     else:
#         response = {'message': f'False'}
#         return jsonify(response), 401
    

# @app.route('/signup', methods=['POST'])
# def signup():
#     values = request.get_json()
#     # Check that the required fields are in the POST'ed data
#     #required = ['email', 'password']
#     #if not all(k in values for k in required):
#     #   return 'Missing values', 400
#     # Create a new Transaction
#     #print('True1')
#     client = MongoClient()
#    # print('True2')
#     db = client['blockchain']
#    # print('True3')
#     collection = db['blockchain']
#     serverStatusResult=db.command("serverStatus")
#     success = db.collection.insert_one({
#             "email": values['email'],
#             "password": values['password']
#             })
#     print ("after this")
#     print (success)
#     if (success!=False):
#         response = {'message': f'True'}
#     else:
#         response = {'message': f'False'}
#     return jsonify(response), 201


# @app.route('/chain', methods=['GET'])
# def full_chain():
#     response = {
#         'chain': blockchain.chain,
#         'length': len(blockchain.chain),
#     }
#     return jsonify(response), 200


# @app.route('/nodes/register', methods=['POST'])
# def register_nodes():
#     values = request.get_json()

#     nodes = values.get('nodes')
#     if nodes is None:
#         return "Error: Please supply a valid list of nodes", 400

#     for node in nodes:
#         blockchain.register_node(node)

#     response = {
#         'message': 'New nodes have been added',
#         'total_nodes': list(blockchain.nodes),
#     }
#     return jsonify(response), 201


# @app.route('/nodes/resolve', methods=['GET'])
# def consensus():
#     replaced = blockchain.resolve_conflicts()

#     if replaced:
#         response = {
#             'message': 'Our chain was replaced',
#             'new_chain': blockchain.chain
#         }
#     else:
#         response = {
#             'message': 'Our chain is authoritative',
#             'chain': blockchain.chain
#         }

#     return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)