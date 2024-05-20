from flask import Flask, render_template, request, jsonify
from sql_connection import get_sql_connection
import json
import products_dao
import orders_dao
import uom_dao

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    products = products_dao.get_all_products(connection, order_by='product_id', order_dir='ASC')
    return render_template('products.html', products=products)


@app.route('/orders')
def orders():
    orders = orders_dao.get_all_orders(connection)
    return render_template('orders.html', orders=orders)

@app.route('/add_product', methods=['GET'])
def add_product_form():
    uoms = uom_dao.get_uoms(connection)
    return render_template('add_product.html', uoms=uoms)

@app.route('/add_order', methods=['GET'])
def add_order_form():
    products = products_dao.get_all_products(connection)
    return render_template('add_order.html', products=products)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    product = {
        'product_name': request.form['product_name'],
        'uom_id': request.form['uom_id'],
        'price_per_unit': request.form['price_per_unit']
    }
    product_id = products_dao.insert_new_product(connection, product)
    products = products_dao.get_all_products(connection)
    success_message = f"Product '{product['product_name']}' added successfully!"
    return render_template('products.html', products=products, success_message=success_message)

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    customer_name = request.form['customer_name']
    order_details = []
    grand_total = 0

    product_ids = request.form.getlist('product_id[]')
    quantities = request.form.getlist('quantity[]')

    for product_id, quantity in zip(product_ids, quantities):
        product = next((p for p in products_dao.get_all_products(connection) if p['product_id'] == int(product_id)), None)
        if product:
            total_price = float(product['price_per_unit']) * int(quantity)
            grand_total += total_price
            order_details.append({
                'product_id': product_id,
                'quantity': quantity,
                'total_price': total_price
            })

    order = {
        'customer_name': customer_name,
        'grand_total': grand_total,
        'order_details': order_details
    }
    order_id = orders_dao.insert_order(connection, order)
    orders = orders_dao.get_all_orders(connection)
    success_message = "Order added successfully!"
    return render_template('orders.html', orders=orders, success_message=success_message)

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    product_id = request.form['product_id']
    products_dao.delete_product(connection, product_id)
    success_message = f"Product with ID {product_id} deleted successfully!"
    products = products_dao.get_all_products(connection, order_by='product_id', order_dir='ASC')
    return render_template('products.html', products=products, success_message=success_message)


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)
