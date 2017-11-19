import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.dates as md
import numpy as np
import sqlite3
import datetime
import pytz

tank_list = []
period = 20
q_range = "days"
# https://bugra.github.io/work/notes/2014-03-31/outlier-detection-in-time-series-signals-fft-median-filtering/

class Tanks:
    def __init__(self, name, nodeID, line_colour):
        self.name = name
        self.nodeID = nodeID 
        self.line_colour = line_colour
        tank_list.append(self)
        
t = Tanks('top',   '1', 'b')
n = Tanks('noels', '2', 'g')
s = Tanks('sals',  '3','r')
m = Tanks('main',  '4','m')
b = Tanks('bay',   '5', 'k')
r = Tanks('relay', '6','c')

tanks_db = "./tank_database.db"
tz = 'Pacific/Auckland'


def get_db():
    conn = sqlite3.connect(tanks_db)
    c = conn.cursor()
    return conn, c


def setup_db():
    # Create table
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                    (timestamp TIMESTAMP, tank_id INTEGER, water_volume REAL, voltage REAL)''')
    conn.commit() # Save (commit) the changes

    
def add_measurement(tank_id,water_volume,voltage):
    # Insert a row of data
    conn, c = get_db()
    c.execute("INSERT INTO measurements VALUES (?,?,?,?)", (datetime.datetime.utcnow(),tank_id,water_volume,voltage) )
    conn.commit() # Save (commit) the changes

def localtime_from_response(resp):
    ts = datetime.datetime.strptime(resp, "%Y-%m-%d %H:%M:%S.%f")
    ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone(tz))
    
def query_via_tankid(tank_id, days_str, q_range):
    time_range = int(days_str)
    plot_range = days_str+' '+q_range
    print 'plot range = '+plot_range
    conn, c = get_db()
    #if days is not None:
    #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i days') AND datetime('now','localtime')" % (days), (tank_id,))
    c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i %s') AND datetime('now','localtime')" % (time_range, q_range), (tank_id,))
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    timestamp = [localtime_from_response(i[0]) for i in ret]
    volume = [i[2] for i in ret]
    voltage = [i[3] for i in ret]
    ret_dict = {'timestamp':timestamp, 'tank_id':tank_id, 'water_volume':volume, 'voltage':voltage }
    #print ret_dict 
    return ret_dict

def detect_outlier_position_by_fft(signal, threshold_freq=.1, frequency_amplitude=.01):
    fft_of_signal = np.fft.fft(signal)
    outlier = np.max(signal) if abs(np.max(signal)) > abs(np.min(signal)) else np.min(signal)
    if np.any(np.abs(fft_of_signal[threshold_freq:]) > frequency_amplitude):
        index_of_outlier = np.where(signal == outlier)
        return None
    else:
        return signal

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
            c = np.array(data[i:i-10])
        else:
            c = np.array(data[i-5:i+5], dtype=np.float32)
            #print c
        try:
            d = np.nanmean(c)
            #print d
            if data[i] == None:
                print 'None found, doing nothing'
            else:
                if ((abs(data[i] - d)) > (b/4)):
                    data[i] = None
                    print 'DUMPED'
                else:
                    print 'data unchanged'
        except:
            pass
    return data
#outlier_positions = list(set(outlier_positions))

#def detect_outlier_position_by_fft(signal, threshold_freq=.1, frequency_amplitude=.01):
    #fft_of_signal = np.fft.fft(signal)
    #outlier = np.max(signal) if abs(np.max(signal)) > abs(np.min(signal)) else np.min(signal)
    #if np.any(np.abs(fft_of_signal[threshold_freq:]) > frequency_amplitude):
        #index_of_outlier = np.where(signal == outlier)
        #return index_of_outlier[0]
    #else:
        #return None

#outlier_positions = []
#for ii in range(10, y_with_outlier.size, 5):
    #outlier_position = detect_outlier_position_by_fft(y_with_outlier[ii-5:ii+5])
    #if outlier_position is not None:
        #outlier_positions.append(ii + outlier_position[0] - 5)
#outlier_positions = list(set(outlier_positions))

#plt.figure(figsize=(12, 6));
#plt.scatter(range(y_with_outlier.size), y_with_outlier, c=COLOR_PALETTE[0], label='Original Signal');
#plt.scatter(outlier_positions, y_with_outlier[np.asanyarray(outlier_positions)], c=COLOR_PALETTE[-1], label='Outliers');
#plt.legend();

def plot_tank(key_tank, period, q_range):
    #print 'vers = '+vers
    format_date = md.DateFormatter('%H:%M\n%d-%m')
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    #if vers == 'water':
    data = 'water_volume'
    label = 'Volume (%)'
    #if vers == 'batt':
        #data = 'voltage'
        #label = 'Battery Voltage'
    #if type(key_tank) is list:
    title_name = ''
    print 'building a list of tanks'
    for x in key_tank:
        print x.name +' tank in list'
    for i in key_tank:
        d = query_via_tankid(i.nodeID, period, q_range)
        cleaned_data = clean_data(d[data])
        #ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
        ax.plot_date(d['timestamp'],cleaned_data, i.line_colour, label=i.name, marker='o', markersize='5')
        title_name += ' '+i.name
        ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
    title_name += ' plot'
    #else:
        #d = sql.query_via_tankid(key_tank.nodeID, period, q_range)
        #if vers == 'bi_plot':
            #print 'bi_plot found'
            #title_name = 'Water Level and Voltage for '+key_tank.name+' Tank'
            #ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)',  marker='o', markersize='5')
            #ax.set_xlabel('Time')
            ## Make the y-axis label, ticks and tick labels match the line color.
            #ax.set_ylabel('Water Volume', color='b')
            #ax.tick_params('y', colors='b')
            #ax2 = ax.twinx()
            #ax2.plot_date(d['timestamp'],d['voltage'], 'r', label='Voltage (V)', marker='p', markersize='5')
            #ax2.set_ylabel('Voltage', color='r')
            #ax2.tick_params('y', colors='r')
        #else:
            #print 'kncoking on through'
            #title_name = key_tank.name+' plot'
            #ax.plot_date(d['timestamp'],d[data], key_tank.line_colour, label=key_tank.name, marker='o', markersize='5')
            #ax.set(xlabel='Datetime', ylabel=label, title=key_tank.name+' '+label)
    #if vers == 'water':
        #plt.axhspan(10, 100, facecolor='#2ca02c', alpha=0.3)
    #if vers == 'batt':
        #plt.axhspan(3.2, 4.2, facecolor='#2ca02c', alpha=0.3)
    ax.get_xaxis().set_major_formatter(format_date)
    #times = ax.get_xticklabels()
    #plt.setp(times, rotation=30)       
    plt.legend()
    ax.grid()
    plt.tight_layout()
    plt.show()
    plt.close()
    
    count = 0
    #handle exceptions for absent port (and keep retrying for a while)
    while (port_check(s_port) is None) and (count < 100):
        count = count + 1
        print s_port+' not found '+str(count)+' times'
        time.sleep(10)        
        if count == 100:
            print 'Exited because serial port not found'
            sys.exit()
    while True:
        rcv = readlineCR(port)

#setup database
setup_db()

plot_tank(tank_list, "20", 'days')

