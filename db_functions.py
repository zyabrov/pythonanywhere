import sqlite3
import config


#-------------  
#db functions
#-------------  

database = config.db         

def create_table(table):
    con = sqlite3.connect(database) 
    cur = con.cursor()
    cur.execute(f"DROP TABLE {table}")
    print("Table dropped... ")
    cur.execute(f"CREATE TABLE {table}(id,name,tg_id,status,manychat_api,start_date,last_payment_date)")
    con.close()
    return table
  
  
def insert_raw_our_clients(values):
    con = sqlite3.connect(database)
    cur = con.cursor()
    var_string = ', '.join('?' * len(values))
    query_string = 'INSERT INTO our_clients VALUES (%s);' % var_string
    cur.execute(query_string, values)
    #cur.execute("INSERT INTO our_clients VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [values])
    #cur.execute("INSERT INTO our_clients VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10]))
    con.commit()
    con.close()
    return 'Новий запис в базу our_clients'


def update_value(col_to_change, value, col_to_index, value_to_index):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("Update our_clients set ? = ? where ? = ?", (col_to_change, value, col_to_index, value_to_index))
    con.commit()
    con.close()


def update_coupons(admin_id, value):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("Update our_clients set coupons = ? where id = ?", (str(value), int(admin_id)))
    con.commit()
    con.close()


def addvalue_by_adminid(col_to_change, value, admin_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    admin_id = int(admin_id)
    cur.execute("Update our_clients set ? = ? where id = ?", (col_to_change, value, admin_id))
    con.commit()
    con.close()


def set_api(value,admin_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    admin_id = int(admin_id)
    cur.execute("Update our_clients set manychat_api = ? where id = ?", (value, admin_id))
    con.commit()
    con.close()
  

def show_all():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM our_clients")
    data = cur.fetchall()
    con.close()
    print(data)
    return data
    
  
  
def get_raw(col_to_find,value):
    print("value to find:", value)
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM our_clients WHERE ? = ?", (col_to_find, value))
    #cur.execute("SELECT * FROM ? WHERE ? = ?", (str(table), str(col_to_find), value,))
    data = cur.fetchone()
    con.close()
    return data


def get_admin(parametr_name, value):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM our_clients WHERE {parametr_name} = ?", (value,))
    res = cur.fetchone()
    desc = cur.description
    con.close()  
    if res != None:
        names = [description[0] for description in desc] 
        admin_db_data = dict(zip(names, res))
    else: 
        admin_db_data = None
    return admin_db_data


def get_coupon (admin_id, coupon_id):
    coupon_db_data = None
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM ? WHERE id = ?", (f'coupons_{admin_id}', int(coupon_id), ))
    coupon_data = cur.fetchone()
    desc = cur.description
    cur.close()
    con.close() 
    if coupon_data != None:
        coupon_db_data = db_data_to_dict(coupon_data, desc)   
    return coupon_db_data


def update_coupon_in_coupons (admin_id, coupon_id, value):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(f"UPDATE coupons_{admin_id} set status = ?", (value,))
    cur.fetchone()
    cur.close()
    con.close()

def db_data_to_dict(data, desc):
    names = [description[0] for description in desc] 
    data = dict(zip(names, data))
    return data


def delete_db_data(db_table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    sql = f"DELETE FROM {db_table}"
    cur.execute(sql)
    con.commit()
    con.close()
    print(cur.rowcount, "record(s) deleted")
    return f'{cur.rowcount} record(s) deleted'
