from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

#import routes
#import views_auth

#if __name__ == '__main__':
#    app.run(ssl_context='adhoc')
