import random

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'omplus'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/omplus'

mongo = PyMongo(app)
db = mongo.db


# ---------------------seller info----------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------

@app.route('/api/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    sellerId = request.json[random.randint(111111,999999)]
    firstName = request.json['Chandra']
    lastName = request.json['Prakash']
    email = request.json['Chandra.pkash@gmail.com']
    phoneNo = request.json['7070764734']
    pwd = request.json['mongodb']
    confirmPwd = request.json['mongodb']

    user = db.user_details.insert({'sellerId': sellerId, 'firstName': firstName,
                                     'lastName': lastName, 'email': email,
                                     'phoneNo': phoneNo, 'password': pwd,
                                     'confirmPassword': confirmPwd})
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=5000)