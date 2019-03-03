import sys
import re
import sql
import plot
import monitor
import telegram
import io
import base64
from flask import Flask, request, jsonify
import json
from init import app, jwt


@app.route("/")
def hello():
    '''
    curl -X GET http://127.0.0.1:5000/
    '''
    return "Hello World!"

@app.route("/tank/<name>", methods=['GET',])
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
def get_tanks_list():
    '''
    curl -X GET http://127.0.0.1:5000/tankslist
    Receives: nothing
    Returns list of dicts of all tanks data [{'name':'tank1', 'id':'1', diam":, "max":, "min":, "min_vol":, "min_percent":, "line_colour":, "status":}, {}, {}, ]
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.get_tank_list()), 200

@app.route("/tank/data", methods=['POST',])
def add_data_point():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name": , "nodeID": , "diam": , "max_payload": , "invalid_min": , "min_vol": , "min_percent": , "line_colour":  }' http://127.0.0.1:5000/tank/graph/<tank>
    Returns: {'Status': 'Success', 'Message': 'Tank added'}/{'Status': 'Error', 'Message': 'Tank not added'}
    '''
    post_data = request.get_data()
    try:
        data = removeNonAscii(post_data)
        payload = json.loads(data)
        if 'PY' in payload['value']:
            #print 'valid string'
            info = post_data.split(";")
            tank = info[1]
            dist = info[2]
            volt = info[3]
            content = {'site': payload['site'], 'tank': tank, 'dist': dist, 'volt' : volt}
            monitor.sort_data(content)
    except:
        content = {'msg': 'excepton'}
    return jsonify(content), 200


    content = request.get_json(silent=False)
    x = sql.Tanks(content['name'], content['nodeID'], int(content['diam']), int(content['max_payload']), int(content['invalid_min']), int(content['min_vol']), float(content['min_percent']), content['line_colour'] )
    # del instance as no longetr used and won't be updated on mods in code
    del x
    ret = {'Status': 'Success', 'Message': 'Well done'}
    return jsonify(ret), 200

@app.route("/tank/add", methods=['POST',])
def add_tank():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name": , "nodeID": , "diam": , "max_payload": , "invalid_min": , "min_vol": , "min_percent": , "line_colour":  }' http://127.0.0.1:5000/tank/graph/<tank>
    Returns: {'Status': 'Success', 'Message': 'Tank added'}/{'Status': 'Error', 'Message': 'Tank not added'}
    '''
    content = request.get_json(silent=False)
    x = sql.Tanks(content['name'], content['nodeID'], int(content['diam']), int(content['max_payload']), int(content['invalid_min']), int(content['min_vol']), float(content['min_percent']), content['line_colour'] )
    # del instance as no longetr used and won't be updated on mods in code
    del x
    ret = {'Status': 'Success', 'Message': 'Well done'}
    return jsonify(ret), 200

@app.route("/tank/remove/<tank>", methods=['DELETE',])
def delete_tank(tank):
    '''
    curl -X DELETE http://127.0.0.1:5000/tank/remove/<tank>
    Returns: {'Status': 'Success', 'Message': 'Tank removed'}/{'Status': 'Error', 'Message': 'Tank not removed'}
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.delete_tank(tank)), 200

@app.route("/tank/status/<tank>", methods=['GET',])
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
def getGraph():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name":"main","type":"water"(or"batt"), "range":"days"(or "hours"), "period":"1"}' http://127.0.0.1:5000/tank/graph/<tank>
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print(content)
    tank_data = sql.get_tank(content['name'], 'tank')
    res =  plot.plot_tank_filtered(tank_data['name'], tank_data['id'], tank_data['line_colour'], content['period'], content['range'], content['type'])
    # above returns tuple ('z.png', img), need to encode 'img' for return
    return base64.b64encode(res[1].getvalue())

@app.route("/tank/rawgraph", methods=['POST',])
def getrawGraph():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"name":"main","type":"water"(or"batt"), "range":"days"(or "hours"), "period":"1"}' http://127.0.0.1:5000/tank/graph/<tank>
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print(content)
    tank_data = sql.get_tank(content['name'], 'tank')
    res =  plot.plot_tank_raw(tank_data['name'], tank_data['id'], tank_data['line_colour'], content['period'], content['range'], content['type'])
    # above returns tuple ('z.png', img), need to encode 'img' for return
    return base64.b64encode(res[1].getvalue())


@app.route("/tank/graphs", methods=['POST',])
def getGraphs():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"tanks":[], "type":"water"(or"batt"), "range":"days"(or "hours"), "period":<integer>}' http://127.0.0.1:5000/tank/graphs
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print(content)
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

@app.route("/tank/rawgraphs", methods=['POST',])
def getGraphsRaw():
    '''
    curl -X POST -H "Content-Type: application/json" -d '{"tanks":[], "type":"water"(or"batt"), "range":"days"(or "hours"), "period":<integer>}' http://127.0.0.1:5000/tank/graphs
    Receives: image object
    '''
    content = request.get_json(silent=False)
    print(content)
    build_id = []
    build_colour = []
    build_list = []
    for x in content['tanks']:
        tank_data = sql.get_tank(x, 'tank')
        build_id.append(tank_data['id'])
        build_colour.append(tank_data['line_colour'])
        build_list.append(tank_data['name'])
    build_dict = {'line_colour':build_colour, 'name':build_list, 'id':build_id}
    res = plot.plot_tank_list_raw(build_dict, content['period'], content['range'], content['type'])
    return base64.b64encode(res[1].getvalue())


@app.route("/tank/status", methods=['PUT',])
def update_status():
    '''
    curl -X PUT -H "Content-Type: application/json" -d '{"tank":<tank>, "type":"tank_status"(or "batt_status"), 'status':<new status>}' http://127.0.0.1:5000/tank/graphs
    Returns:
    '''
    content = request.get_json(silent=False)
    return jsonify(sql.write_tank_col(content['tank'], content['type'], content['status'])), 200

@app.route("/tank", methods=['PUT',])
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

#start the message bot
telegram.MessageLoop(telegram.bot, {'chat': telegram.on_chat_message, 'callback_query': telegram.on_callback_query}).run_as_thread()

if __name__ == "__main__":
    app.run()
