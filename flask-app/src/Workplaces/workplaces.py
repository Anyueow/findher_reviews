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