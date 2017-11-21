import os

import copy
from flask import Flask, json, request, jsonify
import omplus

db = omplus.db
var = 44
outputData = {'error': ''}


def get_user_list():
    output_data = {'error': ''}
    result = db.users.find()
    if result.count() == 0:
        output_data['error'] = 'No Data Found ...!'
        return jsonify(output_data)

    res = []
    snl = 0

    for doc in result:
        snl = snl + 1
        doc['_id'] = str(doc['_id'])
        res.append(doc)

    output_data['result'] = res

    return jsonify(output_data)


def sign_in(request):
    print(request.json)
    output_data = {'error': ''}
    username = request.json['username']
    password = request.json['password']
    print(username + " / " + password)
    res = []
    result = db.user_info.find({'$and': [{"username": username, "password": password}]})

    print('result =========== ', result)
    if result.count() > 0:
        for row in result:
            row['_id'] = str(row['_id'])
            res.append(row)

        output_data['result'] = res
    else:
        output_data['error'] = 'username & password Mismatch'
    return output_data
