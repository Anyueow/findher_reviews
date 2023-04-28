from flask import Blueprint, request, jsonify, make_response, session
import json
from src import db
from datetime import datetime

users = Blueprint('users', __name__)

# Adding a new user 
@users.route('/users', methods=['POST'])
def add_user():
    cursor = db.get_db().cursor()

    user_info = request.json

    user_tuple = f"('{user_info.get('username', 'NULL')}', '{user_info.get('email', 'NULL')}', '{user_info.get('password', 'NULL')}')"
    
    query = f"INSERT INTO users(username, email, password) VALUES {user_tuple}"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added user into database."

#web:4000/c/customers

# Getting all users 
@users.route('/users', methods=['GET'])
def get_users():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT * FROM users")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

@users.route('/login', methods=['POST'])
def login():
    cursor = db.get_db().cursor()

    username = request.json.get('username')
    password = request.json.get('password')

    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    if user:
        # User is valid, return success response
        response_data = {'message': 'Login successful'}
        status_code = 200
    else:
        # User is invalid, return error response
        response_data = {'message': 'Invalid username or password'}
        status_code = 401

    response = make_response(jsonify(response_data), status_code)
    response.mimetype = 'application/json'
    return response

@users.route('/users/userid/<username>', methods=['GET'])
def get_user_id(username):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
    user_id = cursor.fetchone()
    if user_id:
        return jsonify({'user_id': user_id[0]}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    users.run(debug=True)

@users.route('/users/username/<user_id>', methods=['GET'])
def get_username(user_id):
    
    cursor = db.get_db().cursor()
    cursor.execute("SELECT username FROM users WHERE user_id=%s", (user_id,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'


    return the_response

@users.route('/users/<user_id>/workplaces', methods=['POST'])
def add_workplace(user_id):
    # Retrieve workplace information from request body
    workplace_info = request.json

    # Validate required fields
    if not all(key in workplace_info for key in ['company_name', 'industry', 'location', 'website']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Insert workplace into database
    cur = db.connection.cursor()
    cur.execute('INSERT INTO workplaces (company_name, industry, location, website, number_of_employees) VALUES (%s, %s, %s, %s, %s)',
                (workplace_info['company_name'], workplace_info['industry'], workplace_info['location'], workplace_info['website'], workplace_info.get('number_of_employees')))
    db.connection.commit()
    cur.close()

    return jsonify({'message': 'Workplace added successfully'}), 201

# Write review API
@users.route('/users/<user_id>/workplaces/<workplace_id>/reviews', methods=['POST'])
def write_review(user_id, workplace_id):
    # Retrieve review information from request body
    review_info = request.json

    # Validate required fields
    if not all(key in review_info for key in ['content', 'rating']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Insert review into database
    cur = db.connection.cursor()
    cur.execute('INSERT INTO reviews (user_id, workplace_id, content, rating, posted_date) VALUES (%s, %s, %s, %s, NOW())',
                (user_id, workplace_id, review_info['content'], review_info['rating']))
    db.connection.commit()
    review_id = cur.lastrowid
    cur.close()

    # Insert review ratings into database
    ratings = review_info.get('ratings', {})
    for aspect, score in ratings.items():
        cur = db.connection.cursor()
        cur.execute('INSERT INTO ratings (review_id, aspect, score) VALUES (%s, %s, %s)',
                    (review_id, aspect, score))
        db.connection.commit()
        cur.close()

    return jsonify({'message': 'Review added successfully'}), 201