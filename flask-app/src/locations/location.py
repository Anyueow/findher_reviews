from flask import Blueprint, jsonify, make_response
import json
from src import db
from datetime import datetime


locations = Blueprint('locations', __name__)

@locations.route('/locations', methods=['GET'])
def get_locations():

    cursor = db.get_db().cursor()

    cursor.execute("SELECT city, state FROM locations")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response
