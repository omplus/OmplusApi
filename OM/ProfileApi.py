from flask import jsonify
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'omplus'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/omplus'

mongo = PyMongo(app)
with app.app_context():
    db = mongo.db

#register

@app.route('/api/user/register', methods=['POST'])
def register():
    reg = mongo.db.user_details

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

    return jsonify({"data": data})

#get all users

@app.route('/api/getAllUsers', methods=['GET'])
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

#get one user with input as email

@app.route('/api/getuser/<email>', methods=['GET'])
def getUser(email):
    reg = mongo.db.user_details
    user = reg.find_one({'email': email})
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



#update profile

@app.route('/api/updateUser/<email>', methods=['GET'])
def updateUser(email):
    reg = mongo.db.user_details

    try:
        firstname = request.json['firstName']
        lastname = request.json['lastName']
        emailid = request.json['email']
        phoneno = request.json['phoneNo']
        profileImg = request.json['profileImage']
        city = request.json['city']
        state = request.json['state']
        pincode = request.json['pincode']

        output =reg.update_one(
            {"email": email},
            {
                "$set": {
                    "firstName": firstname,
                    "lastName": lastname,
                    "email": emailid,
                    "phoneNo": phoneno,
                    "profileImage": profileImg,
                    "city": city,
                    "state": state,
                    "pincode": pincode
                }
            }
        )
        print('\nRecords updated successfully\n')
    except Exception as e:
        print(str(e))

    return jsonify({"result": output})


# insert bank details-------------------
@app.route('/api/userBankDetails/<sellerId>', methods=['POST'])
def addBankDetails(sellerId):
    details = mongo.db.bank_details

    try:

        accountNo = request.json['accountNo']
        accountHolderName = request.json['accountHolderName']
        bankBranch = request.json['bankBranch']
        address = request.json['address']
        state = request.json['state']
        accountType = request.json['accountType']
        bankName = request.json['bankName']
        ifscCode = request.json['ifscCode']
        city = request.json['city']
        pincode = request.json['pincode']
        primaryAccount = request.json['primaryAccount']

        bankDetail=details.insert({
                        "sellerId": sellerId,
                        "accountNo": accountNo,
                        "accountHolderName": accountHolderName,
                        "bankBranch": bankBranch,
                        "address": address,
                        "state": state,
                        "accountType":accountType,
                        "bankName": bankName,
                        "ifscCode": ifscCode ,
                        "city": city ,
                        "pincode": pincode,
                        "primaryAccount": primaryAccount
        })

        print('\nRecords updated successfully\n')
    except Exception as e:
        print(str(e))

    return jsonify({"result": bankDetail})


# add company details-----
@app.route('/api/userCompanyDetails/<sellerId>', methods=['POST'])
def addCompanyDetails(sellerId):
    details = mongo.db.company_details

    try:
        companyId = request.json['companyId']
        companyName = request.json['companyName']
        displayName = request.json['displayName']
        companyPhoneNo = request.json['companyPhoneNo']
        yearOfExperience = request.json['yearOfExperience']
        companyEmail = request.json['companyEmail']
        city = request.json['city']
        state = request.json['state']
        pincode = request.json['pincode']
        tanNo = request.json['tanNo']
        tradingType = request.json['tradingType']
        natureOfTrading = request.json['natureOfTrading']
        gst = request.json['gst']
        description = request.json['description']
        companyLogo = request.json['companyLogo']
        panNo = request.json['panNo']
        status = request.json['status']
        remarks = request.json['remarks']
        dateOfCreation = request.json['dateOfCreation']

        company_detail=details.insert({
                    "sellerId": sellerId,
                    "companyId": companyId,
                    "companyName": companyName,
                    "displayName": displayName,
                    "companyPhoneNo": companyPhoneNo,
                    "yearOfExperience": yearOfExperience,
                    "companyEmail": companyEmail,
                    "city": city,
                    "state": state,
                    "pincode": pincode,
                    "tanNo": tanNo,
                    "tradingType": tradingType,
                    "natureOfTrading": natureOfTrading,
                    "description": description,
                    "gst": gst,
                    "companyLogo": companyLogo,
                    "panNo": panNo,
                    "status": status,
                    "remarks": remarks,
                    "dateOfCreation": dateOfCreation
        })
        print('\nRecords updated successfully\n')
    except Exception as e:
        print(str(e))

    return jsonify({"result": company_detail})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
