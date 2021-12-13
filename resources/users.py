# import re
import models
from flask import Blueprint, json, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
                        
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', 'users')


# @users.route('/', methods=['GET'])
# def test_user_resource():
#     return "user resource works"



# register route
@users.route('/register', methods=['POST'])
def register():
    # this interm step analogous to making sure we can log req.body in express
    # note: we had to send JSON from postman (choose raw, select JSON from the drop menu, type a perfect JSON object with double quotes around keys)
    payload = request.get_json()
    # print('request.get_json(): ', request.get_json())
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    # print(payload)

    # see if the user exists
    try:
        models.User.get(models.User.email == payload['email'])
        # this will throw and error ("models.DoesNotExist exception")

        # extra -- make it so that this code also prevents duplicate usernames
        # if we get this error, the user is not found ("DoesNotExist"),
        # response: "user with that email already exists"
        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401
    except models.DoesNotExist: 
        # except is like a catch in JS
        # the user does not exist
        # scramble the password with bcrypt
        pw_hash = generate_password_hash(payload['password'])

        # create them
        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash,
            company=payload['company'],
            location=payload['location'],
            employee_title=payload['employeeTitle'],
            is_employee=payload['isEmployee'],
            is_client=payload['isClient'],
            is_admin=payload['isAdmin']
        )

        print('created_user', created_user)

        # this is where we will actually use flask-login
        # this "logs in" the user and starts a session
        # https://flask-login.readthedocs.io/en/latest/#login-example
        login_user(created_user)

        # respond with the new object and success message
        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)

        # we can't jsonify the password (generate_password_hash gives us something in type "bytes" which is unserializable)
        # plus we shouldn't be send back the encrypted pw anyways
        print(type(created_user_dict['password']))
        # so let's just get rid of it
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201


# LOGIN ROUTE
@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    # payload['company'] = payload['company']
    # payload['location'] = payload['location']
    # payload['employee_title'] = payload['employee_title']
    # payload['is_employee'] = payload['is_employee']
    # payload['is_client'] = payload['is_client']
    # payload['is_admin'] = payload['is_admin']



    # look up the user by email
    try:
        # user = models.User.get(models.User.email == payload['email'])
        user = models.User.get(models.User.username == payload['username'])

    # if we got here, we know a user with this email exists
        user_dict = model_to_dict(user)
        # check the users pw using bcrypt
        # check_password_hash: 2 args
        # 1. the encrypted pw you are checking against
        # 2. the pw attempt you are trying to verify
        # https://flask-bcrypt.readthedocs.io/en/latest/
        password_is_good = check_password_hash(user_dict['password'], payload['password'])

        if (password_is_good):
            # LOG THE USER IN!!! using Flask-Login
            login_user(user) # in express we did this manually by setting stuff in session
            print(f"{current_user.username} is currently_user.name in POST login")
            print('model_to_dict(user): ', model_to_dict(user))
            # respond --- all good -- remove the pw first
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                # message=f"Successfully logged in {user_dict['email']}",
                message=f"Successfully logged in {user_dict['username']}",
                status=200
            ), 200
        else:
            print("Username doesn't work") #for the backend
            return jsonify(
                data={},
                message="Email or password is incorrect", # let's be vague
                status=401
            ), 401 

        # else if pw is bad
            #respond -- bad username or password
    except models.DoesNotExist:
    # else if they don't exist
        print('email not found')
        # respond -- bad username or password
        return jsonify(
            data={},
            message="Email or password is incorrect", # let's be vague
            status=401
        ), 401


#route for demonstration
#it will shows us who is logged in, and we can now access that information via current_user
#this is what setting up user_loader in app.py allowed us to do
@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    #check to make sure user is authenticated
    if not current_user.is_authenticated:
        return jsonify(
            data={},
            message="No user currently logged in",
            status=401
        ), 401

    else:
        #we can acccess current_user because we called login_user
        print('current user: ',current_user)
        print(f"{current_user.username} is current_user.name in GET route for logged_in_user")
        print('type(current_user): ', type(current_user))
        user_dict = model_to_dict(current_user)
        user_dict.pop('password')

        return jsonify(
            data=user_dict,
            message=f"Currently logged in as {user_dict['email']}.",
            status=200
        ), 200



#LOGOUT ROUTE
@users.route('/logout', methods=['GET'])
def logout():


    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
    ), 200




 #GET all users
@users.route('/', methods=['GET'])
@login_required
def client_index():
    result = models.User.select()
    print('result = models.User.select(): ', result)

    user_dicts = [model_to_dict(user) for user in result]
    for user_dict in user_dicts:
        user_dict.pop('password')
    print('client_dict', user_dicts)
    return jsonify({
    'data' : user_dicts, 
    'message' : f'Successfully found {len(user_dicts)} client(s)',
    'status': 200
    })  