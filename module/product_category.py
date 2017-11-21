from flask import Flask, json, request, jsonify

import omplus

db = omplus.db


def get_category_list():
    output_data = {'error': ''}
    result = db.product_category.find()

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
