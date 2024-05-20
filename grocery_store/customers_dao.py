def add_new_customer(connection, customer):
    cursor = connection.cursor()
    query = ("INSERT INTO customers "
             "(name, email, phone) "
             "VALUES (%s, %s, %s)")
    data = (customer['customer_name'], customer['customer_email'], customer['customer_phone'])
    cursor.execute(query, data)
    connection.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    return customer_id
