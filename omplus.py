import os
from flask import Flask, json, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from module import user

app = Flask(__name__)

# Create a Connection
client = MongoClient()
# client = MongoClient("mongodb://localhostdb:27017")
# app.config['MONGO_DBNAME'] = 'om'

# Access Database Objects
db = client.om
app.debug = os.environ.get('DEBUG', False)

var = 44
appSecret = "omPlusAppSecret"
ERROR_NotJson = "Request Payload is Not JSon"


# outputData = {'error': ''}


# =================== SUJEET =======================================

@app.route('/', methods=['POST', 'GET'])
def welcome():
    outputData = {'error': ''}
    if not request.json:
        outputData['error'] = ERROR_NotJson

    outputData['result'] = "Welcome to OM+"
    return jsonify(outputData)


@app.route('/api/signin', methods=['POST', 'GET'])
def signIn():
    outputData = {'error': ''}
    if not request.json:
        outputData['error'] = ERROR_NotJson
        return jsonify(outputData)

    user = request.json['email']
    pwd = request.json['password']

    if len(user) > 1 and len(pwd) > 1:
        result = db.user.find({'usr': user})
        # print len(result)
        for doc in result:
            doc['_id'] = str(doc['_id'])
            outputData['result'] = doc
            # return jsonify('status', 'true')
    else:
        outputData['error'] = "All Fields Are Mandatory"

    return jsonify(outputData)


@app.route('/api/userlist', methods=['POST', 'GET'])
def getAllUserList():
    outputData = {'error': ''}
    result = db.user.find()
    res = []
    for doc in result:
        doc['_id'] = str(doc['_id'])
        res.append(doc)

    outputData['result'] = res
    return json.dumps(outputData)


@app.route('/userlist', methods=['POST', 'GET'])
def userList():
    from module import user
    return user.getUserList()


# ==============================================================


if __name__ == '__main__':
    app.run()
