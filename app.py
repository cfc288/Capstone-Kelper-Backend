from flask import Flask, jsonify
from flask_admin import Admin
import flask_admin
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
print('Flask app secret:  ', os.environ.get("FLASK_APP_SECRET"))

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



@app.route('/') 
def hello():
    return 'Hellows'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)