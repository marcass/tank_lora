# Tasks of flask application:
# - form api for data retreival via display option (SPA/telegram?)
# - Authentication management
# - User management

# USAGE:
# INSTALL: sudo pip install flask flask-cors pyopenssl
# START REST API with:
#    FLASK_APP=keyserver.py flask run
# START REST and WebSockets with:
#    gunicorn -k flask_sockets.worker keyserver:app
#
# START DEV REST API WITH ADMIN AUTH:
# python tank_views.py admin pass

# In another terminal:

# curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"password"}' http://127.0.0.1:5000/auth
#response = {
#  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMGU4OTg2NS0wNjM5LTQ3ZDEtYWU0YS1hYTg4ODQxNDIwNjciLCJleHAiOjE1MDg0NTU2NDgsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTA4NDU0NzQ4LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTA4NDU0NzQ4LCJpZGVudGl0eSI6ImFkbWluIn0.NT7t_17Hd3hT6_uTwy5FgGSN-koq8UeybEEKaLbRjIk",
#  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MWZmMDcxMC1hYjFlLTRhMTYtYTU1NS0yZjY0NjdlZDgyZjgiLCJleHAiOjE1MTEwNDY3NDgsImlhdCI6MTUwODQ1NDc0OCwidHlwZSI6InJlZnJlc2giLCJuYmYiOjE1MDg0NTQ3NDgsImlkZW50aXR5IjoiYWRtaW4ifQ.MMOMZCLxJbW9v2GwIgndtDZq_VpCKsueiqwXLgU04eg"
#}

#curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMGU4OTg2NS0wNjM5LTQ3ZDEtYWU0YS1hYTg4ODQxNDIwNjciLCJleHAiOjE1MDg0NTU2NDgsImZyZXNoIjpmYWxzZSwiaWF0IjoxNTA4NDU0NzQ4LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTA4NDU0NzQ4LCJpZGVudGl0eSI6ImFkbWluIn0.NT7t_17Hd3hT6_uTwy5FgGSN-koq8UeybEEKaLbRjIk" http://127.0.0.1:5000/users
import sys
import re
import sql
import plot
import StringIO
import base64
from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
import json
import views_auth
from init import app, jwt
from flask_jwt_extended import jwt_required, \
    create_access_token, jwt_refresh_token_required, \
    create_refresh_token, get_jwt_identity

@app.route("/")
def hello():
    '''
    curl -X GET http://127.0.0.1:5000/
    '''
    return "Hello World!"

@app.route("/user", methods=['POST',])
# @jwt_required
def add_user():
    '''
    Add a new user to everything.
    curl -X POST -H "Content-Type: application/json" -d '{"username":"pell", "password":"blah", "role":"user"}' http://127.0.0.1:5000/user
    Receives: {"username":pell", "password":"blah", "role":"user"}
    Returns: Nothing
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.write_userdata(content)), 200

@app.route("/user/<username>", methods=['DELETE',])
# @jwt_required
def remove_user(username):
    '''
    Remove Username in user userAuth table, and update all tables...
    curl -X DELETE http://127.0.0.1:5000/<username>
    Receives: nothing
    Returns: {'status':'Error. User '+name+' not deleted'}/{'status':'Success. User '+name+' deleted'}
    '''
    return jsonify(sql.delete_user(username)), 200

# shouldn't this be a POST?
@app.route("/auth/user/<username>", methods=['GET',])
# @jwt_required
def get_user_role(username):
    '''
    Auth check and role fetch.
    curl -X GET -H "Content-Type: application/json" -d '{"password":<userPass>}' http://127.0.0.1:5000/auth/user/<username>
    Receives: {'password':<password>}
    Returns: {'status': 'passed'('failed'), 'role':<role>}
    '''
    content = request.get_json(silent=False)
    password = request.json.get('password', None)
    # print content
    return jsonify(sql.auth_user(username, password)), 200

@app.route("/user/data/<username>", methods=['GET',])
# @jwt_required
def get_user_data(username):
    '''
    curl -X GET http://127.0.0.1:5000/user/data/<username>
    Receives: nothing
    Returns {'username': max, 'role':'user'}
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.fetch_user_data(username, 'username')), 200

@app.route("/user", methods=['PUT',])
# @jwt_required
def update_user():
    '''
    Select Username and update in user. Json must contain old username
    curl -X PUT -H "Content-Type: application/json" -d '{"username": <username>, "col":"username","data":<new_user>"}' http://127.0.0.1:5000/user
    Returns: {'status':'Success','message':'User update success'}
            {'status':'Error', 'message':'Failed as non-unique new user'}
            {'status':'Error', 'message':'Failed to setup user'}
            {'status':'Success'. 'message':'Setup new user'}
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.write_userdata(content)), 200

@app.route("/users", methods=['GET',])
# @jwt_required
def get_users():
    '''
    curl -X GET http://127.0.0.1:5000/users
    Returns {'username':[blah, blah], 'role': [blah blah] }
    '''
    return jsonify(sql.get_all_users()), 200

@app.route("/tank/<name>", methods=['GET',])
# @jwt_required
def get_a_tank(name):
    '''
    curl -X GET http://127.0.0.1:5000/tank/<name>
    Receives: nothing
    Returns dict of tank attributes {'name':'tank1', 'id':'1', diam":, "max":, "min":, "min_vol":, "min_percent":, "line_colour":, "status":}
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.get_tank(name, 'tank')), 200

@app.route("/tanksdict", methods=['GET',])
# @jwt_required
def get_tanks_dict():
    '''
    curl -X GET http://127.0.0.1:5000/tanksdict
    Receives: nothing
    Returns dict of lists db {'name':[tank1','tank2',...], 'id':[1,2...], diam":[], "max":[], "min":[], "min_vol":[], "min_percent":[], "line_colour":[], "status":[]}
    '''
    content = request.get_json(silent=False)
    # print content
    return jsonify(sql.get_all_tanks()), 200

@app.route("/tankslist", methods=['GET',])
# @jwt_required
def get_tanks_list():
    '''
    curl -X GET http://127.0.0.1:5000/tankslist
    Receives: nothing
    Returns list of dicts of all tanks data [{'name':'tank1', 'id':'1', diam":, "max":, "min":, "min_vol":, "min_percent":, "line_colour":, "status":}, {}, {}, ]
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.get_tank_list()), 200

@app.route("/tank/add", methods=['POST',])
# @jwt_required
def add_tank():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name": , "nodeID": , "diam": , "max_payload": , "invalid_min": , "min_vol": , "min_percent": , "line_colour":  }' http://127.0.0.1:5000/tank/graph/<tank>
    Returns: {'Status': 'Success', 'Message': 'Tank added'}/{'Status': 'Error', 'Message': 'Tank not added'}
    '''
    content = request.get_json(silent=False)
    x = sql.Tanks(content['name'], content['nodeID'], int(content['diam']), int(content['max_payload']), int(content['invalid_min']), int(content['min_vol']), float(content['min_percent']), content['line_colour'] )
    # del instance as no longetr used and won't be updated on mods in code
    del x
    return jsonify(), 200

@app.route("/tank/remove/<tank>", methods=['DELETE',])
# @jwt_required
def delete_tank(tank):
    '''
    curl -X DELETE http://127.0.0.1:5000/tank/remove/<tank>
    Returns: {'Status': 'Success', 'Message': 'Tank removed'}/{'Status': 'Error', 'Message': 'Tank not removed'}
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.delete_tank(tank)), 200

@app.route("/tank/status/<tank>", methods=['GET',])
# @jwt_required
def getATankStatus(tank):
    '''
    curl -X GET -H "Content-Type: application/json" -d '{"type":"water"(or "batt")}' http://127.0.0.1:5000/tank/status/<tank>
    Receives: {'tank_name':<tank>, 'level_status/batt_status':<status>}
    '''
    content = request.get_json(silent=False)
    ret = sql.get_tank(tank, 'tank')
    if content['type'] == 'water':
        res = {'tank_name':ret['name'], 'level_status':ret['level_status']}
    elif content['type'] == 'batt':
        res = {'tank_name':ret['name'], 'batt_status':ret['batt_status']}
    else:
        res = {'status': 'Unknown status type'}
    return jsonify(res), 200

@app.route("/tank/graph", methods=['POST',])
# @jwt_required
def getGraph():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name":"main","type":"water"(or"batt"), "range":"days"(or "hours"), "period":"1"}' http://127.0.0.1:5000/tank/graph/<tank>
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print content
    tank_data = sql.get_tank(content['name'], 'tank')
    res =  plot.plot_tank_filtered(tank_data['name'], tank_data['id'], tank_data['line_colour'], content['period'], content['range'], content['type'])
    # above returns tuple ('z.png', img), need to encode 'img' for return
    return base64.b64encode(res[1].getvalue())

@app.route("/tank/rawgraph", methods=['POST',])
# @jwt_required
def getrawGraph():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name":"main","type":"water"(or"batt"), "range":"days"(or "hours"), "period":"1"}' http://127.0.0.1:5000/tank/graph/<tank>
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print content
    tank_data = sql.get_tank(content['name'], 'tank')
    res =  plot.plot_tank_raw(tank_data['name'], tank_data['id'], tank_data['line_colour'], content['period'], content['range'], content['type'])
    # above returns tuple ('z.png', img), need to encode 'img' for return
    return base64.b64encode(res[1].getvalue())


@app.route("/tank/graphs", methods=['POST',])
# @jwt_required
def getGraphs():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"tanks":[], "type":"water"(or"batt"), "range":"days"(or "hours"), "period":<integer>}' http://127.0.0.1:5000/tank/graphs
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print content
    build_id = []
    build_colour = []
    build_list = []
    for x in content['tanks']:
        tank_data = sql.get_tank(x, 'tank')
        build_id.append(tank_data['id'])
        build_colour.append(tank_data['line_colour'])
        build_list.append(tank_data['name'])
    build_dict = {'line_colour':build_colour, 'name':build_list, 'id':build_id}
    res = plot.plot_tank_list(build_dict, content['period'], content['range'], content['type'])
    return base64.b64encode(res[1].getvalue())


@app.route("/tank/status", methods=['PUT',])
# @jwt_required
def update_status():
    '''
    curl -X PUT -H "Content-Type: application/json" -d '{"tank":<tank>, "type":"tank_status"(or "batt_status"), 'status':<new status>}' http://127.0.0.1:5000/tank/graphs
    Returns:
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.write_tank_col(content['tank'], content['type'], content['status'])), 200

@app.route("/tank", methods=['PUT',])
# @jwt_required
def update_tank():
    '''
    curl -X PUT -H "Content-Type: application/json" -d '{"name": , "col": , "data":}' http://127.0.0.1:5000/tank
    Returns: {'status':'Success', 'message': 'Status updated'}/{'status':'Error', 'message':'Status not updated'}
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.write_tank_col(content['name'], content['col'], content['data'])), 200

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
