from flask import Flask, json, request, jsonify

import omplus

db = omplus.db
collection = db.inventory

output_data = {'error': ''}


def get_inventory_list():
    output_data = {'error': ''}
    result = collection.find()

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


# register
def add_inventory(payload):
    output_data = {'error': ''}
    result = collection.insert_one(payload)

    if result.inserted_id:
        output_data['status'] = 'Inserted Success...!'
        output_data['_id'] = str(result.inserted_id)
        return jsonify(output_data)
    else:
        output_data['error'] = 'No Data Inserted ...!'
        return jsonify(output_data)

