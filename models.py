from peewee import *
import datetime
# from flask import Flask, jsonify
# from flask_admin import Admin
# from flask_sqlalchemy import SQLAlchemy
# from flask_admin.contrib.sqla import ModelView
# from peewee import *
# from peewee import _StringField
# from flask import Flask, render_template
# from flask_basicauth import BasicAuth
# from app import app


#login/logout
# see docs--> flask-login.readthedocs.io/en/latest/
from flask_login import UserMixin
#from peewee import _StringField

DATABASE = SqliteDatabase('kelperDB.sqlite')


# db = SQLAlchemy(app)

# admin = Admin(app)

# admin.add_view(ModelView(Client, db.session))
######################################################
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    company = CharField(default='none')
    location = CharField()
    employee_title = CharField(default='none')
    is_employee = BooleanField(default=False)
    is_client=BooleanField(default=False)
    is_admin=BooleanField(default=False)

    class Meta:
        database = DATABASE 


####################################################
class Client(Model):
    name = CharField()
 

    class Meta:
        database = DATABASE


####################################################

class Incident(Model):
    
    employee_data_ref = ForeignKeyField(User, backref='employee_ref')

    client_referrence = ForeignKeyField(Client, backref='client_ref')
    
    incident_event = CharField()

    created_at = DateTimeField(default=datetime.datetime.now)

    flagged_for_review = BooleanField(default=False)
    # owner = ForeignKeyField(User, backref='dogs')
    # # this ForeignKeyField will let us go some_dog.owner to get user that owns this dog
    #     #the backref will let us go some_user.dogs to get a list of dogs owner by that user


    class Meta:
        database = DATABASE

######################################################

class Messages(Model):
    sender = ForeignKeyField(User, backref='sender')

    reciever = ForeignKeyField(User, backref='reciever')

    message = CharField()

    class Meta:
        database = DATABASE 

##############################################


# db = SQLAlchemy()

# admin = Admin()


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))





#     class Meta:
#             database = DATABASE 

# admin.add_view(ModelView(Person, db.session))

######################################################
def initialize():
    DATABASE.connect() 


    DATABASE.create_tables([User, Client, Incident, Messages], safe=True)
    print("Connected to the DB and created tables if they didnt already exist")


    DATABASE.close()