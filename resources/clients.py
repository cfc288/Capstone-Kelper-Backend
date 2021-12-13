import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

clients = Blueprint('clients', 'clients')


# GET ROUTE
#this returns all the clients
@clients.route('/', methods=['GET'])
@login_required
def client_index():
    result = models.Client.select()
    print('result = models.Client.select(): ', result)

    client_dicts = [model_to_dict(client) for client in result]
    # for client_dict in client_dicts:
    #     client_dict['owner'].pop('password')
    print('client_dict', client_dicts)
    return jsonify({
    'data' : client_dicts, 
    'message' : f'Successfully found {len(client_dicts)} client(s)',
    'status': 200
    })  
 


# CREATE ROUTE
@clients.route('/', methods=['POST'])
@login_required
def create_client():
    payload = request.get_json()
    print('payload = request.get_json(), payload: ', payload) # you should see request body in your terminal 
    new_client = models.Client.create(name=payload['name'])
    print('new_client: ', new_client)# just prints the ID -- check sqlite3 to see the data
                   # run sqlite3 kelperDB.sqlite and run SQL queries in the CLI

    print('new_client.__dict__', new_client.__dict__)
    # this might be useful, sometimes it gives you better info
    # dict is a class attribute automatically added to python class

    print('dir(new_client),', dir(new_client)) 
    # look at all of this models' stuff and the pretty methods!!

    client_dict = model_to_dict(new_client)
    #this converts the model to a dict 
    # client_dict['user'].pop('password')

    #dog_dict['owner'].pop('password') takes out the password from returning in the console (for better security) 

    return jsonify(
        data=client_dict,
        message='Successfully created client!',
        status=201
    ), 201





# SHOW ROUTE
# Get one client/by id
# GET api/v1/clients/ <client_id> 
#in express it lookes like: router.get('/:id')
@clients.route('/<id>', methods=['GET'])
@login_required
def get_one_clients(id):
    client = models.Client.get_by_id(id)
    print('client = models.Client.get_by_id(id): ', client)
    
    return jsonify(
        data = model_to_dict(client),
        message = 'Sucess!',
        status = 200
    ), 200


# PUT UPDATE ROUTE
# PUT api/v1/clients/<id>
@clients.route('<id>', methods=['PUT'])
def update_client(id):
    payload = request.get_json()

    models.Client.update(**payload).where(models.Client.id == id).execute()

    return jsonify(
        data = model_to_dict(models.Client.get_by_id(id)),
        message = 'resource updated successfully',
        status = 200,
    ), 200


# Delete /Destroy
#Delete api/v1/dogs/<id>
@clients.route('/<id>', methods=['Delete'])
@login_required
def delete_client(id):
    print('*client id', id)
    #we are trying to delete the dog with the id that comes through a param
    delete_query = models.Client.delete().where(models.Client.id == id)
    nums_of_rows_deleted = delete_query.execute()

    #delete all reports with client
    delete_query_incidents = models.Incident.delete().where(id == models.Incident.client_referrence)
    nums_of_rows_deleted = delete_query_incidents.execute()

    print('nums_of_rows_deleted = delete_query.execute()', nums_of_rows_deleted)

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} client with id {id}",
        status=200
    ), 200   
