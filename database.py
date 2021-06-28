from psycopg2 import connect, extensions, sql
from psycopg2.extras import RealDictCursor, DictCursor
import json
from datetime import datetime


def create_database():
    conn =  connect(
        dbname = "postgres",
        user="postgres",
        password = "23447417a-+-"
    )

    DB_NAME = "tecnoglassapp"

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT

    conn.set_isolation_level( autocommit )

    cursor = conn.cursor()

    # use the sql module to avoid SQL injection attacks
    cursor.execute(sql.SQL(
    "CREATE DATABASE {}"
    ).format(sql.Identifier( DB_NAME )))

    cursor.close()

    conn.close()

def create_table():

    conn = connect(
            dbname = dbname,
            user=user,
            password = password
        )

    cursor = conn.cursor()

    queries = ('''CREATE TABLE IF NOT EXISTS customers (
        customer_id serial PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        address VARCHAR (50) NOT NULL,
        phone_number VARCHAR(50) NOT NULL,
        country VARCHAR (50) NOT NULL,
        email VARCHAR (50) NOT NULL);''',

        '''CREATE TABLE IF NOT EXISTS orders (
        order_id serial PRIMARY KEY,
        customer_id INT NOT NULL,
        FOREIGN KEY (customer_id)
            REFERENCES customers (customer_id),
        glass_config VARCHAR (50) NOT NULL,
        date TIMESTAMP NOT NULL DEFAULT NOW(),
        order_status VARCHAR (255) NOT NULL);''')


    for query in queries:
        cursor.execute(query)

        conn.commit()

        print("table created")

dbname = "tecnoglassapp"
user="postgres"
password = "23447417a-+-"

def add_element(table, data):
    conn = connect(
            dbname = dbname,
            user=user,
            password = password
        )

    cursor = conn.cursor()

    if table == 'customers':

        insert_query = f'''INSERT INTO {table} (name, address, phone_number, country, email) VALUES (%s,%s,%s,%s,%s)'''
        values = (data[0], data[1], data[2], data[3], data[4])
    
    else:
        insert_query = f'''INSERT INTO {table} (customer_id, glass_config, order_status) VALUES (%s,%s,%s)'''
        values = (data[0], data[1], data[2])
    print(data[0], data[1], data[2])
    cursor.execute(insert_query, values)

    conn.commit()

    print("record inserted")

def delete_element(table, ids):
    
    conn = connect(
            dbname = dbname,
            user=user,
            password = password
        )

    cursor = conn.cursor()

    if table == 'customers':
        delete_foreign = f'''DELETE FROM orders WHERE customer_id={ids};'''
        cursor.execute(delete_foreign)
        delete_query = f'''DELETE FROM {table} WHERE customer_id={ids};'''
    
    else:
        delete_query = f'''DELETE FROM {table} WHERE order_id={ids};'''

    cursor.execute(delete_query)

    conn.commit()

    print("record deleted")

def fetch_all(table):
    conn = connect(
        dbname = "tecnoglassapp",
        user="postgres",
        password = "23447417a-+-"
    )

    cursor = conn.cursor(cursor_factory = DictCursor)

    fetchall_query = f'''SELECT * FROM {table}'''

    cursor.execute(fetchall_query)
    
    res = cursor.fetchall()
    data = []
    for row in res:
        data.append(dict(row))
    
    return data

def fetch_id(table, id):
    conn = connect(
        dbname = "tecnoglassapp",
        user="postgres",
        password = "23447417a-+-"
    )

    cursor = conn.cursor(cursor_factory = DictCursor)

    fetchid_query = f'''SELECT * FROM {table} WHERE customer_id={id}'''

    cursor.execute(fetchid_query)
    
    res = cursor.fetchall()
    data = []
    for row in res:
        data.append(dict(row))
    
    return data

def update_element(table, data, id):
    conn = connect(
            dbname = dbname,
            user=user,
            password = password
        )

    cursor = conn.cursor()
    print(data)
    update_query = f'''UPDATE {table}
                    SET name = '{data[0]}',
                        address = '{data[1]}',
                        phone_number = '{data[2]}',
                        country = '{data[3]}',
                        email = '{data[4]}'
                    WHERE customer_id = {id}'''
    
    cursor.execute(update_query)
    conn.commit()

    print('record updated')

def update_status(status, id):
    conn = connect(
            dbname = dbname,
            user=user,
            password = password
        )

    cursor = conn.cursor()

    update_query = f'''UPDATE orders
                    SET order_status = '{status}'
                    WHERE order_id = {id}'''
    
    cursor.execute(update_query)
    conn.commit()

    print('order updated')

