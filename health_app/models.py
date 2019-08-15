from datetime import datetime
from health_app import db
import jwt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #TODO : add firstname and lastname instead of username
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20))
    no_of_failed_attemps = db.Column(db.Integer)
    is_account_blocked = db.Column(db.Integer)
    is_account_verified = db.Column(db.Integer)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles')
    records = db.relationship('Record', backref='user', lazy='dynamic')


    def __repr__(self):
        # return f"User({self.username}, {self.email}, {self.image_file})"\
        return self.username


    def __str__(self):
        # return f"User({self.username}, {self.email}, {self.image_file})"\
        return self.username


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories =  db.Column(db.String(20))
    food_item = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        # return f "Record({self.id}, food_item : {self.food_item}, calories : {self.calories}, time : {self.time})"
        return self.food_item

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
