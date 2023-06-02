from flask import Blueprint, request, jsonify, make_response, session
import json
from src import db
from datetime import datetime

workplaces = Blueprint('workplaces', __name__)



@workplaces.route('/workplaces', methods=['GET'])
def get_workplaces():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT company_name FROM workplaces")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Define the route for adding a workplace
@workplaces.route('/workplaces', methods=['POST'])
def add_workplace():
    # Get the workplace details from the request body
    company_name = request.json['company_name']
    industry = request.json['industry']
    location = request.json['location']
    website = request.json['website']
   
    # Connect to the database
    
    cursor = db.get_db().cursor()

    # Insert the new workplace into the database
    sql = "INSERT INTO workplaces (company_name, industry, location, website) VALUES (%s, %s, %s, %s)"
    values = (company_name, industry, location, website)
    cursor.execute(sql, values)
    
    db.get_db().commit()
    
    # Return a response indicating success
    return jsonify({'message': 'Workplace added successfully.'}), 200


""'''# getting all workplaces for form 
@workplaces.route('/workplaces/name', methods=['GET'])
def get_workplaces_forms():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT company_name FROM workplaces")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response
'''""
# getting all workplaces for form 
@workplaces.route('/workplaces/names', methods=['GET'])
def get_workplaces_form():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT company_name as label, workplace_id as value FROM workplaces")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

@workplaces.route('<WorkID>/reviews', methods=['POST'])
def add_workplace_rating(WorkID):
    # get the rating from the query parameters
    rating = request.args.get('rating')
    
    # Get the review details from the request body
    workplaceID = request.json['workplace_id']
    rating = request.json['rating']
    content = request.json['content']

    
    # Connect to the database
    
    cursor = db.get_db().cursor()

    # Insert the new workplace into the database
    sql = "INSERT INTO reviews (workplace_id, content, rating) VALUES (%s, %s, %s)"
    values = (workplaceID, rating, content)
    cursor.execute(sql, values)

    db.get_db().commit()
    # return the new rating information

    return jsonify({'workplace_id': WorkID, 'rating': rating, 'message': "review added"}), 201
