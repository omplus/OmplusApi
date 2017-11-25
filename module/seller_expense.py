import os
from flask import Flask, abort, request, jsonify
from flask import render_template
from pymongo import MongoClient
client = MongoClient()

app = Flask(__name__, template_folder='templates')
db = client.omplus
app.debug = os.environ.get('DEBUG', False) 

seller = db.seller
expense = db.expense

@app.route('/sellers/<seller_id>/expenses', methods=['POST'])
def get_all_expenses():
    """
        Api to list all the expense records of any seller.

    """
    output_data = {'error': ''}

    seller_detail = seller.find_one({'_id': seller_id })
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    all_expenses = expense.find({'seller_id':seller_id})
    output_data['result'] = all_expenses
    return jsonify(output_data)


@app.route('/sellers/<seller_id>/save-expense-detail', methods=['POST'])
def save_expense_detail():
    """
        Api to save new expense detail of any seller.

    """
    output_data = {'error': ''}
    
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    name = request.values.get('name')  
    org_id = request.values.get('org_id')  #org collection
    # gst_no = request.values.get('gst_no')         
    total_cost = request.values.get('total_cost')
    tax_paid = request.values.get('tax_paid')
    tax_id = request.values.get('tax_id')   #tax collection
    total_amount_with_tax = int(total_cost) + int(tax_paid)
    invoice_no = request.values.get('invoice_no')
    date = request.values.get('date')
    expense_id = expense.insert({'seller':seller_id,'name':name,'org':org_id,
                                'total_cost':total_cost,'tax_paid':tax_paid,
                                'tax':tax_id,'total_amount_with_tax':total_amount_with_tax,
                                'invoice_no':invoice_no,'date':date,'is_active':True
                                })
    output_data['result'] = 'Expense details successfully saved'
    return jsonify(output_data)


@app.route('/seller/<seller_id>/expenses/<expense_id>/expense-detail',methods=['GET'])
def get_seller_expense_detail():
    """
        Api to get any particular expense deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    expense_detail = expense.find_one({'_id':expense_id,'seller':seller_id,'is_active':True})
    
    if expense_detail.count() == 0:
        output_data['error'] = 'No expense Found ...!'
        return jsonify(output_data)
    output = (
              {
                'supplier':expense_detail['supplier'],'name':expense_detail['name'],
                'org':expense_detail['org'],'total_cost':expense_detail['total_cost'],
                'tax_paid':expense_detail['tax_paid'],'tax':expense_detail['tax'],
                'total_amount_with_tax':expense_detail['total_amount_with_tax'],'total_cost':expense_detail['total_cost'],
                'invoice_no':expense_detail['invoice_no'],'invoice_no':expense_detail['invoice_no']
                }
            )
    return jsonify({"result": output})


@app.route('/seller/<seller_id>/expenses/<expense_id>/update-expense-detail',methods=['POST'])
def update_seller_expense_detail():
    """
        Api to update any particular expense deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    expense_detail = expense.find_one({'_id':purchase_id,'seller':seller_id,'is_active':True})
    
    if expense_detail.count() == 0:
        output_data['error'] = 'No expense record found ...!'
        return jsonify(output_data)
    name = request.values.get('name')  
    org_id = request.values.get('org_id')  #org collection
    total_cost = request.values.get('total_cost')
    tax_paid = request.values.get('tax_paid')
    tax_id = request.values.get('tax_id')   #tax collection
    total_amount_with_tax = int(total_cost) + int(tax_paid)
    invoice_no = request.values.get('invoice_no')
    date = request.values.get('date')
    
    expense_detail['name'] = name
    expense_detail['org'] = org_id
    expense_detail['total_cost'] = total_cost
    expense_detail['tax_paid'] = tax_paid
    expense_detail['tax'] = tax_id
    expense_detail['total_amount_with_tax'] = total_amount_with_tax
    expense_detail['invoice_no'] = invoice_no
    expense_detail['date'] = date

    expense.save(expense_detail)
    
    output_data['result'] = 'Expense details successfully updated'
    return jsonify({"result": output_data}) 


@app.route('/seller/<seller_id>/expenses/<expense_id>/delete',methods=['POST'])
def delete_seller_expense_detail():
    """
        Api to delete any particular purchase deail of a seller.

    """
    seller_detail = seller.find_one({'_id': seller_id })
    
    if seller_detail.count() == 0:
        output_data['error'] = 'No seller record found ...!'
        return jsonify(output_data)

    expense_detail = expense.find_one({'_id':purchase_id,'seller':seller_id,'is_active':True})
    
    if expense_detail.count() == 0:
        output_data['error'] = 'No expense record found ...!'
        return jsonify(output_data)
    
    expense_detail['is_active'] = False

    expense.save(expense_detail)
    
    output_data['result'] = 'Expense details removed successfully'
    return jsonify({"result": output_data})

