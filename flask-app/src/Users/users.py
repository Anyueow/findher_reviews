from flask import Blueprint, request, jsonify, make_response
import json
from src import db
from datetime import datetime

users = Blueprint('users', __name__)

# Adding a new user 
@users.route('/users/<UsernameId>/<EmailID>/<PassId>', methods=['POST'])
def add_user():
    cursor = db.get_db().cursor()

    user_info = request.json

    
    query = f"INSERT INTO users(user_id, username, email, password) ) VALUES ('{UsernameId}', '{EmailID}', '{PassId}')"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added user into database."
