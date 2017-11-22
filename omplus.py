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
db = client.omplus
app.debug = os.environ.get('DEBUG', False)

var = 44
appSecret = "omPlusAppSecret"
ERROR_NotJson = "Request Payload is Not JSon"

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
        result = db.user.find({'usr': user})
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


# inventory
@app.route('/api/inventory/list', methods=['POST', 'GET'])
def inventory_list():
    from module import inventory
    return inventory.get_inventory_list()


# products
@app.route('/api/product/list', methods=['POST', 'GET'])
def product_list():
    from module import product
    return product.get_product_list()


###################Manish Api########################################


@app.route('/seller/save-purchase-detail', methods=['POST'])
def save_purchase_detail():
    output_data = {'error': ''}
    purchase = db.purchase
    supplier_id = request.values.get('supplier_id')   #supplier collection
    product_id = request.values.get('product_id')     #product collection
    quantity = request.values.get('quantity')         
    unit = request.values.get('unit')
    batch_no = request.values.get('batch_no')
    date_of_mfg = request.values.get('date_of_mfg')
    exp_date = request.values.get('exp_date')
    total_cost = request.values.get('total_cost')
    unit_cost = request.values.get('unit_cost')
    invoice_no = request.values.get('invoice_no')
    tax_id = request.values.get('tax_id')                #tax collection
    date_of_receiving = request.values.get('date_of_receiving') 
    warehouse_id = request.values.get('warehouse_id')     #warehouse collection
    purchase_id = purchase.insert({'supplier':supplier_id,'product':product_id,
                                'quantity':quantity,'unit':unit,
                                'batch_no':batch_no,'date_of_mfg':date_of_mfg,
                                'exp_date':exp_date,'total_cost':total_cost,
                                'unit_cost':unit_cost,'invoice_no':invoice_no,
                                'tax':tax_id,'date_of_receiving':date_of_receiving,
                                 'warehouse':warehouse_id})
    output_data['result'] = 'Purchase details successfully saved'
    return jsonify(output_data)


@app.route('/seller/save-expense-detail', methods=['POST'])
def save_expens_detail():
    output_data = {'error': ''}
    expense = db.expense
    name = request.values.get('name')  
    org_id = request.values.get('org_id')  #org collection
    # gst_no = request.values.get('gst_no')         
    total_cost = request.values.get('total_cost')
    tax_paid = request.values.get('tax_paid')
    tax_id = request.values.get('tax_id')   #tax collection
    total_amount_with_tax = int(total_cost) + int(tax_paid)
    invoice_no = request.values.get('invoice_no')
    date = request.values.get('date')
    expense_id = expense.insert({'name':name,'org':org_id,
                                'total_cost':total_cost,'tax_paid':tax_paid,
                                'tax':tax_id,'total_amount_with_tax':total_amount_with_tax,
                                'invoice_no':invoice_no,'date':date
                                })
    output_data['result'] = 'Expense details successfully saved'
    return jsonify(output_data)


# =======================================================================


if __name__ == '__main__':
    app.run()
