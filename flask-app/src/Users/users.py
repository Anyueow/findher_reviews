from flask import Blueprint, request, jsonify, make_response
import json
from src import db
from datetime import datetime

users = Blueprint('users', __name__)

# Adding a new user 
@users.route('u/users', methods=['POST'])
def add_user():
    cursor = db.get_db().cursor()

    user_info = request.json

    user_tuple = f"('{user_info.get('username', 'NULL')}', '{user_info.get('email', 'NULL')}', '{user_info.get('password', 'NULL')}')"
    
    query = f"INSERT INTO users(user_id, username, email, password) ) VALUES {user_tuple}"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added user into database."

#web:4000/c/customers