# app.py
# Food Delivery System using streamlit and mysql as the database

import streamlit as st
import mysql.connector as mc
# import pandas as pd
import requests
# from streamlit_lottie import st_lottie

config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': 3306,
    'database': 'ofds'
}


def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    else:
        return r.json()


def create_connection():
    db = mc.connect(**config)
    return db


def create_database(db):
    """Create the 'userdb' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ofds")
    cursor.close()


def create_user_table(db):
    cursor = db.cursor()
    create_user_table_query = '''
    CREATE TABLE IF NOT EXISTS user ( 
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        UNIQUE (email)
    );
    '''
    cursor.execute(create_user_table_query)
    db.commit()
    st.write('User table created successfully')


def create_restaurant_table(db):

    cursor = db.cursor()

    create_restaurant_table_query = """
    CREATE TABLE IF NOT EXISTS restaurant (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
    );
    """

    cursor.execute(create_restaurant_table_query)
    db.commit()
    st.write("Restaurant table created successfully")


def create_order_table(db):

    cursor = db.cursor()
    create_order_table_query = """
    CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    order_total DECIMAL(10,2) NOT NULL,
    delivery_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
    );
    """
    cursor.execute(create_order_table_query)
    db.commit()
    st.write("Order table created successfully")


def create_orderitems_table(db):
    cursor = db.cursor()
    create_orderitems_table_query = """
    Create table IF NOT EXISTS orderitems ( 
    order_id int not null, 
    item_name varchar(30),
    quantity int,
    foreign key (order_id) references orders(order_id)
    );
    """
    cursor.execute(create_orderitems_table_query)
    db.commit()
    st.write("Order item table created successfully")


def create_driver_table(db):
    cursor = db.cursor()
    create_driver_table_query = """
    CREATE TABLE IF NOT EXISTS drivers (
    driver_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
    );
    """

    cursor.execute(create_driver_table_query)
    db.commit()
    st.write("Driver table created successfully")


def create_payment_table(db):
    cursor = db.cursor()
    create_payment_table_query = """
    CREATE TABLE IF NOT EXISTS payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
    """

    cursor.execute(create_payment_table_query)
    db.commit()
    st.write("Payment table created successfully")


def create_rating_table(db):
    cursor = db.cursor()
    create_rating_table_query = """ 
    CREATE TABLE IF NOT EXISTS rating (
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
    );
    """

    cursor.execute(create_rating_table_query)
    db.commit()
    st.write("rating table created successfully")


def create_address_table(db):
    cursor = db.cursor()

    create_address_table_query = """ 
    CREATE TABLE IF NOT EXISTS address (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    state VARCHAR(255) NOT NULL, 
    city  VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    pincode INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
    );
    """

    cursor.execute(create_address_table_query)
    db.commit()
    st.write("address table created successfully")


def create_menu_table(db):
    cursor = db.cursor()

    create_menu_table_query = """ 
    CREATE TABLE IF NOT EXISTS menu (
    menu_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
    );
    """

    cursor.execute(create_menu_table_query)
    db.commit()
    st.write("menu table created successfully")


db = create_connection()

create_user_table(db)
create_restaurant_table(db)
create_order_table(db)
create_orderitems_table(db)
create_driver_table(db)
create_payment_table(db)
create_rating_table(db)
create_address_table(db)
create_menu_table(db)
