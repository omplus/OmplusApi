import os
from flask import Flask, abort, request, jsonify
from flask import render_template
from pymongo import MongoClient
client = MongoClient()

app = Flask(__name__, template_folder='templates')
db = client.omplus
app.debug = os.environ.get('DEBUG', False) 

seller = db.seller
purchase = db.purchase

@app.route('/sellers/<seller_id>/purchases', methods=['POST'])
def get_all_purchases():
    """
        Api to list all the purchase records of any seller.

    """
    output_data = {'error': ''}
    seller_detail = seller.find_one({'_id': seller_id })
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    all_purchases = purchase.find({'seller_id':seller_id})
    output_data['result'] = all_purchases
    return jsonify(output_data)


@app.route('/sellers/<seller_id>/save-purchase-detail', methods=['POST'])
def save_purchase_detail():
    """
        Api to save new purchase detail of any seller.

    """
    output_data = {'error': ''}

    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)
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
    purchase_id = purchase.insert({'seller':seller_id,'supplier':supplier_id,'product':product_id,
                                    'quantity':quantity,'unit':unit,
                                    'batch_no':batch_no,'date_of_mfg':date_of_mfg,
                                    'exp_date':exp_date,'total_cost':total_cost,
                                    'unit_cost':unit_cost,'invoice_no':invoice_no,
                                    'tax':tax_id,'date_of_receiving':date_of_receiving,
                                    'warehouse':warehouse_id,'is_active':True})
    output_data['result'] = 'Purchase details successfully saved'
    return jsonify(output_data)


@app.route('/seller/<seller_id>/purchases/<purchase_id>/purchase-detail', methods=['GET'])
def get_seller_purchase_detail():
    """
        Api to get any particular purchase deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    purchase_detail = purchase.find_one({'_id':purchase_id,'seller':seller_id,'is_active':True})
    
    if purchase_detail.count() == 0:
        output_data['error'] = 'No purchase record found ...!'
        return jsonify(output_data)
    output = (
            {
            'supplier':purchase_detail['supplier'],'product':purchase_detail['product'],
            'quantity':purchase_detail['quantity'],'unit':purchase_detail['unit'],
            'batch_no':purchase_detail['batch_no'],'date_of_mfg':purchase_detail['date_of_mfg'],
            'exp_date':purchase_detail['exp_date'],'total_cost':purchase_detail['total_cost'],
            'unit_cost':purchase_detail['unit_cost'],'invoice_no':purchase_detail['invoice_no'],
            'tax':purchase_detail['tax'],'date_of_receiving':purchase_detail['date_of_receiving'],
            'warehouse':purchase_detail['warehouse']
            }
        )
    return jsonify({"result": output})


@app.route('/seller/<seller_id>/purchases/<purchase_id>/update-purchase-detail', methods=['POST'])
def update_seller_purchase_detail():
    """
        Api to update any particular purchase deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    purchase_detail = purchase.find_one({'_id':purchase_id,'seller':seller_id,'is_active':True})
    
    if purchase_detail.count() == 0:
        output_data['error'] = 'No purchase record found ...!'
        return jsonify(output_data)
    
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
    warehouse_id = request.values.get('warehouse_id')  
    
    purchase_detail['supplier_id'] = supplier_id
    purchase_detail['product_id'] = product_id
    purchase_detail['quantity'] = quantity
    purchase_detail['unit'] = unit
    purchase_detail['batch_no'] = batch_no
    purchase_detail['date_of_mfg'] = date_of_mfg
    purchase_detail['exp_date'] = exp_date
    purchase_detail['total_cost'] = total_cost

    purchase_detail['unit_cost'] = unit_cost
    purchase_detail['invoice_no'] = invoice_no
    purchase_detail['tax_id'] = tax_id
    purchase_detail['date_of_receiving'] = date_of_receiving
    purchase_detail['warehouse_id'] = warehouse_id

    purchase.save(purchase_detail)
    output_data['result'] = 'Purchase details successfully updated'
    return jsonify({"result": output_data})  


@app.route('/seller/<seller_id>/purchases/<purchase_id>/delete', methods=['POST'])
def delete_seller_purchase_detail():
    """
        Api to delete any particular purchase deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    purchase_detail = purchase.find_one({'_id':purchase_id,'seller':seller_id,'is_active':True})
    
    if purchase_detail.count() == 0:
        output_data['error'] = 'No purchase record found ...!'
        return jsonify(output_data)
    
    purchase_detail['is_active'] = False

    purchase.save(purchase_detail)
    output_data['result'] = 'Purchase details removed successfully'
    return jsonify({"result": output_data})