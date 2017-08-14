import sqlite3


def get_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return conn, c
 
def setup_db():
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS measurements (water REAL, voltage REAL)''')

def add_measurement(vol, volt):
   conn, c = get_db()
   c.execute("INSERT INTO measurements VALUES (?,?)", (vol, volt))
   conn.commit()
   
setup_db()

w = 'NULL'
v = 3.2
add_measurement(w,v)

def dump():
    conn, c = get_db()
    c.execute("SELECT * FROM measurements")
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    volume = [i[0] for i in ret]
    voltage = [i[1] for i in ret]
    ret_dict = {'water_volume':volume, 'voltage':voltage }
    #print ret_dict 
    return ret_dict

print dump()
