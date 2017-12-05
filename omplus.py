import os
from flask import Flask, json, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from module import api_key

app = Flask(__name__)

# Create a Connection
client = MongoClient()
# client = MongoClient("mongodb://localhostdb:27017")
# app.config['MONGO_DBNAME'] = 'om'

# Access Database Objects
db = client.omplus
app.debug = os.environ.get('DEBUG', False)

var = 44
appSecret = "omPlusAppSecret"
ERROR_NotJson = "Request Payload is Not JSon"
ERROR_AllFieldsMandatory = "All Fields Are Required...!"


# outputData = {'error': ''}


# =================== SUJEET =======================================

@app.route('/', methods=['POST', 'GET'])
def welcome():
    output_data = {'error': ''}
    if not request.json:
        output_data['error'] = ERROR_NotJson

    output_data['result'] = "Welcome to OM+"
    return jsonify(output_data)


@app.route('/api/signin', methods=['POST', 'GET'])
def sign_in():
    output_data = {'error': ''}
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    user = request.json['email']
    pwd = request.json['password']

    if len(user) > 1 and len(pwd) > 1:
        result = db.user.find_one({'usr': user})
        # print len(result)
        for doc in result:
            doc['_id'] = str(doc['_id'])
            output_data['result'] = doc
            # return jsonify('status', 'true')
    else:
        output_data['error'] = "All Fields Are Mandatory"

    return jsonify(output_data)


@app.route('/api/userlist', methods=['POST', 'GET'])
def get_all_user_list():
    output_data = {'error': ''}
    result = db.user.find()
    res = []
    for doc in result:
        doc['_id'] = str(doc['_id'])
        res.append(doc)

    output_data['result'] = res
    return json.dumps(output_data)


@app.route('/userlist', methods=['POST', 'GET'])
def user_list():
    from module import user
    return user.get_user_list()


# warehouse
@app.route('/api/warehouse/list', methods=['POST', 'GET'])
def warehouse_list():
    from module import warehouse
    return warehouse.get_warehouse_list()


@app.route('/api/warehouse/register', methods=['POST'])
def warehouse_register():
    print("hit - " + str(request))
    output_data = {'error': ''}
    from module import warehouse
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    payload = request.json

    try:
        if len(payload[api_key.CompanyId]) > 2 and len(
                payload[api_key.WarehouseName]) > 0 and len(payload[api_key.WarehouseManager]) > 0:
            return warehouse.add_warehouse(payload)
        else:
            output_data['error'] = ERROR_AllFieldsMandatory
            return jsonify(output_data)

    except Exception as e:
        # print str(e)
        print(e)
        output_data['error'] = "pls check payload " + str(e)
        return jsonify(output_data)


@app.route('/api/warehouse/info', methods=['POST'])
def warehouse_info():
    print("payload - " + str(request))
    output_data = {'error': ''}
    from module import warehouse
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    payload = request.json

    try:
        if len(payload[api_key.WarehouseId]) > 2:
            return warehouse.warehouse_info(payload)
        else:
            output_data['error'] = ERROR_AllFieldsMandatory + "Invalid Payload"
            return jsonify(output_data)

    except Exception as e:
        # print str(e)
        print(e)
        output_data['error'] = "pls check payload " + str(e)
        return jsonify(output_data)


# inventory
@app.route('/api/inventory/list', methods=['POST', 'GET'])
def inventory_list():
    from module import inventory
    return inventory.get_inventory_list()


# inventory register/adding
@app.route('/api/inventory/register', methods=['POST'])
def inventory_register():
    print("hit - " + str(request))
    output_data = {'error': ''}
    from module import inventory
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    payload = request.json

    try:
        if len(payload[api_key.InventoryWarehouseId]) > 2 and len(
                payload[api_key.InventoryProductId]) > 0 and len(payload[api_key.InventorySupplierId]) > 0:
            return inventory.add(payload)
        else:
            output_data['error'] = ERROR_AllFieldsMandatory
            return jsonify(output_data)

    except Exception as e:
        # print str(e)
        print(e)
        output_data['error'] = "pls check payload " + str(e)
        return jsonify(output_data)


# inventory info
@app.route('/api/inventory/info', methods=['POST'])
def inventory_info():
    print("payload - " + str(request))
    output_data = {'error': ''}
    from module import inventory
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    payload = request.json

    try:
        if len(payload[api_key.InventoryProductId]) > 2:
            return inventory.info(payload)
        else:
            output_data['error'] = ERROR_AllFieldsMandatory + "Invalid Payload"
            return jsonify(output_data)

    except Exception as e:
        # print str(e)
        print(e)
        output_data['error'] = "pls check payload " + str(e)
        return jsonify(output_data)


# products
@app.route('/api/product/list', methods=['POST', 'GET'])
def product_list():
    from module import product
    return product.get_product_list()


# ==============================================================


if __name__ == '__main__':
    # app.run(debug=True, host="localhost", port=5000)
    app.run()
