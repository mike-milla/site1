# from functools import wraps
# from flask import request, jsonify
# import jwt

# # Replace this with your secret key used for JWT encoding and decoding
# SECRET_KEY = "your_secret_key_here"

# def access_granted(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token or not token.startswith('Bearer '):
#             return jsonify({"message": "Token is missing or invalid"}), 401

#         try:
#             # Extract the token from "Bearer <token>"
#             token = token.split(' ')[1]
#             # Verify the token and get the payload
#             payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#             # If the token is valid, call the target function
#             return func(*args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token has expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 401

#     return wrapper
# from flask import Flask, request, jsonify
# import jwt
# import datetime

# app = Flask(__name__)

# class JWT:
#     def __init__(self):
#         self.header = {
#             'alg': 'HS256',
#             'typ': 'JWT'
#         }

#     @staticmethod
#     def base64url_decode(data):
#         encoded = data.replace('-', '+').replace('_', '/')
#         padded = encoded + '=' * (4 - len(encoded) % 4)
#         return base64.b64decode(padded)

#     @staticmethod
#     def base64url_encode(data):
#         encoded = base64.b64encode(data).decode('utf-8')
#         return encoded.replace('+', '-').replace('/', '_').rstrip('=')

#     def generate_auth_token(self, user_id, secret_key):
#         header = self.base64url_encode(json.dumps(self.header))

#         payload = {
#             'user_id': user_id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)
#         }
#         payload = self.base64url_encode(json.dumps(payload))

#         secret_key += user_id
#         signature = jwt.encode(header + '.' + payload, secret_key, algorithm='HS256')
#         signature = self.base64url_encode(signature)

#         token = header + '.' + payload + '.' + signature
#         return token

#     def verify_auth_token(self, token, secret_key):
#         token_parts = token.split('.')
#         if len(token_parts) != 3:
#             return False

#         header, payload, signature = token_parts
#         decoded_payload = self.base64url_decode(payload).decode('utf-8')
#         payload = json.loads(decoded_payload)

#         secret_key += payload['user_id']

#         try:
#             jwt.decode(token, secret_key, algorithms=['HS256'])
#             return True
#         except jwt.ExpiredSignatureError:
#             return False
#         except jwt.InvalidTokenError:
#             return False

#     def get_token_data(self, token, secret_key):
#         token_parts = token.split('.')
#         if len(token_parts) != 3:
#             return False

#         header, payload, signature = token_parts
#         decoded_payload = self.base64url_decode(payload).decode('utf-8')
#         payload = json.loads(decoded_payload)

#         secret_key += payload['user_id']

#         try:
#             jwt.decode(token, secret_key, algorithms=['HS256'])
#             expired = payload['exp'] < datetime.datetime.utcnow().timestamp()
#             uid = payload['user_id']
#             return {
#                 "expired": expired,
#                 "uid": uid
#             }
#         except jwt.ExpiredSignatureError:
#             return {
#                 "expired": True,
#                 "uid": None
#             }
#         except jwt.InvalidTokenError:
#             return {
#                 "expired": False,
#                 "uid": None
#             }

# jwt_handler = JWT()

# @app.route('/protected_endpoint')
# def protected_endpoint():
#     token = request.headers.get('Authorization')
#     if not token or not token.startswith('Bearer '):
#         return jsonify({"message": "Token is missing or invalid"}), 401

#     token = token.split(' ')[1]
#     secret_key = "your_secret_key_here"
    
#     if jwt_handler.verify_auth_token(token, secret_key):
#         token_data = jwt_handler.get_token_data(token, secret_key)
#         if token_data["uid"]:
#             return jsonify({"message": "This is a protected endpoint", "user_id": token_data["uid"]}), 200
#         else:
#             return jsonify({"message": "Access denied"}), 403
#     else:
#         return jsonify({"message": "Invalid or expired token"}), 401

# if __name__ == '__main__':
#     app.run()
