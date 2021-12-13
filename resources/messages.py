from peewee import query_to_string
import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

messages = Blueprint('messages', 'messages')

# main route: api/v1/messages

# GET route
#this returns all the incidents no matter who the user/client is
@messages.route('/', methods=['GET'])
@login_required
def main_index():
    try:
        result = models.Messages.select()

        message_dicts = [model_to_dict(message) for message in result]
        # for message_dicts in message_dicts:
        #     message_dicts['sender'].pop('password')

        return jsonify({
        'data' : message_dicts, 
        'message' : f'Successfully found {len(message_dicts)} incident reports',
        'status': 200
        }) 
    except models.DoesNotExist:
        return jsonify ({
            'message' : 'unable to comply'
        }) 


#######################################

#GET messages route for per user
@messages.route('/allmessagesperuser', methods=['GET'])
@login_required
def index_per_user_messages():
    
    current_user_message_dicts = [model_to_dict(message) for message in current_user.reciever]

    for message_dict in current_user_message_dicts:
        print('incident_dict (in /allreportsperuser): ', message_dict)
        #
        message_dict['sender'].pop('password')
        #message_dict['sender'].pop('username')
        message_dict['sender'].pop('email')

        message_dict['reciever'].pop('password')
        #message_dict['reciever'].pop('username')
        message_dict['reciever'].pop('email')
        print('current_user_message_dicts',current_user_message_dicts)
    
    return jsonify({
        'data': current_user_message_dicts,
        'message': f"Successfully found {len(current_user_message_dicts)} reports for {current_user}",
        'status': 200
    }), 200



############################################
#CREATE

# #POST /api/v1/incidents/
# #note for this route needs the trailing slash (/)
@messages.route('/newmessage/reciever/<id>', methods=['POST'])
#(in form on front end have dropdown of all clients and ref client and put into url)
@login_required
def create_message(id):
    payload = request.get_json()

    print('payload in POST messages route: ', payload) # you should see request body in your terminal 
    
    try:
        reciever = models.User.get_by_id(id)
        #checks for id
        print('model_to_dict(reciever):', model_to_dict(reciever))

        new_message = models.Messages.create(message=payload['message'], sender=current_user.id, 
        reciever=reciever.id )

        print('new_message under POST/messages: ', new_message)

        # just prints the ID -- check sqlite3 to see the data
                    # run sqlite3 dogs.sqlite and run SQL queries in the CLI

    #print(new_dog.__dict__)
    # this might be useful, sometimes it gives you better info
    # dict is a class attribute automatically added to python class
    #print(dir(new_dog)) # look at all of this models' stuff and the pretty methods!!
        # print('model_to_dict(new_message): ', model_to_dict(new_message))

        message_dict = model_to_dict(new_message)
        
        print('message_dict[sender]', message_dict['sender'])
        message_dict['sender'].pop('password')
        #message_dict['sender'].pop('username')
        message_dict['sender'].pop('email')

        print('reciever', message_dict['reciever'])
        message_dict['reciever'].pop('password')
        # #message_dict['reciever'].pop('username')
        message_dict['reciever'].pop('email')
        
        

        return jsonify(
            data= message_dict,
            message='Successfully created Message!',
            status=201
        ), 201
      
    except models.DoesNotExist:
        print('User not found')

        return jsonify(
            data={},
            message="User does not exist",
            status=401
        ), 401
################################################

#DELETE route

@messages.route('/<id>', methods=['Delete'])
@login_required
def delete_message(id):
    print('*message id', id)
    #we are trying to delete the dog with the id that comes through a param
    delete_query = models.Messages.delete().where(models.Messages.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print('nums_of_rows_deleted = delete_query.execute()', nums_of_rows_deleted)

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} reports with id {id}",
        satus=200
    ), 200   