# Mostly obtained from:
# https://github.com/vimalloc/flask-jwt-extended
# also check out: https://gist.github.com/jslvtr/139cf76db7132b53f2b20c5b6a9fa7ad
import sql
import creds
# import pprint
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, \
    create_access_token, jwt_refresh_token_required, \
    create_refresh_token, get_jwt_identity

from init import app, jwt

# app.secret_key = 'ksajdkhsadulaulkj1092830983no1y24'  # Change this!
app.secret_key = creds.flask_secret
app.config['JWT_HEADER_TYPE'] = 'Bearer'

@app.route('/auth/login', methods=['POST'])
def auth():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"username":"mw", "password": "pass"}' http://127.0.0.1:5000/auth/login
    '''
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # print username
    # print password
    content = sql.auth_user(username, password)
    if content['status'] == 'passed':
        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        ret = {
            'access_token': create_access_token(identity=username),
            'refresh_token': create_refresh_token(identity=username), 'data':{
            'role': content['role']}
        }
        # print ret
        return jsonify(ret), 200
    else:
        return jsonify({"Status": "Error", "Message": "Bad username or password"}), 401

# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.

# websanova defalts to: refreshData: {url: 'auth/refresh', method: 'GET', enabled: true, interval: 30}
@app.route('/auth/refresh', methods=['POST', 'GET'])
# refresh token not supported out of the box with websanova so using jwt to refresh
# @jwt_refresh_token_required
@jwt_required
def refresh():
    # str = pprint.pformat(request.environ, depth=5)
    # print str

    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    print ret
    return jsonify(ret), 200

@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 401,
        'sub_status': 101,
        'msg': 'The token has expired'
    }), 401
