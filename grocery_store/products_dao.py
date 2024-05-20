# products_dao.py

from sql_connection import get_sql_connection

def get_all_products(connection, order_by='product_id', order_dir='ASC'):
    cursor = connection.cursor()
    query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name "
             "FROM products INNER JOIN uom ON products.uom_id = uom.uom_id "
             "ORDER BY {} {}".format(order_by, order_dir))
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    cursor.close()
    return response


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit)"
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()

    # Retrieve the last inserted ID using the SELECT LAST_INSERT_ID() statement
    cursor.execute("SELECT LAST_INSERT_ID()")
    last_inserted_id = cursor.fetchone()[0]

    cursor.close()

    return last_inserted_id


def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products WHERE product_id = %s")
    cursor.execute(query, (product_id,))
    connection.commit()
    cursor.close()

