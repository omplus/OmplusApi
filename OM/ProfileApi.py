from flask import jsonify
from flask import Flask, request,session, flash, url_for, redirect, render_template
from flask_pymongo import PyMongo
from werkzeug import generate_password_hash,check_password_hash

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'omplus'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/omplus'

mongo = PyMongo(app)
with app.app_context():
    db = mongo.db
ERROR_NotJson = "Request Payload is Not JSon"


# user--------------
@app.route('/api/user/register', methods=['POST'])
def register():
    output_data = {'error': ''}
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)

    sellerId = request.json['sellerId']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    emailid = request.json['email']
    phoneNo = request.json['phoneNo']
    pwd = request.json['pwd']
    confirmPwd = request.json['confirmPwd']
    reg = mongo.db.user_details
    if reg.query.filter(reg.email == emailid).count() > 0:
        output = "The provided E-mail is already in use by another user."
        return jsonify({"result": output})
    else:
    _hashed_pwd = generate_password_hash(pwd)
    _hashed_confirmPwd = generate_password_hash(confirmPwd)
    user = reg.insert({
        'sellerId': sellerId,
        'firstName': firstName,
        'lastName': lastName,
        'email': emailid,
        'phoneNo': phoneNo,
        'pwd': _hashed_pwd,
        'confirmPwd': _hashed_confirmPwd})
    db.session.add(user)
    db.session.commit()
    data = reg.find_one({"_id": user})
    return jsonify({"result": data})


@app.route('/api/user/signin/', methods=[ 'GET'])
def sign_in():
    output_data = {'error': ''}
    if not request.json:
        output_data['error'] = ERROR_NotJson
        return jsonify(output_data)
    emailid = request.json['email']
    pwd = request.json['pwd']
    if len(emailid) > 1 :
       if len(pwd) > 1:
          result = mongo.db.user_details.query.filter({'email': emailid, 'pwd': check_password_hash(pwd)})
          if result.count() > 0:
              if result['disable']=='false':
                  for doc in result:
                    doc['_id'] = str(doc['_id'])
                    output = "Successfully logged in"
                    output_data['result'] = doc+output
              else:
                  output_data = "User Has been Disbled"
                  return jsonify({"result": output_data})

          else:
                output_data = "Invalid Login ID or password"
                return jsonify({"result": output_data})

       else:
             output_data['error'] = "valid password required"

    else:
        output_data['error'] = "valid Email-iD required"

    return jsonify(output_data)


@app.route('/api/user/<email>', methods=['GET','UPDATE'])
def user(email):
    if request.method == 'GET':
        signin = mongo.db.user_details
        user = signin.find_one({'email': email})
        if user:
            output = (
                {
                    "sellerId": user['sellerId'],
                    "firstName": user['firstName'],
                    "lastName": user['lastName'],
                    "email": user['email'],
                    "phoneNo": user['phoneNo'],
                    "pwd": user['pwd'],
                    "profileImg": user['profileImg'],
                    "city": user['city'],
                    "state": user['state'],
                    "pincode": user['pincode']
                }
            )
        else:
            output = "No Result Found"
        return jsonify({"result": output})
    if request.method == 'UPDATE':
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        profileImg = request.json['profileImage']
        city = request.json['city']
        state = request.json['state']
        pincode = request.json['pincode']

        update = mongo.db.user_details
        output = update.update_one(
            {"email": email},
            {
                "$set": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "profileImage": profileImg,
                    "city": city,
                    "state": state,
                    "pincode": pincode
                }
            }
        )
        print('\nRecords updated successfully\n')
        return jsonify({"result": output})


# bank details-------------------
@app.route('/api/userBankDetails/<sellerId>', methods=['POST','GET'])
def addBankDetails(sellerId):
    details = mongo.db.bank_details
    if request.method == 'POST':
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
            data = details.find_one({"_id": bankDetail})
            return jsonify({"result": data})
        except Exception as e: \
                print(str(e))
    else:
        user = details.find_one({'sellerId': sellerId})
        if user:
            output = (
                {
                    "sellerId": user['sellerId'],
                    "accountNo": user['accountNo'],
                    "accountHolderName": user['accountHolderName'],
                    "bankBranch": user['bankBranch'],
                    "address": user['address'],
                    "state": user['state'],
                    "accountType": user['accountType'],
                    "bankName": user['bankName'],
                    "ifscCode": user['ifscCode'],
                    "city": user['city'],
                    "pincode": user['pincode'],
                    "primaryAccount": user['primaryAccount']
                }
            )
        else:
            output = "No Result Found"
        return jsonify({"result": output})

 # add company details-----


# companyDetails-----
@app.route('/api/userCompanyDetails/<sellerId>', methods=['POST','GET'])
def companyDetails(sellerId):
        details = mongo.db.company_details
        if request.method == 'POST':
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
                data = details.find_one({"_id": company_detail})
                return jsonify({"result": data})
            except Exception as e:
                print(str(e))
        else:
            user = details.find_one({'sellerId': sellerId})
            if user:
                output = (
                    {
                        "sellerId": user['sellerId'],
                        "companyId": user['companyId'],
                        "companyName": user['companyName'],
                        "displayName": user['displayName'],
                        "companyPhoneNo": user['companyPhoneNo'],
                        "yearOfExperience": user['yearOfExperience'],
                        "companyEmail": user['companyEmail'],
                        "city": user['city'],
                        "state": user['state'],
                        "pincode": user['pincode'],
                        "tanNo": user['tanNo'],
                        "tradingType": user['tradingType'],
                        "natureOfTrading": user['natureOfTrading'],
                        "description": user['description'],
                        "gst": user['gst'],
                        "companyLogo": user['companyLogo'],
                        "panNo": user['panNo'],
                        "status": user['status'],
                        "remarks": user['remarks'],
                        "dateOfCreation": user['dateOfCreation']
                    }
                )
            else:
                output = "No Result Found"
            return jsonify({"result": output})


@app.route('/disableUser')
def disableUser():
    reg = mongo.db.user_details
    _id=reg.insert({
        'disable': 'true'})
    session.pop('user', None)
    data = reg.find_one({"_id": _id})
    return jsonify({"result": data})



if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
