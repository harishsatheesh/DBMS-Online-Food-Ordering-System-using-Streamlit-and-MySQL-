# user data
# global variable to store user_id
global logged_in_user_id
logged_in_user_id = None
import mysql.connector
import itertools
import time

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database="ofds"
)

mc = db.cursor()


# def login(email, password):
#     mc.execute(f"SELECT password FROM users WHERE email = '{email}'")
#     detail = mc.fetchall()
#     # for i in detail:
#     try:
#         passw = detail[0][0]
#         if passw == password:
#             return True
#         else:
#             return False
#     except:
#         return False

def login(email, password):
    global logged_in_user_id  # Declare the global variable

    mc.execute(f"SELECT user_id, password FROM users WHERE email = '{email}'")
    user_details = mc.fetchall()

    try:
        user_id, passw = user_details[0]
        if passw == password:
            # Set the global variable with the user_id
            logged_in_user_id = user_id
            return True  # Return authentication result and user_id
        else:
            return False, None
    except IndexError:
        return False, None


# def get_order_info():
#     global logged_in_user_id
#     query = """SELECT o.order_id, r.name AS restaurant_name, o.paymentmethod, o.order_total
#         FROM orders o
#         JOIN restaurant r ON o.restaurant_id = r.restaurant_id
#         WHERE o.user_id ={}""".format(logged_in_user_id)
#     mc.execute(query)
#     db.commit()
#     return True

# def get_order_info():
#     global logged_in_user_id
#     query = """SELECT o.order_id, r.name AS restaurant_name, o.paymentmethod, o.order_total
#                FROM orders o
#                JOIN restaurant r ON o.restaurant_id = r.restaurant_id
#                WHERE o.user_id = {}""".format(logged_in_user_id)

#     mc.execute(query)
#     result = mc.fetchall()  # Fetch the result set
#     return result

def get_order_info():
    global logged_in_user_id
    query = """SELECT o.order_id, r.name AS restaurant_name, o.paymentmethod, o.order_total,
                      (SELECT name FROM users WHERE user_id = o.user_id) AS user_name,
                      (SELECT address FROM users WHERE user_id = o.user_id) AS user_address,
                      (SELECT phone FROM users WHERE user_id = o.user_id) AS user_phone
               FROM orders o
               JOIN restaurant r ON o.restaurant_id = r.restaurant_id
               WHERE o.user_id = {}""".format(logged_in_user_id)

    mc.execute(query)
    result = mc.fetchall()  # Fetch the result set
    return result


def signup(name, email, address, phnumber, sign_password):
    # pz = ''
    mc.execute(
        f"INSERT INTO users (user_id,name,email, password, phone,address) VALUES (DEFAULT, '{name}','{email}', '{sign_password}','{phnumber}','{address}')")
    # mc.execute(f"INSERT INTO USER (USER_ID, USER_NAME, PASSWORD) VALUES ('{id}', '{name}','{password}') ")
    db.commit()
    return True


def get_details(email):
    mc.execute(
        f"SELECT user_id, name, phone, email , address FROM users WHERE email = '{email}'")
    details = mc.fetchall()
    return [details[0][0], details[0][1], details[0][2], details[0][3], details[0][4]]


# def place_order(total_amt, paymentmethod, food_list, qty_list):
#     try:
#         mc.execute(
#             f"INSERT INTO orders( user_id, order_total ,paymentmethod,restaurant_id) VALUES ( '{logged_in_user_id}', '{total_amt}','{paymentmethod}','1')")
#         mc.execute("SELECT LAST_INSERT_ID()")
#         order_idd = mc.fetchone()[0]

#         for (food, qty) in zip(food_list, qty_list):
#             mc.execute(
#                 f"INSERT INTO orderitems ( order_id, item_name, quantity ) VALUES ('{order_idd}', '{food}', '{qty}')")
#         db.commit()
#         return True
#     except:
#         return False


import logging


def place_order(total_amt, paymentmethod, food_list, qty_list):
    try:
        # Print or log information for debugging
        print(f"Attempting to place order for user ID {logged_in_user_id}")
        logging.debug(
            f"Total Amount: {total_amt}, Payment Method: {paymentmethod}")

        mc.execute(
            f"INSERT INTO orders( user_id, order_total ,paymentmethod,restaurant_id) VALUES ( '{logged_in_user_id}', '{total_amt}','{paymentmethod}','1')")
        mc.execute("SELECT LAST_INSERT_ID()")
        order_idd = mc.fetchone()[0]

        # Print or log information for debugging
        print(f"Order ID generated: {order_idd}")
        logging.debug(f"Order ID: {order_idd}")

        for (food, qty) in zip(food_list, qty_list):
            mc.execute(
                f"INSERT INTO orderitems ( order_id, item_name, quantity ) VALUES ('{order_idd}', '{food}', '{qty}')")

        # Print or log information for debugging
        print("Order placed successfully.")
        logging.debug("Order placed successfully.")

        db.commit()
        return True
    except Exception as e:
        # Print or log the exception for debugging
        print(f"Error placing order: {e}")
        logging.error(f"Error placing order: {e}")
        return False


def get_user_data():
    mc.execute("SELECT user_id, email, name, address, phone FROM users")
    details = mc.fetchall()
    detail_dict = {'User Id': [i[0] for i in details],
                   'Email Id': [i[1] for i in details],
                   'Name': [i[2] for i in details],
                   'Address': [i[3] for i in details],
                   'Phone Number': [i[4] for i in details]}
    return detail_dict


def get_order_data():
    mc.execute("SELECT * FROM orders")
    details = mc.fetchall()
    details_dict = {'Order Id': [i[0] for i in details],
                    'User Id': [i[1] for i in details],
                    'Total Amount': [i[2] for i in details]}
    return details_dict


def get_orderitem_data():
    mc.execute("SELECT * FROM orderitems")
    details = mc.fetchall()
    details_dict = {'order_id': [i[0] for i in details],
                    'Food Item': [i[1] for i in details],
                    'QTY': [i[2] for i in details]}
    return details_dict


def update_details(user_id, email, name, address, number):
    mc.execute(
        f"UPDATE users SET email = '{email}', name ='{name}', address ='{address}', phone = '{number}' WHERE user_id ={user_id} ")
    db.commit()
    return True


def update_password(user_id, password):
    mc.execute(
        f"UPDATE users SET password ='{password}' WHERE user_id={user_id} ")
    db.commit()
    return True


def get_orderitem_detail(order_id):
    mc.execute(f"SELECT * FROM orderitems WHERE order_id = '{order_id}'")
    details = mc.fetchall()
    detail_dict = {'order_id': [i[0] for i in details],
                   'Food Item': [i[1] for i in details],
                   'QTY': [i[2] for i in details]}
    return detail_dict


# def delete_user(user_id):
#     mc.execute("SET FOREIGN_KEY_CHECKS=0")
#     mc.execute(
#         f"DELETE users, orders, orderitems FROM users INNER JOIN orders ON users.user_id = orders.user_id INNER JOIN orderitems on orders.order_id = orderitems.order_id  WHERE users.user_id ={user_id}")
#     db.commit()
def delete_user(user_id):
    try:
        # Assuming you have a 'users' table with a 'user_id' column
        mc.execute(f"DELETE FROM users WHERE user_id = {user_id}")
        db.commit()
        print(f"User with user_id {user_id} deleted successfully.")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


login("sample", "1234")

# DELIMITER //

# CREATE FUNCTION CalculateTotalAmount(order_id INT)
# RETURNS DECIMAL(10, 2)
# BEGIN
#     DECLARE total DECIMAL(10, 2);

#     SELECT SUM(order_total) INTO total
#     FROM orders
#     WHERE order_id = order_id;

#     RETURN total;
# END //

# DELIMITER ;
