from peewee import query_to_string
import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

incidents = Blueprint('incidents', 'incidents')

# main route: api/v1/incidents



# GET route
#this returns all the incidents no matter who the user/client is
@incidents.route('/', methods=['GET'])
@login_required
def main_incidents_index():
    result = models.Incident.select()
    print('result = models.Incident.select(): ', result)

    incident_dicts = [model_to_dict(incident) for incident in result]
    try:
        for incident_dict in incident_dicts:
            incident_dict['employee_data_ref'].pop('password')
            print('incident_dicts', incident_dict)
    except:
        print('something went wrong')
    finally:
        return jsonify({
        'data' : incident_dicts, 
        'message' : f'Successfully found {len(incident_dicts)} incident reports',
        'status': 200
        })  



####################################################################

#GET route for per user
@incidents.route('/allreportsperuser', methods=['GET'])
@login_required
def index_per_user():
    result = models.Incident.select()
    print('result = models.Client.select():', result)
    current_user_incident_dicts = [model_to_dict(incident) for incident in current_user.employee_ref]

    for incident_dict in current_user_incident_dicts:
        print('incident_dict (in /allreportsperuser): ', incident_dict)
        incident_dict['employee_data_ref'].pop('password')
        incident_dict['employee_data_ref'].pop('username')
        incident_dict['employee_data_ref'].pop('email')

    
    return jsonify({
        'data': current_user_incident_dicts,
        'message': f"Successfully found {len(current_user_incident_dicts)} reports for {current_user}",
        'status': 200
    }), 200

################################################

#GET route for per client
@incidents.route('/allreportsperclient/<id>', methods=['GET'])
@login_required
def index_per_client(id):
    # result = models.Incident.get client ref - client id()
    # client = models.Client.get_by_id(id)

    # for incident in models.Incident.select(models.Incident.incident_event, models.Client.id, models.Client.name ).join(models.Client).where(models.Client.id == id):
        # print ('model_to_dict(incident): ', model_to_dict(incident))
        # print('incident.incident_event: ',incident.incident_event)
        # print('incident.client_ref: ', incident.client_referrence)
    
    incident_list = []
    
    for incident in models.Incident.select( models.Incident).join(models.Client).switch(models.Incident).join(models.User).where(models.Client.id == id):
        incident_data = model_to_dict(incident)
        incident_data['employee_data_ref'].pop('username')
        incident_data['employee_data_ref'].pop('password')
        incident_data['employee_data_ref'].pop('email')       
        incident_list.append(incident_data) 
        
        

    # client = models.Client.get_by_id(id)
    # query = client.client_ref
    # for item in query:
    #     print('item: ', model_to_dict(item))

    #employee_data
    
    return jsonify({
        'data': incident_list,
        'message': f"Successfully found {len(incident_list)} reports",
        'status': 200
    }), 200


################
#POST route
#new_dog = models.Dog.create(name=payload['name'], owner=current_user.id, breed=payload['breed'])
#defineds owner=payload['owner'], returns user name to front end......
# employee info???
# user_employee_company
# user_employee_location
# user_employee_title
# client_name



#update route?
#PUT /api/v1/incidents/
# PUT api/v1/incidents/<id>
@incidents.route('<id>', methods=['PUT'])
@login_required
def update_incident(id):
    payload = request.get_json()

    models.Incident.update(**payload).where(models.Incident.id == id).execute()
    print('model_to_dict(models.Incident.get_by_id(id))', model_to_dict(models.Incident.get_by_id(id)))
    return jsonify(
        data = model_to_dict(models.Incident.get_by_id(id)),
        message = 'Report updated successfully',
        status = 200,
    ), 200


######################################

# #CREATE/ and or update? an 'incident' route
# #POST /api/v1/incidents/
# #note for this route needs the trailing slash (/)
@incidents.route('/newincident/client/<id>', methods=['POST'])
#(in form on front end have dropdown of all clients and ref client and put into url)
@login_required
def create_incident(id):
    payload = request.get_json()

    print('payload in POST route: ', payload) # you should see request body in your terminal 
    # current_client = models.Client.select('name')

    try:
        client = models.Client.get_by_id(id)
        #checks for id
        print('model_to_dict(client):', model_to_dict(client))

        new_incident = models.Incident.create(incident_event=payload['incident_event'], employee_data_ref=current_user.id, client_referrence=client.id)


        print('new_incident under POST/incidents: ', new_incident)# just prints the ID -- check sqlite3 to see the data
                    # run sqlite3 dogs.sqlite and run SQL queries in the CLI

    #print(new_dog.__dict__)
    # this might be useful, sometimes it gives you better info
    # dict is a class attribute automatically added to python class
    #print(dir(new_dog)) # look at all of this models' stuff and the pretty methods!!

        incident_dict = model_to_dict(new_incident)
        # incident_dict['emlpoyee_data_ref'].pop('password')
        # incident_dict['employee_info'].pop('username')
        # incident_dict['employee_info'].pop('email')
        

        return jsonify(
            data=incident_dict,
            message='Successfully created incident!',
            status=201
        ), 201

    except models.DoesNotExist:
        print('client not found')

        return jsonify(
            data={},
            message="Client does not exist",
            status=401
        ), 401


######################################

#DELETE route
#

@incidents.route('/<id>', methods=['Delete'])
@login_required
def delete_client(id):
    print('*incident id', id)
    #we are trying to delete the dog with the id that comes through a param
    delete_query = models.Incident.delete().where(models.Incident.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print('nums_of_rows_deleted = delete_query.execute()', nums_of_rows_deleted)

    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} reports with id {id}",
        status=200
    ), 200   