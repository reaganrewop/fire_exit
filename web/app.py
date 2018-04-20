import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from pymongo import MongoClient
import urllib.request,json
from bson import json_util
from flask_cors import CORS

import pandas as pd
import re
import itertools
import operator


import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

def init_db():
    client = MongoClient("mongodb://127.168.0.1:9000/")
    db = client['firexitdb']
    collection = db['exit1']
    serverstatus = db.command("serverStatus")
    myCursor = db.exit1.find()
    for item in myCursor:
        if (item["status"]=="blocked"):
            return ({"status":"blocked"})
        elif (item["status"]=="unblocked"):
            return ({"status":"unblocked"})



@app.route('/check', methods=['GET'])
def mine():
    query = init_db()
    print (query)
    #response = {
    #    'message': "inside mine, working",
    #}
    return jsonify(query), 200



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=9999, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)