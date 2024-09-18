from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

class Order:
    def __init__(self, order_id, user_name, status, description, products):
        self.order_id = order_id
        self.user_name = user_name
        self.status = status
        self.description = description
        self.products = products


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

def get_connection():
    connection = psycopg2.connect(host='localhost', port=5432, database='OrdersApplication',
                                  user='administrator', password='root')

    cursor = connection.cursor()

    return connection, cursor


@app.route("/order/all")
def get_order():
    connection, cursor = get_connection()

    cursor.execute("""SELECT Order_.orderid, Order_.user_name, status, description, product.productId, product_name, price
                FROM ORDER_ JOIN productinorder
	            ON productinorder.orderid = ORDER_.orderid
	            JOIN product 
	            ON product.productid = productinorder.productid""")

    orders_data = cursor.fetchall()

    orders = []
    for row in orders_data:
        if orders.__len__() == 0 or orders[orders.__len__()-1].order_id != row[0]:
            orders.append(Order(row[0], row[1], row[2], row[3], [Product(row[4], row[5], row[6])]))
        else:
            orders[orders.__len__() - 1].products.append(Product(row[4], row[5], row[6]))

    order_dict = []
    for order in orders:
        order.products = [it.__dict__ for it in order.products]
        order_dict.append(order.__dict__)


    return order_dict

if __name__ == '__main__':
    app.run('0.0.0.0')


