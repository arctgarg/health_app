from flask import render_template, jsonify, request
from health_app import app, bcrypt
from health_app.models import User, Record
from health_app import db
import jwt
from datetime import datetime, timedelta
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers["authorization"]
        # //TODO - correct parsing of jwt token
        # if not token:
        #     return jsonify("token is missing")
        # try:
        #     data = jwt.decode(token, app.config['SECRET_KEY'])
        # except:
        #     return jsonify("invalid token"), 401

        # user = Users.query.filter(username = data["user"]).first()
        user = User.query.filter_by(id = 1).first()
        if not user :
            return jsonify("invalid token")

        return f(user, *args, **kwargs)
    return decorated

# def roles_required(f, roles):
#     @wraps(f)
#     def decorated(*args, **kwargs):


@app.route('/users', methods = ['POST'])
@token_required
def user():
    content = request.json
    response_type = request.headers["accept"]
    hashed_password = bcrypt.generate_password_hash(content["password"]).decode("utf-8")
    user = User(username=content["username"], password = hashed_password, email = content["email"])
    db.session.add(user)
    db.session.commit()
    print user.password
    return jsonify(user.id)


@app.route('/users/<int:user_id>', methods = ['GET'])
@token_required
def getUser(user, user_id):
    if user_id != user.id:
        return jsonify("Unauthorized access")
    return jsonify(user.username)
    # // TODO -> return entire user object from here


@app.route('/users/<int:user_id>', methods = ['PUT'])
@token_required
def getUser(user, user_id):
    if user_id != user.id:
        return jsonify("Unauthorized access")
    for key in request.json:
        print key
        user[key] = request.json[key]
    db.session.add(user)
    db.session.commit()
    return jsonify(user.username)
    # // TODO -> return entire user object from here


@app.route('/users/<int:user_id>/records', methods = ['POST'])
@token_required
def addRecord(user, user_id):
    if(user_id != user.id):
        return jsonify("Unauthorized")
    data = request.json
    calories = 100
    if "calories" in data:
        calories = data["calories"]
    record = Record(food_item = data["food_item"], calories = calories, date_posted = datetime.utcnow(), user_id = user.id, user = user)
    db.session.add(record)
    db.session.commit()
    return jsonify(record.id) # TODO : return the record object here


@app.route('/users/<int:user_id>/calories/<int:calories>', methods = ['POST'])
@token_required
def setCalorieLimit(user, user_id, calories):
    if user.id != user_id:
        return jsonify("Unauthorized")



@app.route('/users/<int:user_id>/records', methods = ['GET'])
@token_required
def getRecords(user, user_id):
    if(user_id != user.id):
        return jsonify("Unauthorized")
    for record in user.records:
        print record
    return jsonify(user.username)

@app.route('/users/<int:user_id>/unblock', methods = ['PUT'])
@token_required
def getRecords(user, user_id):
    #TODO : check if user is admin/user manager
    if not user.is_account_blocked:
        return jsonify("Account already in unblocked state")
    user.is_account_blocked = 0;
    db.session.add(user)
    db.session.commit()
    return jsonify("Your account has been unblocked.")


@app.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email = email).first()
    message = ""
    if user :
        if not bcrypt.check_password_hash(user.password, password):
            user.no_of_failed_attemps += 1
            if user.no_of_failed_attemps == 3:
                user.is_account_blocked = 1
                message = "Your account has been blocked."
            else:
                message = f"Incorrect password. You can try for {3 - user.no_of_failed_attemps} times before your account gets blocked."
            db.session.add(user)
            db.session.commit()
        else:
            token = jwt.encode({"user" : user.username, "exp" : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({"token" : token})

    return jsonify("Invalid email id")


@app.route('/register', methods = ['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password = hashed_password, email = data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify("Your account has been created")


# @app.route('/user/<int:user_id>/image', methods = ['POST'])
