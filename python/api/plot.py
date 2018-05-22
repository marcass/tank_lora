import matplotlib
matplotlib.use('Agg')
import numpy as np
import sql
import matplotlib.pyplot as plt
import matplotlib.dates as md
matplotlib.rcParams['timezone'] = tanks.tz
import StringIO
import base64
from telegram import messages

def clean_data(data):
    #std deviation for range is
    a = np.array(data, dtype=np.float32)
    #print data
    #print a.dtype
    b = np.nanstd(a)
    print b
    members = len(data)
    for i in range(members):
        if i < 5:
            c = np.array(data[i:i+10])
        elif i > (members - 5):
            c = np.array(data[i-10:i])
        else:
            c = np.array(data[i-5:i+5], dtype=np.float32)
            #print c
        try:
            d = np.nanmean(c)
            #print d
            if data[i] != None:
                if ((abs(data[i] - d)) > (b/4)):
                    data[i] = None
        except:
            pass
    return data

def median_data(data):
     members = len(data)
     res = data
     for i in range(members):
         start = i
         stop = i+5
         a = data[start:stop]
         try:
             med = np.nanmedian(a)
             res[i] = med
         except:
             pass
     return res

#From monitor.py
# Need to do something like: https://stackoverflow.com/questions/41459657/how-to-create-dynamic-plots-to-display-on-flask
def plot_tank_list(tank_data, period, target_id, q_range):
    # tank_data is a list of dicts consisting of id, name and line colour for all tanks
    #set up img variable
    img = StringIO.StringIO()
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
    title_name = ''
    print 'building a list of tanks'
    for x in tank_data:
        print tank_data[x]['name'] +' tank in list'
    for i in tank_data:
        try:
            d = sql.query_via_tankid(tank_data[i]['id'], period, q_range)
            medians = median_data(d[data])
            ax.plot_date(d['timestamp'],medians, tank_data[i]['line_colour'], label=tank_data[i]['name'])
            title_name += ' '+tank_data[i]['name']
            ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
        except:
            messages(target_id, "Please resend the plot request, eg '/plot 1' as there has been a problem")
    #this is for telegram to send title name
    title_name += ' plot'
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
    # fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    # https://stackoverflow.com/questions/34492197/how-to-render-and-return-plot-to-view-in-flask
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close()
    # plot_url = base64.b64encode(img.getvalue())
    # # In your Html put:
    # # <img src="data:image/png;base64, {{ plot_url }}">
    # return render_template('test.html', plot_url=plot_url)
    return base64.b64encode(img.getvalue())

    # In your Html put:
    # <img src="data:image/png;base64, {{ plot_url }}">

def plot_tank_raw(tank_name, tank_id, line_colour, period, target_id, q_range):
    #set up img variable
    img = StringIO.StringIO()
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
    d = sql.query_via_tankid(tank_id, period, q_range)
    #this is for telegram to send title name
    title_name = tank_name+' plot'
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
    # fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    # https://stackoverflow.com/questions/34492197/how-to-render-and-return-plot-to-view-in-flask
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close()
    # plot_url = base64.b64encode(img.getvalue())
    # # In your Html put:
    # # <img src="data:image/png;base64, {{ plot_url }}">
    # return render_template('test.html', plot_url=plot_url)
    return base64.b64encode(img.getvalue())

def plot_tank_filtered(tank_name, tank_id, line_colour, period, target_id, q_range):
    #set up img variable
    img = StringIO.StringIO()
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
    d = sql.query_via_tankid(tank_id, period, q_range)
    medians = median_data(d[data])
    ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
    #this is for telegram to send title name
    title_name = tank_name+' plot'
    ax.plot_date(d['timestamp'], medians, line_colour, label=tank_name, marker='o', markersize='5')
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
    # fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    # https://stackoverflow.com/questions/34492197/how-to-render-and-return-plot-to-view-in-flask
    fig.savefig(img, format='png')
    img.seek(0) # rewind to beginning of file
    plt.close()
    # plot_url = base64.b64encode(img.getvalue())
    # # In your Html put:
    # # <img src="data:image/png;base64, {{ plot_url }}">
    # return render_template('test.html', plot_url=plot_url)
    return base64.b64encode(img.getvalue())
