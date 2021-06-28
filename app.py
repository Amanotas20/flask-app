from flask import Flask, request, render_template, url_for
from database import fetch_all, fetch_id, add_element, delete_element, update_element, update_status
from datetime import datetime
app = Flask(__name__)

#RENDER HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")

#FETCHS ALL CUSTOMERS/ORDERS DATA FROM DATABASE
@app.route("/fetch", methods=['post', 'get'])

def fetch():
    table = request.form.get('table-type')
    ids = request.form.get('search-bar')

    if ids:
        data = fetch_id(table, ids)
    else:       
        data = fetch_all(table)    

    return render_template("index.html", table=table, data=data, ids=ids)

#REDIRECTS TO CREATE NEW CUSTOMER PAGE
@app.route('/create-customer')
def customer_page():
    return render_template('create-customer.html')

#REDIRECTS TO CREATE NEW ORDER PAGE
@app.route('/create-order')
def order_page():
    return render_template('create-order.html')

#CREATES A NEW CUSTOMER
@app.route('/create-customer/<customers>/', methods=['POST'])
def create_customer(customers):

    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('customer_phone')
    country = request.form.get('country')
    email = request.form.get('customer_email')

    customer_info = [name, address, phone, country, email]

    add_element(customers, customer_info)

    return render_template('index.html', table='customers')

#CREATES A NEW GLASS ORDER
@app.route('/create-order/<orders>/', methods=['POST'])
def create_order(orders):
      
    customer_id = request.form.get('customer_id')
    glass_config = request.form.get('glass_config')
    order_status = 'requested'
    
    orders_info = [customer_id, glass_config, order_status]

    add_element(orders, orders_info)

    return render_template('index.html', table='customers')

#DELETES A RECORD FROM THE DATABASE
@app.route('/delete', methods=['POST'])
def delete():
    
    table = request.form.get('table-delete')
    customer_id = request.form.get('id-delete')
    

    delete_element(table, customer_id)

    return render_template('index.html', table='customers')

#REDIRECTS TO UPDATE CUSTOMERS PAGE
@app.route('/update', methods=['get'])
def update():

    return render_template('update-customer.html')

#RETRIEVES CUSTOMER DATA TO UPDATE
@app.route('/update/fetch', methods=['post'])
def fetch_customer_info():

    table = 'customers'
    ids = request.form.get('customer_id_upd')

    data = fetch_id(table, ids)

    return render_template('update-customer.html', data=data, ids=ids)

#UPDATES CUSTOMER DATA
@app.route('/update/record', methods=['POST'])
def update_userInfo():
    ids = request.form.get('customer_id')
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('customer_phone')
    country = request.form.get('country')
    email = request.form.get('customer_email')

    customer_info = [name, address, phone, country, email]

    update_element('customers', customer_info, ids)

    return render_template('index.html')

#UPDATES ORDER STATUS
@app.route('/update-order', methods=['POST'])
def update_order_status():
    ids = request.form.get('id-order')
    order_status = request.form.get('new-status')

    update_status(order_status, ids)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()