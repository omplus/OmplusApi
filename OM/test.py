import random
from flask import jsonify
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'omplus'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/omplus'

mongo = PyMongo(app)
with app.app_context():
    db = mongo.db


# ---------------------seller info----------------------------------------


# ----------------------------------------------------------------------------------------------------------

@app.route('/api/user/register', methods=['POST'])
def register():
    reg = mongo.db.user_details
    # if request.method == 'GET':
    #    return render_template('register.html')

    #sellerId = request.json[random.randint(111111,999999)]
    sellerId = request.json['sellerId']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    phoneNo = request.json['phoneNo']
    pwd = request.json['pwd']
    confirmPwd = request.json['confirmPwd']

    user = reg.insert({'sellerId': sellerId, 'firstName': firstName, 'lastName': lastName,
                       'email': email, 'phoneNo': phoneNo, 'pwd': pwd, 'confirmPwd': confirmPwd})
    data = reg.find_one({"_id": user})
    # pr data["firstName"]
    return jsonify({"firstName": data['firstName']})
# db.session.add(user)
 #   db.session.commit()
 #   flash('User successfully registered')
    # return redirect(url_for('index'))


@app.route('/api/users', methods=['GET'])
def getUsers():
    reg = mongo.db.user_details
    output = []
    data = reg.find()
    for d in data:
        output.append(
            {
                "sellerId": d['sellerId'],
                "firstName": d['firstName'],
                "lastName": d['lastName'],
                "email": d['email'],
                "phoneNo": d['phoneNo'],
                "pwd": d['pwd'],
                "confirmPwd": d['confirmPwd'],
            }
        )

    return jsonify({"output": output})


@app.route('/api/user/<firstName>', methods=['GET'])
def getUser(firstName):
    reg = mongo.db.user_details
    user = reg.find_one({'firstName': firstName})
    if user:
        output = (
            {
                "sellerId": user['sellerId'],
                "firstName": user['firstName'],
                "lastName": user['lastName'],
                "email": user['email'],
                "phoneNo": user['phoneNo'],
                "pwd": user['pwd'],
                "confirmPwd": user['confirmPwd'],
            }
        )
    else:
        output = "No Result Found"

    return jsonify({"result": output})

"""
@app.route('/api/users/<firstName>', methods=['GET'])
def filterUsers(firstName):
    reg = mongo.db.user_details
    output = []
    if firstName:
        data = reg.find({"firstName": firstName})
    else:
        data = reg.find({})

    for d in data:
        output.append(
                {
                    "sellerId": d['sellerId'],
                    "firstName" : d['firstName'],
                    "lastName": d['lastName'],
                    "email" : d['email'],
                    "phoneNo" : d['phoneNo'],
                    "pwd" : d['pwd'],
                    "confirmPwd" : d['confirmPwd'],
                    }
                )

"""
if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
