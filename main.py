from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField  # Added SubmitField to imports
from pprint import pprint  # Import pprint for pretty printing
from collections import defaultdict
from flask import Flask, request, redirect, url_for, flash, render_template
import random
from mysql.connector import pooling
from flask import request
from flask import Flask, render_template, flash, redirect, url_for, jsonify, session, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit

from flask import redirect, url_for, session
from flask_mail import Mail, Message
import os
from flask_wtf import FlaskForm
from wtforms import EmailField
import pymysql
import secrets
from werkzeug.utils import secure_filename
import hashlib
import base64
import requests
from flask import render_template
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from passlib.hash import sha256_crypt
from flask import render_template, request, redirect, flash, url_for
import mysql.connector
import hashlib
import hmac
import base64
from urllib.parse import unquote
import requests
from flask import Flask, render_template, request, redirect, url_for
import uuid
import os
import mysql.connector
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import redirect, url_for, jsonify
import mysql.connector
import datetime
import pickle
import numpy as np
from mysql.connector import Error
from flask import redirect, url_for
import mysql.connector.errors
import datetime
import functools


app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

app.secret_key = '8gBm/:&EnhH.1/q'
# Config MySQL
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'onlinebook'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PORT'] = 4306
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': '4306',
    'database': 'onlinebook',
}

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=32,  # Adjust the pool size as needed
    pool_reset_session=True,
    **db_config  # Include your database configuration here
)

def create_tables():
    with db_pool.get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10, 2),
                category VARCHAR(255)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT,
                quantity INT,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def content_based_filtering(product_id, num_recommendations=2):
    cur = mysql.connection.cursor()

    # Retrieve data for the reference product
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    reference_product = cur.fetchone()
    if not reference_product:
        print('Reference product not found.')
        return None

    # Extract category and other data from the reference product
    data_cat = reference_product['category']
    print('Showing results for Product Id:', product_id)

    # Fetch products with the same category as the reference product
    category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))
    print('Total products matched in the same category:', category_matched)
    cat_products = cur.fetchall()

    # Retrieve attribute levels of the reference product
    cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
    id_level = cur.fetchone()
    if not id_level:
        print('Attribute levels not found for Product Id:', product_id)
        return None

    recommend_id = []
    cate_level = ['fiction', 'nonfiction', 'scifi', 'history']

    for product_f in cat_products:
        cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        f_level = cur.fetchone()
        if f_level and f_level['product_id'] != int(product_id):
            match_score = 0
            for cat_level in cate_level:
                if f_level.get(cat_level) == id_level.get(cat_level):
                    match_score += 1
            if match_score == len(cate_level):
                recommend_id.append(f_level['product_id'])

    print('Total recommendations found:', recommend_id[:num_recommendations])
    if recommend_id:
        placeholders = ','.join(str(n) for n in recommend_id[:num_recommendations])
        query = f'SELECT * FROM products WHERE id IN ({placeholders})'
        cur.execute(query)
        recommend_list = cur.fetchall()
        return recommend_list, recommend_id[:num_recommendations], category_matched, product_id
    else:
        print('No recommendations found.')
        return None


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Proceed with other processing, such as database updates
            return 'File uploaded successfully!'
    return 'No file uploaded or file upload failed.'


# Route to display products
@app.route('/')
def index():
    form = OrderForm(request.form)

    if 'uid' in session:
        uid = str(session['uid'])
    else:
        uid = None

    # Get a connection from the connection pool
    conn = db_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get products for different categories
    categories = ['fiction', 'nonfiction', 'scifi', 'history']
    product_data = {}

    try:
        for category in categories:
            cursor.execute("SELECT * FROM products WHERE category = %s ORDER BY RAND() LIMIT 4", (category,))
            product_data[category] = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error executing query:", err)
    finally:
        # Close cursor and return connection to the pool
        cursor.close()
        conn.close()

    # Calculate noOfItems dynamically based on the items in the cart
    noOfItems = get_no_of_items_in_cart()

    return render_template('home.html', product_data=product_data, form=form, noOfItems=noOfItems)


def get_no_of_items_in_cart(json_data=None):
    try:
        # Check if the session exists
        if 'cart' in session:
            # Check if the payment is complete
            if json_data and 'status' in json_data and json_data['status'] == 'COMPLETE':
                print("Resetting cart to 0")
                session['cart'] = {}
                return 0
            else:
                # Calculate the total number of items in the cart
                no_of_items = sum(session['cart'].values())
                print("Number of items in cart:", no_of_items)
                return no_of_items
        else:
            print("No cart data found in session")
            return 0
    except Exception as e:
        print(f"Error occurred: {e}")
        return 0




class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})


# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                flash(' Welcome to Online Book Store', 'success')
                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)



    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=50)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    address = StringField('', [validators.length(min=3)], render_kw={'autofocus': True, 'placeholder': 'Your Address '})
    mobile = StringField('', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobile'})


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        address = form.address.data
        mobile = form.mobile.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Check if email is already registered
        result = cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if result > 0:
            flash('Email already registered', 'danger')
            cur.close()
            return render_template('register.html', form=form)

        # If email is unique, proceed with registration
        cur.execute("INSERT INTO users(name, email, username, password, address, mobile) VALUES(%s, %s, %s, %s, %s,%s)",
                    (name, email, username, password, address ,mobile))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


class MessageForm(Form):  # Create Message Form
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


import logging

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    try:
        logging.debug("Adding item to cart and mycart...")

        # Ensure 'cart' exists in the session
        if 'cart' not in session:
            session['cart'] = {}

        # Ensure 'mycart' exists in the session
        if 'mycart' not in session:
            session['mycart'] = {}

        # Convert product_id to string
        str_product_id = str(product_id)

        # Add the product to the session's cart
        if str_product_id in session['cart']:
            # Increment the quantity in the session if the product is already in the cart
            session['cart'][str_product_id] += 1
        else:
            # Add the product with quantity 1 to the session if it's not in the cart
            session['cart'][str_product_id] = 1

        # Add the product to the session's mycart
        if str_product_id in session['mycart']:
            # Increment the quantity in the session if the product is already in mycart
            session['mycart'][str_product_id] += 1
        else:
            # Add the product with quantity 1 to the session if it's not in mycart
            session['mycart'][str_product_id] = 1

        logging.debug("Item added to session cart and mycart.")

        # Check if the user is logged in
        if 'logged_in' in session:
            logging.debug("User is logged in.")

            # Add the product to the cart table in the database
            with db_pool.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to fetch rows as dictionaries

                # Fetch product details including discount from the database
                cursor.execute("SELECT pName, price, discount FROM products WHERE id = %s", (product_id,))
                product_info = cursor.fetchone()

                if product_info:
                    name, price, discount = product_info['pName'], float(product_info['price']), product_info['discount']

                    # Fetch the quantity from the session
                    cart_quantity = session['cart'][str_product_id]
                    mycart_quantity = session['mycart'][str_product_id]

                    # Check if the product is already in the database cart
                    cursor.execute("SELECT * FROM cart WHERE uid = %s AND pid = %s", (session.get('uid'), product_id))
                    cart_item = cursor.fetchone()

                    if cart_item:
                        # Update the quantity and discount if the product is already in the database cart
                        cursor.execute("UPDATE cart SET quantity = %s, discount = %s WHERE uid = %s AND pid = %s",
                                       (cart_quantity, discount, session.get('uid'), product_id))
                        logging.debug("Updated quantity and discount in database cart.")
                    else:
                        # Insert a new record with quantity and discount if the product is not in the database cart
                        cursor.execute("INSERT INTO cart (uid, pid, quantity, discount) VALUES (%s, %s, %s, %s)",
                                       (session.get('uid'), product_id, cart_quantity, discount))
                        logging.debug("Inserted item into database cart.")

                    # Check if the product is already in the database mycart
                    cursor.execute("SELECT * FROM mycart WHERE uid = %s AND pid = %s", (session.get('uid'), product_id))
                    mycart_item = cursor.fetchone()

                    if mycart_item:
                        # Update the quantity and discount if the product is already in the database mycart
                        cursor.execute("UPDATE mycart SET quantity = %s, discount = %s WHERE uid = %s AND pid = %s",
                                       (mycart_quantity, discount, session.get('uid'), product_id))
                        logging.debug("Updated quantity and discount in database mycart.")
                    else:
                        # Insert a new record with quantity and discount if the product is not in the database mycart
                        cursor.execute("INSERT INTO mycart (uid, pid, quantity, discount) VALUES (%s, %s, %s, %s)",
                                       (session.get('uid'), product_id, mycart_quantity, discount))
                        logging.debug("Inserted item into database mycart.")

                    conn.commit()
                    flash('Item added to  Shopping cart', 'success')
                    logging.debug("Redirecting to view_cart...")
                    return redirect(url_for('view_cart'))
                else:
                    logging.error("Product not found in database.")
                    flash('Product not found in database', 'danger')
                    return redirect(url_for('index'))  # Redirect to home or product listing page
        else:
            flash('You need to be logged in to perform this action.', 'danger')
            logging.debug("Redirecting to login...")
            return redirect(url_for('login'))
    except Exception as e:
        error_message = f'Error adding item to cart and mycart: {str(e)}'
        logging.error(error_message)
        flash(error_message, 'danger')
        logging.debug("Redirecting to view_cart due to error...")
        return redirect(url_for('view_cart'))


from datetime import datetime, timedelta
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Query the PHPMyAdmin users table to find the user with the given email address
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            reset_token = str(uuid.uuid4())

            # Update the PHPMyAdmin users table to set the reset token and expirationtime
            cur.execute("UPDATE users SET reset_token = %s, reset_token_expiration = %s WHERE email = %s",
                        (reset_token, datetime.utcnow() + timedelta(hours=1), email))
            mysql.connection.commit()

            # Send the password reset email
            msg = MIMEMultipart()
            msg['From'] = 'acaashish08@gmail.com'
            msg['To'] = user['email']
            msg['Subject'] = 'Password Reset Request'
            message = f'Click the link below to reset your password: \n\n http://127.0.0.1:5000//reset-password/{reset_token}\n\n This link will expire in 1 hour.'
            msg.attach(MIMEText(message, 'plain'))

            # Send the email using your email provider's SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('acaashish08@gmail.com', 'tyrx anta pwyf kbfd')
                server.sendmail('acaashish08@gmail.com', user['email'], msg.as_string())
            flash('Check your email please', 'success')
            return redirect(url_for('login'))

        else:
            return 'User not found'

    else:
        return render_template('forgot_password.html')


# Route to display the password reset link sent message

@app.route('/reset-password/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    cur = mysql.connection.cursor()

    if request.method == 'GET':
        # Query the PHPMyAdmin users table to find the user with the given reset token
        cur.execute("SELECT * FROM users WHERE reset_token = %s", (reset_token,))
        user = cur.fetchone()

        if user:
            # Display the password reset form
            return render_template('reset-password.html', reset_token=reset_token)

        else:
            # Display an error message if the reset token is invalid
            return 'Invalid reset token'

    else:
        # Update the user's password in the PHPMyAdmin users table
        new_password = request.form['password']
        password = sha256_crypt.encrypt(str(new_password))
        cur.execute(
            "UPDATE users SET password = %s, reset_token = NULL, reset_token_expiration = NULL WHERE reset_token = %s",
            (password, reset_token))
        mysql.connection.commit()

        # Redirect the user to the login page
        return redirect(url_for('login'))

    # Close the cursor object
    cur.close()


import logging

@app.route('/cart')
def view_cart():
    cart_items = {}
    total_price = 0
    noOfItems = 0

    try:
        if 'cart' in session:
            with db_pool.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                for product_id, quantity in session['cart'].items():
                    cursor.execute('SELECT pName, price, discount FROM products WHERE id = %s', (product_id,))
                    product_info = cursor.fetchone()

                    if product_info and 'price' in product_info:
                        name, price, discount = product_info['pName'], float(product_info['price']), product_info['discount']

                        discounted_price = price - (price * discount / 100)
                        total_price += discounted_price * quantity
                        cart_items[product_id] = {'pName': name, 'price': price, 'quantity': quantity, 'discount': discount}
                        noOfItems += quantity  # Increment noOfItems based on quantity

        return render_template('cart.html', cart_items=cart_items, total_price=total_price, noOfItems=noOfItems)
    except KeyError:
        error_message = "Cart is empty or not found"
        logging.error(error_message)
        return render_template('error.html', error_message=error_message)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        logging.error(error_message)
        return render_template('error.html', error_message=error_message)


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    # Check if 'cart' is in session and is a dictionary
    if 'cart' in session and isinstance(session['cart'], dict):
        print("Current Cart:", session['cart'])

        # Convert product_id to string
        str_product_id = str(product_id)

        # Check if the product is in the cart
        if str_product_id in session['cart']:
            # Decrement the quantity
            session['cart'][str_product_id] -= 1

            # Check if quantity is less than or equal to 0, remove the product from the cart
            if session['cart'][str_product_id] <= 0:
                del session['cart'][str_product_id]

                # Remove the product from the 'cart' table in the database
                with db_pool.get_connection() as conn:
                    cursor = conn.cursor()
                    uid = session.get('uid', None)
                    cursor.execute("DELETE FROM cart WHERE uid = %s AND pid = %s", (uid, product_id))
                    conn.commit()

                flash('Item removed from cart', 'success')
            else:
                # Update the quantity in the 'cart' table for the product
                with db_pool.get_connection() as conn:
                    cursor = conn.cursor()
                    uid = session.get('uid', None)
                    cursor.execute("UPDATE cart SET quantity = %s WHERE uid = %s AND pid = %s",
                                   (session['cart'][str_product_id], uid, product_id))
                    conn.commit()

                flash('Quantity removed', 'success')

        print("Updated Cart:", session['cart'])

    # Redirect to the view_cart route
    return redirect(url_for('view_cart'))


@app.route('/')
def home():
    # Your code to calculate noOfItems
    noOfItems = 10  # Example value

    return render_template('home.html', noOfItems=noOfItems)



SECRET_KEY = "8gBm/:&EnhH.1/q"


def generate_signature(secret_key, payload):
    message = payload.encode()
    signature = hmac.new(secret_key.encode(), message, hashlib.sha256)
    return base64.b64encode(signature.digest()).decode()

import json
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart_items = {}
    total_price = 0

    if 'cart' in session:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            for product_id, quantity in session['cart'].items():
                cursor.execute('SELECT pName, price, discount FROM products WHERE id = %s', (product_id,))
                product_info = cursor.fetchone()
                print("Product Info:", product_info)
                if product_info and 'price' in product_info and 'discount' in product_info:
                    name, price, discount = product_info['pName'], float(product_info['price']), float(product_info['discount'])
                    print("Name:", name, "Price:", price, "Discount:", discount)

                    # Calculate discounted price
                    discounted_price = price - (price * discount / 100)
                    total_price += discounted_price * quantity

                    cart_items[product_id] = {'pName': name, 'price': price, 'quantity': quantity, 'discount': discount}
                else:
                    print(f"Product information not found or incomplete for product ID: {product_id}")

    # Get uid from cart table in the database
    uid = None
    if 'uid' in session:
        uid = session['uid']
    else:
        # Query the database to get the uid based on cart items or any other relevant criteria
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT uid FROM cart WHERE pid = %s', (product_id,))
  # Add your condition to retrieve the uid
            uid_row = cursor.fetchone()
            if uid_row:
                uid = uid_row[0]  # Assuming uid is in the first column of the result

    # Example data for signature generation
    transaction_uuid = str(uuid.uuid4())
    product_code = 'EPAYTEST'

    # Concatenate fields for signature
    signed_field_names = f'total_amount={total_price},transaction_uuid={transaction_uuid},product_code={product_code}'
    print("Signature Data:", signed_field_names)
    print("UID Data:", uid)
    # Generate the signature
    signature = generate_signature(SECRET_KEY, signed_field_names)
    print("Generated Signature:", signature)

    # Example POST request using requests library
    url = 'https://rc-epay.esewa.com.np/api/epay/main/v2/form'
    payload = {
        'amount': total_price,
        'tax_amount': 100,
        'total_amount': total_price,
        'transaction_uuid': transaction_uuid,
        'product_code': product_code,
        'product_service_charge': 0,
        'product_delivery_charge': 0,
        'success_url': 'https://esewa.com.np',
        'failure_url': 'https://google.com',
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
        'signature': signature
    }

    response = requests.post(url, data=payload)
    print(response.text)



    noOfItems = get_no_of_items_in_cart()
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price,
                           noOfItems=noOfItems, transaction_uuid=transaction_uuid,
                           signed_field_names='total_amount,transaction_uuid,product_code', signature=signature ,uid=uid,)




# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'onlinebook'





# Define the decode_base64_to_json function
def decode_base64_to_json(data):
    try:
        # Decode the Base64 encoded data
        decoded_data = base64.b64decode(data).decode('utf-8')
        # Convert the decoded data to JSON format
        json_data = json.loads(decoded_data)
        return json_data
    except Exception as e:
        # Handle decoding or JSON parsing errors
        print("Decoding Error:", e)
        return {'error': str(e)}

@app.route('/success_url', methods=['GET'])
def success_url():
    # Check if the request method is GET
    if request.method == 'GET':
        # Get the encoded data from the query parameter named 'data'
        encoded_data = request.args.get('data')

        # Check if encoded_data is present
        if encoded_data:
            try:
                # Decode the data using the decode_base64_to_json function
                decoded_json = decode_base64_to_json(encoded_data)

                # Check if the 'status' field in the decoded JSON data is 'COMPLETE'
                if decoded_json.get('status', '').upper() == 'COMPLETE':
                    # Update the payment status in the database
                    uid = session.get('uid')

                    # Check if UID is available in the session
                    if uid:
                        try:
                            complete = 'paid'
                            conn = mysql.connection.cursor()
                            # Update payment status to 'complete' for the user's cart
                            conn.execute("UPDATE cart SET payment = %s WHERE uid = %s", (complete, uid))
                            conn.execute("UPDATE mycart SET payment = %s WHERE uid = %s", (complete, uid))
                            mysql.connection.commit()
                        except mysql.connector.Error as e:
                            print(f"Error updating payment status: {e}")
                            return jsonify(error='Error updating payment status'), 500
                    else:
                        return jsonify(error='Missing session UID'), 400

                    # Redirect or render template based on your application flow
                    # Example: return redirect(url_for('success_page'))
                    noOfItems = get_no_of_items_in_cart()
                    return render_template('success_url.html',noOfItems=noOfItems,decoded_json=decoded_json)
                else:
                    return jsonify(message='Data retrieved but status is not complete'), 200
            except Exception as e:
                print(f"Error processing data: {e}")
                return jsonify(error='Error processing data'), 500
        else:
            return jsonify(error='Encoded data not found in query parameters'), 400
    else:
        return 'Method Not Allowed', 405
@app.route('/success_url_khalti', methods=['GET'])
def success_url_khalti():
    # Extract data from URL parameters
    pidx = request.args.get('pidx')
    transaction_id = request.args.get('transaction_id')
    amount = request.args.get('amount')
    total_amount = request.args.get('total_amount')
    mobile = request.args.get('mobile')
    status = request.args.get('status')
    purchase_order_id = request.args.get('purchase_order_id')
    purchase_order_name = request.args.get('purchase_order_name')

    # Log the request data for debugging purposes
    app.logger.info(f"Request data: pidx={pidx}, transaction_id={transaction_id}, amount={amount}, total_amount={total_amount}, mobile={mobile}, status={status}, purchase_order_id={purchase_order_id}, purchase_order_name={purchase_order_name}")

    # Pass data to HTML template
    noOfItems = get_no_of_items_in_cart()
    return render_template('success_url_khalti.html', noOfItems=noOfItems,
                           pidx=pidx, transaction_id=transaction_id,
                           amount=amount, total_amount=total_amount,
                           mobile=mobile, status=status,
                           purchase_order_id=purchase_order_id,
                           purchase_order_name=purchase_order_name)

@app.route('/success_page')
def success_page():
    # Render the success_page.html template
    noOfItems = get_no_of_items_in_cart()
    return render_template('success_url.html',noOfItems=noOfItems)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        flash('Order placed successfully!', 'success')
        # Clear the cart after placing the order
        session.pop('cart', None)
        return redirect(url_for('home'))
    else:
        message = "Welcome to the checkout page!"
        cart_items = get_cart()

        # Calculate total price with proper handling for both dictionary items and integers
        total_price = sum(
            (item['price'] * item['quantity']) if isinstance(item, dict) else item
            for item in cart_items.values()
        )


        return render_template('checkout.html', message=message, cart_items=cart_items, total_price=total_price)


class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Your Full Name'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = StringField('', [validators.length(min=1), validators.DataRequired()],
                           render_kw={'placeholder': 'Your order number'})
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Place your location'})

import json
import traceback

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    # Extract data from the POST request
    url = 'https://a.khalti.com/api/v2/epayment/initiate/'
    return_url = request.form.get('return_url')
    website_url = request.form.get('website_url')
    amount_paisa = request.form.get('amount')
    purchase_order_id = request.form.get('purchase_order_id')

    try:
        # Check if the 'amount' value is a valid number
        amount_number = float(amount_paisa)

        # Convert the 'amount' value to an integer
        amount_money = int(amount_number * 100)

        # Print the extracted values for debugging
        print(f"Return URL: {success_url}")
        print(f"Website URL: {website_url}")
        print(f"Amount: {amount_money}")
        print(f"Purchase Order ID: {purchase_order_id}")

        # Define the payload for Khalti API
        payload = {
            "return_url": return_url,
            "website_url": website_url,
            "amount": amount_money,  # Include the 'amount' in the payload
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": "Ram Bahadur",
                "email": "test@khalti.com",
                "phone": "9800000001"
            }
        }

        # Convert payload to JSON format
        json_payload = json.dumps(payload)

        # Set headers for the API request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key e6dc36e5cc4c49609b00625ebdbbd8f7'
        }

        # Make a POST request to Khalti API with the payload data
        response = requests.post(url, headers=headers, data=json_payload)

        # Print the API response for debugging
        print(response.text)
        new_res = json.loads(response.text)
        print(new_res)

        # Redirect to the payment URL returned by Khalti API
        return redirect(new_res['payment_url'])

    except ValueError as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return "Error: Invalid amount value.", 500

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        traceback.print_exc()  # Print the full traceback
        return "Error: An unknown error occurred.", 500

@app.route('/fiction', methods=['GET', 'POST'])
@is_logged_in
def fiction():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get products
    values = 'fiction'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()

    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args.get('order')  # Use request.args.get to avoid KeyError
        now = datetime.now()
        week = timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        noOfItems = get_no_of_items_in_cart()
        return render_template('fiction.html', fiction=products, form=form, noOfItems=noOfItems)

    if 'view' in request.args:
        product_id = request.args.get('view')  # Use request.args.get to avoid KeyError
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchone()
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)

        if 'uid' in session:
            uid = session['uid']
            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product = cur.fetchone()
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                            (now_time, uid, product_id))
            else:
                cur.execute("INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)", (uid, product_id))
                mysql.connection.commit()
            # Calculate noOfItems dynamically based on the items in the cart
        noOfItems = get_no_of_items_in_cart()
        return render_template('view_product.html', x=x, fiction=product, noOfItems=noOfItems)

    elif 'order' in request.args:
        product_id = request.args.get('order')  # Use request.args.get to avoid KeyError
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchone()
        x = content_based_filtering(product_id)
        noOfItems = get_no_of_items_in_cart()
        return render_template('order_product.html', x=x, fiction=product, form=form, noOfItems=noOfItems)
    noOfItems = get_no_of_items_in_cart()
    return render_template('fiction.html', fiction=products, form=form, products=products, noOfItems=noOfItems)


@app.route('/nonfiction', methods=['GET', 'POST'])
@is_logged_in
def nonfiction():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'nonfiction'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']

        now = datetime.now()
        week = timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        noOfItems = get_no_of_items_in_cart()
        return render_template('nonfiction.html', nonfiction=products, form=form, noOfItems=noOfItems)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cur.fetchone()
        if product is not None:
            cur.close()  # Close the cursor after fetching the product
            noOfItems = get_no_of_items_in_cart()
            return render_template('view_product.html', x=x, fiction=product, noOfItems=noOfItems)
        else:
            cur.close()  # Close the cursor in case of no product found
            # Handle the case when no product is found
            flash('Product not found', 'error')
            return redirect(url_for('nonfiction'))

    elif 'order' in request.args:
        product_id = request.args['order']
        cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cur.fetchone()
        if product is not None:
            cur.close()  # Close the cursor after fetching the product
            x = content_based_filtering(product_id)
            noOfItems = get_no_of_items_in_cart()
            return render_template('order_product.html', x=x, fiction=product, form=form, noOfItems=noOfItems)
        else:
            cur.close()  # Close the cursor in case of no product found
            # Handle the case when no product is found
            flash('Product not found', 'error')
            return redirect(url_for('nonfiction'))
    noOfItems = get_no_of_items_in_cart()
    return render_template('nonfiction.html', nonfiction=products, form=form, noOfItems=noOfItems)


@app.route('/scifi', methods=['GET', 'POST'])
@is_logged_in
def scifi():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    if 'uid' in session:
        uid = str(session['uid'])
    else:
        uid = None
    # Get message
    values = 'scifi'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.now()
        week = timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        noOfItems = get_no_of_items_in_cart()
        return render_template('scifi.html', scifi=products, form=form, noOfItems=noOfItems)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        product = curso.fetchone()  # Use fetchone() as you are retrieving a single product
        noOfItems = get_no_of_items_in_cart()
        return render_template('view_product.html', x=x, fiction=product, noOfItems=noOfItems)

    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchone()  # Use fetchone() as you are retrieving a single product
        x = content_based_filtering(product_id)
        noOfItems = get_no_of_items_in_cart()
        return render_template('order_product.html', x=x, fiction=product, form=form, noOfItems=noOfItems)
    noOfItems = get_no_of_items_in_cart()
    return render_template('scifi.html', scifi=products, form=form, noOfItems=noOfItems)


@app.route('/history', methods=['GET', 'POST'])
@is_logged_in
def history():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    if 'uid' in session:
        uid = str(session['uid'])
    else:
        uid = None
    values = 'history'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.now()
        week = timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        curs.close()

        flash('Order successful', 'success')
        noOfItems = get_no_of_items_in_cart()
        return render_template('history.html', history=products, form=form, noOfItems=noOfItems)

    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        product = curso.fetchone()  # Use fetchone() as you are retrieving a single product
        noOfItems = get_no_of_items_in_cart()
        return render_template('view_product.html', x=x, fiction=product, noOfItems=noOfItems)

    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchone()  # Use fetchone() as you are retrieving a single product
        x = content_based_filtering(product_id)
        noOfItems = get_no_of_items_in_cart()
        return render_template('order_product.html', x=x, fiction=product, form=form, noOfItems=noOfItems)
    noOfItems = get_no_of_items_in_cart()
    return render_template('history.html', history=products, form=form, noOfItems=noOfItems)


# Subscription form route
@app.route('/subscribe', methods=['POST'])
def subscribe(subscribed_emails=None):
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email is not already subscribed
        if email not in subscribed_emails:
            # Add the email to the list (You might want to use a database to store subscriptions)
            subscribed_emails.append(email)

            # Print the subscribed email to the console (for demonstration purposes)
            print(f"New subscription: {email}")

            # You might want to redirect to a thank you page or display a success message.
            # For now, let's redirect back to the home page.
            return redirect('/')
        else:
            # Handle case where email is already subscribed
            # You might want to show an error message to the user
            return render_template('error.html', message='Email already subscribed')


@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # GEt user form
        username = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['firstName']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['admin_logged_in'] = True
                session['admin_uid'] = uid
                session['admin_name'] = name

                return redirect(url_for('admin'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')


# Route for admin registration
# Admin registration route
# Define WTForms registration form

from wtforms import Form, StringField, PasswordField, validators


class admin_RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)],
                             render_kw={'autofocus': True, 'placeholder': 'First Name'})
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)],
                            render_kw={'placeholder': 'Last Name'})
    email = StringField('Email', [validators.Length(min=6, max=100)],
                        render_kw={'placeholder': 'Email'})
    mobile = StringField('Mobile', [validators.Length(min=10, max=15)],
                         render_kw={'placeholder': 'Mobile'})
    address = StringField('Address', [validators.Length(min=1, max=200)],
                          render_kw={'placeholder': 'Address'})
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ], render_kw={'placeholder': 'Password'})
    confirm = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm Password'})
    user_type = StringField('User Type', render_kw={'placeholder': 'User Type'})  # Added field for user type
    confirm_code = StringField('Confirm Code',
                               render_kw={'placeholder': 'Confirm Code'})  # Added field for confirm code


# Admin registration route


@app.route('/admin_register', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_register():
    form = admin_RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            mobile = form.mobile.data
            address = form.address.data
            password = sha256_crypt.encrypt(str(form.password.data))
            user_type = form.type.data
            confirm_code = form.confirmCode.data

            # Create cursor
            cur = mysql.connection.cursor()

            # Check if email is already registered
            result = cur.execute("SELECT * FROM admin WHERE email = %s", (email,))
            if result > 0:
                flash('Email already registered', 'danger')
                cur.close()
                return redirect(url_for('admin_register'))

            # Insert user record into the database
            cur.execute(
                "INSERT INTO admin (firstName, lastName, email, mobile, address, password, type, confirmCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, email, mobile, address, password, user_type, confirm_code))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash('You are now registered and can log in', 'success')
            return redirect(url_for('admin_login'))
        except Exception as e:
            flash('An error occurred while registering: ' + str(e), 'danger')
            # Print the error message for debugging
            print('Error:', e)

    return render_template('admin_register.html', form=form)


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    order_rowss = curso.execute("SELECT * FROM cart")
    return render_template('pages/index.html', result=result,order_rowss=order_rowss, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM users")
    order_rowss = curso.execute("SELECT * FROM cart")
    return render_template('pages/all_orders.html', result=result,order_rowss=order_rowss, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)

@app.route('/cart_orders')
@is_admin_logged_in  # Assuming you have a decorator for admin login check
def cart_orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    order_rowss = curso.execute("SELECT * FROM cart")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/includes/cart_order.html', result=result, row=num_rows, order_rowss=order_rowss,
                   order_rows=order_rows,        users_rows=users_rows)
@app.route('/users')
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")

    result = curso.fetchall()
    order_rowss = curso.execute("SELECT * FROM cart")
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rowss=order_rowss,order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        author = request.form.get('author')
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        discount = request.form['discount']
        file = request.files['picture']

        if name and price and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")

            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)

                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()

                    # Check if 'author' is provided and not empty
                    if author is not None and author.strip() != "":
                        # Insert the record into the database
                        curs.execute(
                            "INSERT INTO products(pName, price, author, available, category, item, pCode, discount, picture) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",
                            (name, price, author, available, category, item, code, discount,picture))
                        mysql.connection.commit()

                        product_id = curs.lastrowid
                        curs.execute("INSERT INTO product_level(product_id) VALUES (%s)", [product_id])

                        if category in ['fiction', 'nonfiction', 'scifi', 'history']:
                            selected_categories = request.form.getlist(category)
                            for lev in ['fiction', 'nonfiction', 'scifi', 'history']:
                                if lev in selected_categories:
                                    yes = 'yes'
                                else:
                                    yes = 'no'
                                # Use parameterized queries to prevent SQL injection
                                query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                                curs.execute(query, (yes, product_id))
                            # Commit cursor after updating all levels
                            mysql.connection.commit()
                        else:
                            flash('Product level not found', 'danger')
                            return redirect(url_for('admin_add_product'))

                        # Close Connection
                        curs.close()

                        flash('Product added successfully', 'success')
                        return redirect(url_for('admin_add_product'))
                    else:
                        flash('Author field cannot be empty', 'danger')
                        return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not saved', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all forms', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        cursor = mysql.connection.cursor()

        # Retrieve product and product level information
        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        cursor.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = cursor.fetchone()

        if product:
            if request.method == 'POST':
                # Retrieve form data
                name = request.form.get('name')
                price = request.form.get('price')
                author = request.form.get('author')
                available = request.form.get('available')
                category = request.form.get('category')
                item = request.form.get('item')
                code = request.form.get('code')
                file = request.files.get('picture')

                # Print form data
                print("Name:", name)
                print("Price:", price)
                print("Author:", author)
                print("Available:", available)
                print("Category:", category)
                print("Item:", item)
                print("Code:", code)
                print("File:", file)  # This will print file information

                # Validate form data
                if all((name, price, author, available, category, item, code)):
                    filename = product['picture']
                    if file:
                        filename = secure_filename(file.filename)
                        if filename.lower().endswith(tuple(app.config['ALLOWED_EXTENSIONS'])):
                            file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
                        else:
                            flash('Unsupported file format', 'danger')
                            return redirect(url_for('edit_product', id=product_id))

                    # Update product information
                    cursor.execute(
                        "UPDATE products SET pName=%s, price=%s, author=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                        (name, price, author, available, category, item, code, filename, product_id)
                    )

                    # Update product level information
                    for lev in ['fiction', 'nonfiction', 'scifi', 'history']:
                        level = request.form.getlist(lev)
                        for l in level:
                            cursor.execute(f'UPDATE product_level SET {l}=%s WHERE product_id=%s', ('yes', product_id))
                            mysql.connection.commit()

                    flash('Product updated', 'success')
                    return redirect(url_for('edit_product', id=product_id))
                else:
                    flash('Please fill all fields', 'danger')
                    return redirect(url_for('edit_product', id=product_id))
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            flash('Product not found', 'danger')
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)

    if request.method == 'GET' and 'q' in request.args and request.args['q'].strip():
        q = request.args['q']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Close Connection
        cur.close()

        if products:
            flash('Showing result for: ' + q, 'success')
            noOfItems = get_no_of_items_in_cart()
            return render_template('search.html', products=products, form=form,noOfItems=noOfItems)
        else:
            flash('Nothing found for: ' + q, 'warning')
    elif request.method == 'GET' and 'q' in request.args and not request.args['q'].strip():
        flash('Please enter the book name', 'danger')
    elif request.method == 'POST':
        flash('Please use the search form to submit queries', 'danger')
    noOfItems = get_no_of_items_in_cart()
    return render_template('search.html', form=form ,noOfItems=noOfItems)


@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                noOfItems = get_no_of_items_in_cart()
                return render_template('profile.html', result=res, noOfItems=noOfItems)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


class UpdateRegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobile'})


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # Create Cursor
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                                      (name, email, password, mobile, q))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                noOfItems = get_no_of_items_in_cart()
                return render_template('user_settings.html', result=result, form=form,noOfItems=noOfItems)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


def fetch_product_data():
    # Implement this function to fetch product data from your database
    # Example code:
    product_data = {
        'fiction': [],
        'nonfiction': [],
        'scifi': [],
        'history': []
    }
    try:
        # Connect to your database and fetch product data
        # Example:
        # cursor.execute("SELECT * FROM products WHERE category = %s", ('fiction',))
        # fiction_products = cursor.fetchall()
        # for product in fiction_products:
        #     product_data['fiction'].append(product)
        # Repeat this process for other categories

        # For now, I'll return an empty product_data dictionary
        return product_data
    except Exception as e:
        print("Error fetching product data:", e)
        return None


@app.route('/wishlist', methods=['GET', 'POST'])
@is_logged_in
def wishlist():
    if request.method == 'GET':
        user_id = session.get('uid')
        if user_id:
            wishlist_items = retrieve_wishlist_items(user_id)
            # Fetch product data for wishlist items
            product_data = fetch_product_data(wishlist_items)  # Pass wishlist_items to fetch_product_data
            noOfItems = get_no_of_items_in_cart()
            return render_template('wish_list.html', items=wishlist_items, product_data=product_data,
                                   noOfItems=noOfItems)
        else:
            flash('Please log in to view your wishlist', 'warning')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Handle adding items to the wishlist
        item_id = request.form.get('item_id')
        if item_id:
            user_id = session.get('user_id')
            if user_id:
                add_to_wishlist(user_id, item_id)
                flash('Item added to wishlist successfully', 'success')
                return redirect(url_for('wishlist'))
            else:
                flash('Please log in to add items to your wishlist', 'warning')
                return redirect(url_for('login'))
        else:
            flash('Invalid request. Please try again.', 'danger')
            return redirect(url_for('wishlist'))

def retrieve_wishlist_items(user_id):
    wishlist_items = []
    try:
        # Get a connection from the pool
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                id, 
                pName, 
                price, 
                author, 
                available, 
                category, 
                item, 
                pCode, 
                picture, 
                date
            FROM 
                products 
            WHERE 
                id IN (SELECT item_id FROM wishlist WHERE uid = %s)
        """
        print("Executing query:", query)  # Print the query for debugging
        cursor.execute(query, (user_id,))
        columns = [column[0] for column in cursor.description]
        wishlist_items = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()  # Close the connection
        print("Successfully retrieved wishlist items:", wishlist_items)  # Print fetched data for debugging
    except mysql.connector.Error as e:
        print("MySQL Error retrieving wishlist items:", e)
    except Exception as e:
        print("Error retrieving wishlist items:", e)
    return wishlist_items


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist_route():
    user_id = session.get('uid')
    if not user_id:
        flash('Please log in to add items to your wishlist', 'warning')
        return redirect(url_for('login'))

    product_id = request.form.get('product_id')
    if not product_id:
        flash('Invalid request. Please try again.', 'danger')
        return redirect(url_for('wishlist'))

    added = add_to_wishlist(user_id, product_id)
    if added:
        flash('Item added to wishlist successfully', 'success')
    else:
        flash('Item added to wishlist successfully', 'info')
    return redirect(url_for('wishlist'))


def add_to_wishlist(user_id, item_id):
    try:
        # Create a cursor
        cursor = mysql.connection.cursor()

        # Insert the new wishlist item into the database
        cursor.execute("INSERT INTO wishlist (uid, item_id, created_at) VALUES (%s, %s, NOW())", (user_id, item_id))

        # Commit the transaction
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

    except Exception as e:
        print("Error adding item to wishlist:", e)




@app.route('/remove_item', methods=['POST'])
def remove_item():
    try:
        # Retrieve the item ID from the form data
        item_id = request.form.get('item_id')

        # Ensure that item_id is not empty
        if not item_id:
            raise ValueError("Item ID is empty")

        # Your code for deleting the item from the wishlist goes here

        # Acquire a connection from the pool
        connection = db_pool.get_connection()

        # Execute the SQL query to remove the item from the wishlist
        with connection.cursor() as cursor:
            # Construct the DELETE query for the wishlist table
            delete_query = "DELETE FROM wishlist WHERE item_id = %s"

            # Execute the DELETE query with the item_id parameter
            cursor.execute(delete_query, (item_id,))

        # Commit the transaction
        connection.commit()

        # Close the connection
        connection.close()
        # Redirect to the wishlist route after removing the item
        return redirect(url_for('wishlist'))

    except ValueError as ve:
        # Handle specific ValueError (e.g., empty item_id)
        print("Error removing item:", ve)
        return jsonify(error=str(ve)), 400  # Bad Request status code

    except Exception as e:
        # Handle any other exceptions, such as database errors
        print("Error removing item:", e)
        return jsonify(error="Failed to remove item"), 500  # Internal Server Error status code

    # Recommendation system


def fetch_product_data(cart_items):
    product_data = []
    try:
        # Get a connection from the pool
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        # Example query to fetch product data based on cart items or product IDs
        query = """
            SELECT 
                id, 
                pName, 
                price, 
                author, 
                available, 
                category, 
                item, 
                pCode, 
                picture, 
                date
            FROM 
                products 
            WHERE 
                id IN (%s)
        """
        # Extract product IDs from cart_items
        product_ids = [item['pid'] for item in cart_items]
        # Create a comma-separated string of product IDs for the SQL query
        product_ids_str = ','.join(map(str, product_ids))
        final_query = query % product_ids_str
        print("Executing query:", final_query)  # Print the query for debugging
        cursor.execute(final_query)
        columns = [column[0] for column in cursor.description]
        product_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()  # Close the connection
        print("Successfully fetched product data:", product_data)  # Print fetched data for debugging
    except Exception as e:
        print("Error fetching product data:", e)
    return product_data



@app.route('/mypurchase', methods=['GET'])
@is_logged_in
def my_purchase():
    if request.method == 'GET':
        user_id = session.get('uid')
        if user_id:
            try:
                cart_items = retrieve_cart_items(user_id)
                # Fetch product data for cart items
                product_data = fetch_product_data(cart_items)  # Implement this function to fetch product data based on cart items
                noOfItems = get_no_of_items_in_cart()
                return render_template('mypurchase.html', items=cart_items, product_data=product_data, noOfItems=noOfItems)
            except mysql.connector.errors.Error as e:
                print("MySQL Error retrieving cart items:", e)
                flash('Error retrieving cart items', 'danger')
                return redirect(url_for('index'))  # Redirect to home or product listing page
        else:
            flash('Please log in to view your purchases', 'warning')
            return redirect(url_for('login'))

def retrieve_cart_items(user_id):
    cart_items = []
    try:
        # Get a connection from the pool
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
    products.id, 
    products.pName, 
    products.price, 
    products.author, 
    products.available, 
    products.category, 
    products.item, 
    products.pCode, 
    products.picture, 
    products.date,
    mycart.payment,
    mycart.quantity
FROM 
    products 
INNER JOIN 
    mycart ON products.id = mycart.pid
WHERE 
    mycart.uid = %s;
        """
        print("Executing query:", query)  # Print the query for debugging
        cursor.execute(query, (user_id,))
        columns = [column[0] for column in cursor.description]
        cart_items = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()  # Close the connection
        print("Successfully retrieved cart items:", cart_items)  # Print fetched data for debugging
    except mysql.connector.Error as e:
        print("MySQL Error retrieving cart items:", e)
    except Exception as e:
        print("Error retrieving cart items:", e)
    return cart_items


@app.route('/remove_itemcart', methods=['POST'])
def remove_itemcart():
    try:
        # Retrieve the item ID from the form data
        item_id = request.form.get('item_id')

        # Ensure that item_id is not empty
        if not item_id:
            raise ValueError("Item ID is empty")

        # Acquire a connection from the pool
        connection = db_pool.get_connection()
        if connection is None:
            # Handle the case where the connection could not be established
            flash('Error connecting to the database', 'danger')
            return redirect(url_for('index'))  # Redirect to an appropriate page

        # Execute the SQL query to remove the item from the mycart table
        with connection.cursor() as cursor:
            # Construct the DELETE query for the mycart table
            delete_query = "DELETE FROM mycart WHERE pid = %s"

            # Execute the DELETE query with the item_id parameter
            cursor.execute(delete_query, (item_id,))

        # Commit the transaction
        connection.commit()

        # Close the connection
        connection.close()



        # Get the updated number of items in the cart
        noOfItems = get_no_of_items_in_cart()

        # Redirect to the mypurchase.html template after removing the item
        return render_template('mypurchase.html',noOfItems=noOfItems)

    except ValueError as ve:
        # Handle specific ValueError (e.g., empty item_id)
        error_message = "Error removing item: " + str(ve)
        print(error_message)
        flash(error_message, 'danger')
        return redirect(url_for('mypurchase'))

    except Exception as e:
        # Handle any other exceptions, such as database errors
        error_message = "Error removing item: " + str(e)
        print(error_message)
        flash(error_message, 'danger')
        return redirect(url_for('mypurchase'))



# Pickle the objects with a compatible protocol version


pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))




@app.route('/recommend')
def recommend_ui():
    noOfItems = get_no_of_items_in_cart()
    return render_template('recommend.html' , noOfItems=noOfItems)


@app.route('/recommend_books', methods=['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        if not user_input:  # Check if user_input is empty
            flash('Error: Please enter a search keyword', 'danger')
            return redirect(url_for('index'))  # Redirect to another route or page

        user_input = user_input.lower()  # Convert input to lowercase for case insensitivity
        matched_indices = [i for i, title in enumerate(pt.index.str.lower()) if user_input in title]  # Get indices of matched titles

        if len(matched_indices) == 0:
            flash('Error: Book not found', 'danger')
            return redirect(url_for('index'))  # Redirect to another route or page

        index = matched_indices[0]  # Use the first matched index for simplicity; you can modify this as needed
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'].str.lower() == pt.index[i[0]].lower()]  # Case-insensitive search
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(data)
        noOfItems = get_no_of_items_in_cart()
        return render_template('recommend.html', data=data ,noOfItems=noOfItems)
    except IndexError:
        flash('Error: Book not found', 'danger')
        return redirect(url_for('index'))  # Redirect to another route or page


@app.route('/payment_form', methods=['GET', 'POST'])
def payment_form():
    if request.method == 'POST':
        amount = request.form.get('amount')
        tax_amount = request.form.get('tax_amount')
        total_amount = request.form.get('total_amount')
        transaction_uuid = request.form.get('transaction_uuid')
        product_code = request.form.get('product_code')
        product_service_charge = request.form.get('product_service_charge')
        product_delivery_charge = request.form.get('product_delivery_charge')
        success_url = request.form.get('success_url')
        failure_url = request.form.get('failure_url')
        signed_field_names = request.form.get('signed_field_names')
        signature = request.form.get('signature')

        # Process the form data as needed, such as sending it to eSewa for payment processing
        # Example: send_payment_request(amount, tax_amount, total_amount, transaction_uuid, product_code, etc.)

        return redirect(success_url)  # Redirect to the success URL after processing the payment

    return render_template('proceedtopay.html')  # Render the payment form template for GET requests


@app.route('/process_rating', methods=['POST'])
def process_rating():
    if request.method == 'POST':
        # Get form data
        book_id = request.form.get('pid')
        rating = request.form.get('rating_value')

        # Get user ID from session
        userid = session.get('uid')

        # Print the data to check values (for debugging)
        print(f'Book ID: {book_id}, Rating: {rating}, User ID: {userid}')

        # Check if rating value is provided
        if rating:
            try:
                # Connect to MySQL and execute the insert query
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ratings (pid, rating_value, uid) VALUES (%s, %s, %s)", (book_id, rating, userid))
                conn.commit()
                cursor.close()

                # Flash a success message
                flash('Thank you for your Rating!', 'success')

                # Redirect to a specific URL or return a JSON response indicating success
                return jsonify({'success': True, 'message': 'Thank you for your Rating!'})
            except Exception as e:
                # Flash an error message
                flash('An error occurred while processing your rating.', 'error')

                # Return a JSON response indicating error
                return jsonify({'success': False, 'error': str(e)})
        else:
            # Flash a message for missing rating value
            flash('Rating value is missing.', 'error')

            # Return a JSON response indicating missing rating value
            return jsonify({'success': False, 'error': 'Rating value is missing'})

    # Return a JSON response indicating invalid request method
    return jsonify({'success': False, 'error': 'Invalid request method'})



if __name__ == '__main__':
    app.run(debug=True)
