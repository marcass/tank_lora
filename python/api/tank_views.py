# Tasks of flask application:
# - form api for data retreival via display option (SPA/telegram)
# - Authentication management
# - User management

# USAGE:
# INSTALL: sudo pip install flask flask-cors pyopenssl
# START REST API with:
#    FLASK_APP=keyserver.py flask run
# START REST and WebSockets with:
#    gunicorn -k flask_sockets.worker keyserver:app
#
# START REST API WITH ADMIN AUTH:
# python views.py admin pass

# In another terminal:
# curl -X GET http://127.0.0.1:5000/users

# curl -X GET http://127.0.0.1:5000/listallowed

# curl -X GET http://127.0.0.1:5000/door/status

# curl -X POST -H "Content-Type: application/json" -d '{"door":"topgarage", "pincode":"000"}' http://127.0.0.1:5000/usekey
# Response: {"pin_correct": False}

# curl -X POST -H "Content-Type: application/json" -d '{"door":"topgarage", "pincode":"1111"}' http://127.0.0.1:5000/usekey
# Response:  {"pin_correct": True}

# curl -X POST -H "Content-Type: application/json" -d '{"door":"topgarage", "pincode":"1111"}' http://127.0.0.1:5000/usekey
# Response:  {"pin_correct": False} # NOW FALSE because it was a burn code!

# curl -X POST -H "Content-Type: application/json" -d '{"username": "max", "keycode": "AAB23", "doorlist":["topgarage", "frontdoor", "bottomgarage"], "enabled":"1"}' http://127.0.0.1:5000/user
# Response:  {  "Status": "Added key" }

# curl -X POST -H "Content-Type: application/json" -d '{"username": "mw", "keycode": "1111", "doorlist":["topgarage", "frontdoor"], "enabled":"1"}' http://127.0.0.1:5000/user

# curl -X POST -H "Content-Type: application/json" -d '{"username": "burner", "keycode": "1111", "doorlist":["topgarage"], "enabled":"1"}' http://127.0.0.1:5000/user

# curl -X POST -H "Content-Type: application/json" -d '{"username": "burner", "keycode": "1111", "doorlist":["topgarage",  "frontdoor", "bottomgarage"], "enabled":"1"}' http://127.0.0.1:5000/user
# Response:  {  "Status": "Added key" }

#allowed values are: topgarage, frontdoor, bottomgarage
#curl -X POST -H "Content-Type: application/json" -d '{"door":"topgarage", "pincode":"00003"}' http://127.0.0.1:5000/usekey
# Response:  {  "pin_correct": true}

#curl -X PUT -H "Content-Type: application/json" -d '{"door":"topgarage","status":"opened"}' http://127.0.0.1:5000/door/status
# Response:  { "door":"top garage", "status": "opened"}

#curl -X GET -H "Content-Type: application/json" -d '{"days":"10"}' http://127.0.0.1:5000/getlog
# Response:  {  log stuff in here }

# curl -X DELETE -H "Content-Type: application/json" -d '{"username":"mw"}' http://127.0.0.1:5000/user

# curl -X GET -H "Content-Type: application/json" -d '{"username":"max"}' http://127.0.0.1:5000/user

# curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"password"}' http://127.0.0.1:5000/auth
#response = {
#  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMGU4OTg2NS0wNjM5LTQ3ZDEtYWU0YS1hYTg4ODQxNDIwNjciLCJleHAiOjE1MDg0NTU2NDgsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTA4NDU0NzQ4LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTA4NDU0NzQ4LCJpZGVudGl0eSI6ImFkbWluIn0.NT7t_17Hd3hT6_uTwy5FgGSN-koq8UeybEEKaLbRjIk",
#  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MWZmMDcxMC1hYjFlLTRhMTYtYTU1NS0yZjY0NjdlZDgyZjgiLCJleHAiOjE1MTEwNDY3NDgsImlhdCI6MTUwODQ1NDc0OCwidHlwZSI6InJlZnJlc2giLCJuYmYiOjE1MDg0NTQ3NDgsImlkZW50aXR5IjoiYWRtaW4ifQ.MMOMZCLxJbW9v2GwIgndtDZq_VpCKsueiqwXLgU04eg"
#}

#curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMGU4OTg2NS0wNjM5LTQ3ZDEtYWU0YS1hYTg4ODQxNDIwNjciLCJleHAiOjE1MDg0NTU2NDgsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTA4NDU0NzQ4LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTA4NDU0NzQ4LCJpZGVudGl0eSI6ImFkbWluIn0.NT7t_17Hd3hT6_uTwy5FgGSN-koq8UeybEEKaLbRjIk" http://127.0.0.1:5000/listallowed
import sys
import re
import sql
import plot
from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
import json
# import views_auth
from init import app, jwt
# from flask_jwt_extended import jwt_required, \
#     create_access_token, jwt_refresh_token_required, \
#     create_refresh_token, get_jwt_identity

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/listallowed", methods=['GET',])
# @jwt_required
def list_allowed_users():
    '''
    List allowed users
    ["admin":["max", "mw", "etc"], "user":[...]]
    '''
    return jsonify(sql.get_allowed()), 200

@app.route("/user", methods=['POST',])
# @jwt_required
def add_user():
    '''
    Add a new user to everything.
    '''
    content = request.get_json(silent=False)
    #{"username":invalid", "keycode":"invalid", "doorlist":["topgarage","frontdoor","bottomgarage"], "enabled":"1"}
    #{"username":pell", "password":"blah","keycode":"00003", "doorlist":["topgarage","frontdoor","bottomgarage"], "enabled":"1"}
    timeStart = None
    timeEnd = None
    doorlist = None
    if content.has_key('timeStart'):
        # print 'has time start'
        timeStart = content['timeStart'] # parse this to datetime in sql script
    else:
        content.update({'timeStart':0})
        # print 'making timeStart content = '+str(content)
    if content.has_key('timeEnd'):
        timeEnd = content['timeEnd'] # parse this to datetime in sql scrip
    else:
        content.update({'timeEnd':0})
    if not keycode_validation(content['keycode']):
        return jsonify({'status':'keycode failure'}), 200
    #sql.write_userdata(content)
    return jsonify(sql.write_userdata(content)), 200

@app.route("/user/<username>", methods=['DELETE',])
# @jwt_required
def remove_user(username):
    '''
    Remove Username in user userAuth table, and update all tables...
    {'username':'mw'}
    '''
    sql.delete_user(username)
    resp = {}
    return jsonify(resp), 200

@app.route("/auth/user/<username>", methods=['GET',])
# @jwt_required
def get_user_role(username):
    '''

    '''
    content = request.get_json(silent=False)
    password = request.json.get('password', None)
    # print content
    return jsonify(sql.auth_user(username, password)), 200

@app.route("/user/data/<username>", methods=['GET',])
# @jwt_required
def get_user_data(username):
    '''
    Receives: nothing
    Returns {'username': max, 'role':'user'}
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.fetch_user_data(username)), 200

# @app.route("/user", methods=['GET',])
# @jwt_required
# def get_user():
#     '''
#     Receives: {'username':'max'}
#     Returns {'username':, }
#     '''
#     content = request.get_json(silent=False)
#     return jsonify(sql.fetch_user_data(content['username'])), 200

@app.route("/user", methods=['PUT',])
# @jwt_required
def update_user():
    '''
    Select Username and update in user. Json must contain old username
    #{"old_username":"pell", "username":pell", "role":"admin"}

    curl -X PUT -H "Content-Type: application/json" -d '{"username":"max","role":"admin(or user)"}' http://127.0.0.1:5000/user
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.write_userdata(content)), 200

@app.route("/users", methods=['GET',])
# @jwt_required
def get_users():
    '''
    Returns [{'username':[blah, blah], }]
    '''
    return jsonify(sql.get_all_users()), 200

@app.route("/tanks", methods=['GET',])
# @jwt_required
def get_tanks():
    '''
    Returns all possible tank names in db [{'name':[tank1','tank2',...], 'id':[1,2...], diam":[], "max":[], "min":[], "min_vol":[], "min_percent":[], "line_colour":[], "status":[]}]
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.get_all_tanks()), 200
# up to here
@app.route("/tank/status", methods=['GET',])
@jwt_required
def getStatus():
    content = request.get_json(silent=False)
    return jsonify(sql.get_tank_status()), 200

@app.route("/door/status/<door>", methods=['GET',])
@jwt_required
def getADoorStatus(door):
    content = request.get_json(silent=False)
    return jsonify(sql.get_adoorstatus(door)), 200

@app.route("/door/log/<door>", methods=['POST',])
@jwt_required
def getLog(door):
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.get_doorlog(door, content)), 200

@app.route("/door/status", methods=['PUT',])
@jwt_required
def update_status():
    content = request.get_json(silent=False)
    sql.update_doorstatus(content["status"], content['door'])
    return jsonify(content), 200

@app.route("/getlog", methods=['GET',])
@jwt_required
def getAccessLog():
    '''
    curl -X GET -H "Content-Type: application/json" -d '{"days":"5"}' http://127.0.0.1:5000/getlog
    '''
    content = request.get_json(silent=False)
    resp = get_access_log(content['days'])
    return jsonify(resp), 200

try:
    sql.setup_admin_user(sys.argv[1], sys.argv[2])
except:
    pass

if __name__ == "__main__":
    app.run()
#    app.run(ssl_context='adhoc')
#    from gevent import pywsgi
#    from geventwebsocket.handler import WebSocketHandler
#    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
#    server.serve_forever()
