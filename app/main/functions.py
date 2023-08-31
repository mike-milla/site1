import africastalking
from flask import jsonify

from . import *

# import os
africastalking.initialize(
    username="joe2022",
    api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
    # justpaste.it/1nua8
)
sms = africastalking.SMS


def send_sms(phone, message):
    recipients = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is ", error)


# Test
# send_sms("+254729225710", "This is test message on Fleet.")
def gen_random(N):
    characters = string.ascii_letters + string.digits + '_'
    gen_str = ''.join(random.choice(characters) for _ in range(N))
    return gen_str


# Test    
# gen_random(N=4)

import bcrypt


def hash_password(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode()


def hash_password1(password):
    # Generate a random salt
    salt = bcrypt.gensalt()
    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hashed password as a utf-8 string
    return hashed_password.decode('utf-8')


def hash_verify1(password, hashed_password):
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# Test
# hash_password("kenya1234")
# Output
# $2b$12$LyTDdwhw5GHR6ILxTSrCfu69/x4xpihitQ3QZXUHOXa7YRQtg2FcO
def hash_verify(password, hashed_password):
    bytes = password.encode('utf-8')
    result = bcrypt.checkpw(bytes, hashed_password.encode())
    return result


# hash_verify("kenya1234", "$2b$12$LyTDdwhw5GHR6ILxTSrCfu69/x4xpihitQ3QZXUHOXa7YRQtg2FcO")
# Output
# Returns True/False
# generates Encryption Key
from cryptography.fernet import Fernet


def gen_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


# Test
# gen_key()
def load_key():
    return os.getenv('FLASK_CONFIG') or 'dPPHGwy78bxwspvOXXiGwxlKpUhPzlVSfY7OEUNwScA='


# Test
# print(load_key())
def encrypt(data):
    key = load_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data.decode()


# Test
# encrypt("+254729225710")
# Output
# gAAAAABjLX8d8JAsCS9ipJ8mO44Px4hb6GgfydOllU7P1JJqHWTQXEXchS-CMqsE2sSz2mDhrlGDjmmCYFCn4Em7X7F6nHVBTQ==
def decrypt(encrypted_data):
    key = load_key()
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()


# Test - Provide the Encrypted
# decrypt("gAAAAABjIY3vZqXEHBV9DIvizYUfsA6uPxx1pT16_OyopLYIAg4x52wUMwVWhRS2_IgVcQfKKZbWPRWmrcfJ15Nu3zj7rMdwWw==")
# Output
# +254729225710
def send_email(email, message):
    import smtplib
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("modcomlearning@gmail.com", "your password")
    # sending the mail
    s.sendmail("modcomlearning@gmail.com", email, message)
    # terminating the session
    s.quit()


# Test
# send_email("johndoe@gmail.com", "Test Email")

import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth


# In this fucntion we provide phone(used to pay), amount to be paid and invoice no being paid for.
def mpesa_payment(amount, phone, invoice_no):
    # GENERATING THE ACCESS TOKEN
    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"

    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    data = r.json()
    access_token = "Bearer" + ' ' + data['access_token']

    #  GETTING THE PASSWORD
    timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    business_short_code = "174379"
    data = business_short_code + passkey + timestamp
    encoded = base64.b64encode(data.encode())
    password = encoded.decode('utf-8')

    # BODY OR PAYLOAD
    payload = {
        "BusinessShortCode": "174379",
        "Password": "{}".format(password),
        "Timestamp": "{}".format(timestamp),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,  # use 1 when testing
        "PartyA": phone,  # change to your number
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
        "AccountReference": "account",
        "TransactionDesc": "account"
    }

    # POPULAING THE HTTP HEADER
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)


# Test
# mpesa_payment("2500", "254714356761", "NCV003")
import hashlib
import secrets


def generate_salt():
    # Generate a random 16-byte (128-bit) salt as a hexadecimal string
    return secrets.token_hex(16)


def hash_data(data):
    # Create a SHA-256 hash object
    salt = generate_salt()
    sha256 = hashlib.sha256()

    # Update the hash object with the concatenated data and salt
    sha256.update((data + salt).encode())

    # Get the digest (hash value) as a hexadecimal string
    digest = sha256.hexdigest()

    return digest


import re
import html


def sanitize_input(input_str):
    input_str = input_str.strip()
    input_str = html.escape(input_str)
    input_str = re.sub(r'[\'";`]', '', input_str)

    return input_str


def sanitize_data(data):
    for key, value in data.items():
        data[key] = sanitize_input(value)
    return data


def encrypt_key(key, val):
    keys = ['password']
    if key in keys:
        if key == 'password':
            val = hash_password(val)
        return encrypt(val)
    return val


def make_res(success=0, msg='', res='', cause=0):
    d = {
        'success': success,
        'message': msg,
        'response': res
    }
    if cause:
        d['cause'] = cause
    return jsonify(d)


def verify_access(jsn):
    auth = jsn.get('access_token')
    ref = jsn.get('refresh_token')
    return


def get_table(f):
    return 'app_users'


def remove_keys(keys, haystack):
    if type(keys) == str:
        haystack.pop(keys, None)
        return haystack
    for key in keys:
        haystack.pop(key, None)
    return haystack


def format_date(date_string):
    input_format = "%Y-%m-%d"
    date_object = datetime.datetime.strptime(str(date_string), input_format)
    output_format = "%Y-%m-%d %H:%M:%S.%f"
    formatted_date = date_object.strftime(output_format)

    return formatted_date


def getNow():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# print(hash_verify('pw19',decrypt('gAAAAABkzBvanbs0-B3UCLc8c5b7uwpxLraESJDDPSF9VVt02ot2hDvfXO2Mcaa2yGThf6Zul0bFuMx1E23ODP_Gs8Sv1AzRK1L-JwTJZ4A_G0QrGu7-a7GJ5mQQNHq9BtC35JPj5lHAHtLolPBNhbctvbG3vZ38SQ==')))
# print(encrypt(hash_password('4545')))
# print(hash_verify('4545','$2b$12$ZQlIAURsWaFEqR6OhBpRuerQddN2g/I3baf3aVKSLh5ng6IGNV8La'))
# print(hash_verify("$2b$12$Etn/cf3U5GFpW04jPnxYz.kJTBDwcBJvKfU7laUqW6LTpa0W.3uNW",sanitize_input('pw15')))


def can_rate(rating, followers):
    try:
        rating = float(rating)
        if not followers:
            return rating <= 1
        if rating <= 1:
            return True

        if rating <= 2:
            return followers >= THIRD_CLASS_STAR
        if rating <= 2.5:
            return followers >= SECOND_CLASS_STAR

        if rating <= 3:
            return followers >= FIRST_CLASS_STAR

        return

        pass
    except Exception as e:
        return


