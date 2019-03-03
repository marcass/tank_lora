import os
import pty
import sys
import creds
import sql
import numpy as np
import telegram
import plot
from collections import deque
from numpy import median
# import tank_views

buffer_by_name_dict = {}
# setup que circular buffer class
class Buffer:
    def __init__(self, name):
        global buffer_by_name_dict
        self.name = name
        self.water_buff = deque([],3)
        self.batt_buff = deque([],3)
        buffer_by_name_dict[self.name] = self
    def filtered_water(self, val):
        self.water_buff.append(val)
        return int(median(self.water_buff))
    def filtered_batt(self, val):
        self.batt_buff.append(val)
        return float(median(self.batt_buff))

#global variables
build_list = []
dur = None
sql_span = None
vers = None

def sort_data(data):
    global vers
    # {'dist':str, 'site': str, 'volt': str, 'tank': str}
    try:
        in_node = data['tank']
        print('in node = '+str(in_node))
        tank_data = sql.get_tank(in_node, 'id')
        # print tank_data
        in_tank = tank_data['name']
        if len(tank_data)>0:
            print('found tank is '+in_tank)
        else:
            print('tank not found')
            return
        if in_tank not in buffer_by_name_dict:
            obj = in_tank
            obj = Buffer(in_tank)
        buff = buffer_by_name_dict[in_tank]
        try:
            dist = int(data['dist'])
            dist = buff.filtered_water(dist)
        except:
            dist = None
        try:
            batt = float(data['volt'])
            batt = buff.filtered_batt(batt)
        except:
            batt = None
        try:
            if (dist < int(tank_data['min_dist'])) or (dist > int(tank_data['max_dist'])):
                print('Payload out of range')
                level = None
            else:
                print('payload in range')
                dist = dist - int(tank_data['min_dist'])
                level = float(tank_data['max_dist'] - dist)/float(tank_data['max_dist']) * 100.0
                post_data({'tags': {'type':'water_level', 'sensorID':in_tank, 'site': 'rob_tanks'}, 'value': level, 'measurement': 'tanks'})
                if level < tank_data['min_percent']:
                    print(tank_data['name']+' under thresh')
                    if tank_data['level_status'] != 'bad':
                        vers = 'water'
                        graph = plot.plot_tank_filtered(tank_data['name'], tank_data['id'], tank_data['line_colour'], '1', 'days', 'water')
                        # test send_graph
                        # telegram.send_graph(creds.marcus_ID, graph)
                        # telegram.bot.sendMessage(creds.marcus_ID, tank_data['name'] +' tank is low', reply_markup=telegram.a.format_keys(tank_data))
                        # pruduction send
                        telegram.send_graph(creds.group_ID, graph)
                        telegram.bot.sendMessage(creds.group_ID, tank_data['name'] +' tank is low', reply_markup=telegram.a.format_keys(tank_data))
                        sql.write_tank_col(tank_data['name'], 'tank_status', 'bad')
                    elif tank_data['level_status'] == 'bad':
                        print('ignoring low level as status flag is bad')
                    else:
                        print('status flag error')
                else:
                    print('level fine, doing nothing')
        except:
            print('exception for some reason')
            level = None
        try:
            if (batt == 0) or (batt > 5.0):
                batt = None
            if batt < 3.2:
                if tank_data['batt_status'] != 'low':
                    # vers = 'batt'
                    # plot.plot_tank(rec_tank, '1',creds.marcus_ID, 'days')
                    # telegram.send_graph()
                    sql.write_tank_col(tank_data['name'], 'batt_status', 'low')
                elif tank_data['batt_status'] == 'low':
                    print('ignoring low battery as status flag is '+tank_data['batt_status'])
                else:
                    print('status flag error')
        except:
            batt = None
        post_data({'tags': {'type':'batt_level', 'sensorID':in_tank, 'site': 'rob_tanks'}, 'value': batt, 'measurement': 'tanks'})
        #add to db
        # print 'writing value voltage ' +str(batt) +' and volume ' +str(level) +' to db for ' +sql.tanks_by_nodeID[in_node].name
        sql.add_measurement(in_node,level,batt)
    except:
        print('malformed string')

#start the message bot
# telegram.MessageLoop(telegram.bot, {'chat': telegram.on_chat_message, 'callback_query': telegram.on_callback_query}).run_as_thread()
# print('Listening ...')
