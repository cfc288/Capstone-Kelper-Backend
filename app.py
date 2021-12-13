from flask import Flask, jsonify, after_this_request
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from peewee import *
from peewee import _StringField
from flask import Flask, render_template
from flask_basicauth import BasicAuth



from resources.users import users
from resources.clients import clients
from resources.incidents import incidents
from resources.messages import messages

# from resources.redemption import redemption?


import models

# from models import User
from flask_login import UserMixin
from peewee import _StringField

from flask_cors import CORS

from flask_login import LoginManager

import os 

from dotenv import load_dotenv
load_dotenv()

DEBUG=True 

PORT=8000

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'


app.secret_key = os.environ.get("FLASK_APP_SECRET")
#print('Flask app secret:  ', os.environ.get("FLASK_APP_SECRET"))
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


#2 -> instantiate the loginManager to actually get a login_manager
login_manager = LoginManager()



#3 -> actually connect the app with the login_manager
login_manager.init_app(app) 



# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# admin.add_view(ModelView(Person, db.session))


# admin.add_view(ModelView(User, db.session))

@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        #IMPORTANT CHANGE, USE GET_BY_ID DOCS SAY USE .get but that is not correct as of 20Nov2021
        #per the docs "It should return none" (not raise an eception)
        # if the ID is not valid
        return user
    except models.DoesNotExist:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data={
            'error':'User not logged in',
            'link':'link here' #if you wanted to add a reroute to the front end
            },
        message="You must be logged in to access this material.",
        status=401
    ), 401
        





# #Cors stuff / notes here
CORS(clients, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(incidents, origins=['http://localhost:3000'], supports_credentials=True)
CORS(messages, origins=['http://localhost:3000'], supports_credentials=True)
# CORS(redemption, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(clients, url_prefix='/api/v1/clients')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(incidents, url_prefix='/api/v1/incidents')
app.register_blueprint(messages, url_prefix='/api/v1/messages')
#app.register_blueprint(messages, url_prefix='/api/v1/messages')

# we don't want to hog up the SQL connection pool
# so we should connect to the DB before every request
# and close the db connection after every request


#this is middleware
@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

@app.route('/') 
def hello():
    return 'Hellows'



# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()




if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)