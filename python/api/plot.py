import matplotlib
matplotlib.use('Agg')
import numpy as np
import sql
import matplotlib.pyplot as plt
import matplotlib.dates as md

# From sql.py
# def plot_tank(tank, period, vers, target_id, q_range):
    format_date = md.DateFormatter('%H:%M\n%d-%m')
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    if vers == 'water':
        data = 'water_volume'
        label = 'Volume (l)'
    if vers == 'batt':
        data = 'voltage'
        label = 'Battery Voltage'
    if type(tank) is list:
        title_name = ''
        for i in tank:
            d = query_via_tankid(i.nodeID, period, q_range)
            ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
            title_name += ' '+i.name
            ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
        title_name += ' plot'
    else:
        d = sql.query_via_tankid(tank.nodeID, period, q_range)
        if vers == 'bi_plot':
            title_name = 'Water Level and Voltage for '+tank.name+' Tank'
            ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)',  marker='o', markersize='5')
            ax.set_xlabel('Time')
            # Make the y-axis label, ticks and tick labels match the line color.
            ax.set_ylabel('Water Volume', color='b')
            ax.tick_params('y', colors='b')
            ax2 = ax.twinx()
            ax2.plot_date(d['timestamp'],d['voltage'], 'r', label='Voltage (V)', marker='p', markersize='5')
            ax2.set_ylabel('Voltage', color='r')
            ax2.tick_params('y', colors='r')
        else:
            title_name = tank.name+' plot'
            ax.plot_date(d['timestamp'],d[data], tank.line_colour, label=tank.name, marker='o', markersize='5')
            ax.set(xlabel='Datetime', ylabel=label, title=tank.name+' '+label)
            plt.axhspan(tank.min_vol, tank.calced_vol, facecolor='#2ca02c', alpha=0.3)
    ax.get_xaxis().set_major_formatter(format_date)
    #times = ax.get_xticklabels()
    #plt.setp(times, rotation=30)
    plt.legend()
    ax.grid()
    plt.tight_layout()
    fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    plt.close()
    #send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'), title_name)
    send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'))

#From monitor.py
# Need to do something like: https://stackoverflow.com/questions/41459657/how-to-create-dynamic-plots-to-display-on-flask
def plot_tank(key_tank, period, target_id, q_range):
    global vers
    global dur
    print vers
    #print 'vers = '+vers
    format_date = md.DateFormatter('%H:%M\n%d-%m')
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    if vers == 'water':
        data = 'water_volume'
        label = 'Volume (%)'
    if vers == 'batt':
        data = 'voltage'
        label = 'Battery Voltage'
    if type(key_tank) is list:
        title_name = ''
        print 'building a list of tanks'
        for x in key_tank:
            print x.name +' tank in list'
        for i in key_tank:
            try:
                d = sql.query_via_tankid(i.nodeID, period, q_range)
                medians = median_data(d[data])
                ax.plot_date(d['timestamp'],medians, i.line_colour, label=i.name)
                title_name += ' '+i.name
                ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
            except:
                message = bot.sendMessage(target_id, "Please resend the plot request, eg '/plot 1' as there has been a problem")
                #pass
            #ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
        title_name += ' plot'
    else:
        d = sql.query_via_tankid(key_tank.nodeID, period, q_range)
        if vers == 'bi_plot':
            print 'bi_plot found'
            title_name = 'Water Level and Voltage for '+key_tank.name+' Tank'
	    ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)')
            #ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)',  marker='o', markersize='5')
            ax.set_xlabel('Time')
            # Make the y-axis label, ticks and tick labels match the line color.
            ax.set_ylabel('Water Volume', color='b')
            ax.tick_params('y', colors='b')
            ax2 = ax.twinx()
            ax2.plot_date(d['timestamp'],d['voltage'], 'r', label='Voltage (V)', marker='p', markersize='5')
            ax2.set_ylabel('Voltage', color='r')
            ax2.tick_params('y', colors='r')
        else:
            print 'kncoking on through'
            title_name = key_tank.name+' plot'
            ax.plot_date(d['timestamp'],d[data], key_tank.line_colour, label=key_tank.name, marker='o', markersize='5')
            ax.set(xlabel='Datetime', ylabel=label, title=key_tank.name+' '+label)
    if vers == 'water':
        plt.axhspan(10, 100, facecolor='#2ca02c', alpha=0.3)
    if vers == 'batt':
        plt.axhspan(3.2, 4.2, facecolor='#2ca02c', alpha=0.3)
    ax.get_xaxis().set_major_formatter(format_date)
    #times = ax.get_xticklabels()
    #plt.setp(times, rotation=30)
    plt.legend()
    ax.grid()
    plt.tight_layout()
    fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    plt.close()
