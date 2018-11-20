import sys
sys.path.append('..')

from cursor_wrapper import get_cursor

import pyodbc
from flask import Flask, jsonify, request
app = Flask(__name__)

cursor = get_cursor()

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    user_json = request.get_json()
    quote_wrap = lambda astr: '"' + astr + '"' if astr[0] != '"' else astr
    for key in user_json:
        user_json[key] = quote_wrap(user_json[key])
    sql = '''
    INSERT INTO jobbie_db.User (firstName, lastName, email, password)
    VALUES
    ({}, {}, {}, {})
    '''.format(user_json['firstName'], user_json['lastName'], user_json['email'], user_json['password'])
    try:
        cursor.execute(sql)
        cursor.commit()
        return jsonify({'status': 'Registered'})
    except pyodbc.IntegrityError as e:
        print(e)
        return jsonify({'status': 'Not Registered; Duplicate email'})


@app.route('/setinformation', methods=['POST'])
def set_information():
    user_json = request.get_json()
    email = user_json['email']
    del user_json['email']
    user = cursor.execute("SELECT * FROM User WHERE email = '{}'".format(email)).fetchall()[0]
    if user_json['password'] != user.password:
        return jsonify({'status': 'Failed; Incorrect Password'})

    keys, values = list(user_json.keys()), ["'"+val+"'" for val in user_json.values()]

    sql = 'UPDATE User SET '+', '.join([keys[i]+' = '+values[i] for i in range(len(keys))])
    sql += " WHERE email = '{}'".format(email)

    try:
        cursor.execute(sql)
        cursor.commit()
        return jsonify({'status': 'Changed information'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'Error; Information not changed'})
        

if __name__ == "__main__":
    app.run(debug=True)
