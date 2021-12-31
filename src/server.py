#! /usr/bin/env python3.9

"""
Stripe Flask app to route to Stripe's checkout session.
"""

import json
import os
import socket
import csv
# from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import CORS
import stripe

# # Setup Stripe python client library.
# load_dotenv(find_dotenv())

if os.environ.get('stage') == 'production':
    rooms_service_url = os.environ.get('rooms_service_url')
    customer_service_url = os.environ.get('customer_service_url')
    bookings_service_url = os.environ.get('bookings_service_url')
    stripe_service_url = os.environ.get('stripe_service_url')
    ui_service_url = os.environ.get('ui_service_url')
    booking_room_service_url = os.environ.get('room_booking_service_url')
else:
    rooms_service_url = os.environ.get('rooms_service_url_internal')
    customer_service_url = os.environ.get('customer_service_url_internal')
    bookings_service_url = os.environ.get('bookings_service_url_internal')
    stripe_service_url = os.environ.get('stripe_service_url_internal')
    ui_service_url = os.environ.get('ui_service_url_internal')
    booking_room_service_url = (
        os.environ.get('room_booking_service_url_internal'))

stripe.api_version = '2020-08-27'
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
app = Flask(__name__, template_folder='templates', static_folder='static')

CORS(app)
cors_config = {"origins": "*"}
cors = CORS(app, resources={r"/*]": cors_config})

JSON_PATH = os.path.join(app.static_folder, 'data', 'prices.json')


def get_prices():
    """
    Converts prices.csv from Stripe's product portal into JSON format
    """
    data = {}
    # Open a csv reader called DictReader
    csv_path = os.path.join(app.static_folder, 'data', 'prices.csv')
    with open(csv_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Convert each row into a dictionary
        # and add it to data
        for rows in csv_reader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['Product Name']
            print(rows)
            data[key] = {k: v for k, v in rows.items() if v}
    with open(JSON_PATH, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


@app.route("/health")
def health_check():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return jsonify(
            {
                "message": "Service is healthy.",
                "service:": "stripe",
                "ip_address": local_ip
            }
    ), 200


@app.route('/', methods=['GET'])
def get_example():
    """
    Renders temporary homepage
    """
    get_prices()
    return render_template('index.html')


@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    """
    Fetch the Checkout Session to display the JSON result on the success page
    """
    session_id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    return jsonify(checkout_session)


@app.route('/create-checkout-session/<int:room>/<int:book>', methods=['GET'])
def create_checkout_session(room, book):
    """
    Create new Checkout Session for the order
    """
    with open(JSON_PATH, encoding="utf-8") as json_file:
        data = json.load(json_file)
    price = data['Room ' + str(room)]['Price ID']

    try:
        booking_room_service_url='http://localhost:33000'
        # ?session_id={CHECKOUT_SESSION_ID}
        # means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=booking_room_service_url
            + '/send_notification/' + str(book),
            cancel_url=booking_room_service_url
            + '/delete_booking/' + str(book),
            payment_method_types=os.environ.get('PAYMENT_METHOD_TYPES')
            .split(','),
            mode='payment',
            line_items=[{
                'price': price,
                'quantity': 1
            }]
        )
        return redirect(checkout_session.url, code=303)
    except Exception as err:
        return jsonify(
            {
                "message": "An error occurred creating the payment session.",
                "error": str(err)
            }
        ), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
