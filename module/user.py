import os

import copy
from flask import Flask, json, request, jsonify
# Import MongoClient from pymongo.
from pymongo import MongoClient
from bson.json_util import dumps

# app = Flask(__name__)

# Create a Connection
client = MongoClient()
# client = MongoClient("mongodb://localhostdb:27017")
# app.config['MONGO_DBNAME'] = 'om'
# Access Database Objects
db = client.om
# app.debug = os.environ.get('DEBUG', False)
var = 44
outputData = {'error': ''}

def getUserList():
    outputData = {'error': ''}
    result = db.user.find()
    res = []
    snl = 0

    for doc in result:
        snl = snl + 1
        doc['_id'] = str(doc['_id'])
        res.append(doc)

    outputData['result'] = res

    return jsonify(outputData)


def sign_in(request):
    print (request.json)
    outputData = {'error': ''}
    username = request.json['username']
    password = request.json['password']
    print (username + " / " + password)
    res = []
    result = db.user_info.find({'$and': [{"username": username, "password": password}]})
    print ('result =========== ', result)
    if result.count() > 0:
        for row in result:
            row['_id'] = str(row['_id'])
            res.append(row)

        outputData['result'] = res
    else:
        outputData['error'] = 'username & password Mismatch'
    return outputData