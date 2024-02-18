from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import jwt
from aes import decrypt, encrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tugas_sql:12345@localhost/db_all_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db) 


class AllUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), nullable=True)
    data = db.Column(db.Text)

SECRET_KEY = b'secretkey1234567' 

def generate_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    

# Middleware untuk manajemen log
@app.before_request
def log_request_info():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header
        payload = decode_token(token)
        if payload:
            method = request.method
            path = request.path
            data = request.data.decode('utf-8')
            username = AllUsers.query.get(payload['user_id']).username if 'user_id' in payload else None
    
            log_entry = Log(method=method, path=path, username=username, data=data)
            db.session.add(log_entry)
            db.session.commit()
    
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Cek apakah username dan password cocok
    user = AllUsers.query.filter_by(username=username).first()
    if user and decrypt(user.password) == password:
        token = generate_token(user.id)
        return jsonify({'status': 'success', 'token': token}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401


# Endpoint CRUD untuk User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Cek apakah username sudah ada dalam database
    existing_user = AllUsers.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409  # Conflict
    
    # Jika tidak ada, buat pengguna baru
    new_user = AllUsers(username=data['username'], password=encrypt(data['password']))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User created successfully'}), 201  # Created


@app.route('/users', methods=['GET'])
def get_all_users():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'status': 'error', 'message': 'Missing authorization header'}), 401
    
    token = auth_header
    payload = decode_token(token)
    
    if not payload:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    
    users = AllUsers.query.order_by(AllUsers.id).all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username
        }
        user_list.append(user_data)
    return jsonify({'status': 'success', 'data': user_list})


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'status': 'error', 'message': 'Missing authorization header'}), 401
    
    token = auth_header
    payload = decode_token(token)
    
    if not payload:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    
    user = AllUsers.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'username': user.username
        }
        return jsonify({'status': 'success', 'user': user_data})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'status': 'error', 'message': 'Missing authorization header'}), 401
    
    token = auth_header
    payload = decode_token(token)
    
    if not payload:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    
    user = AllUsers.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    data = request.get_json()
    
    # Check if the new username already exists
    if 'username' in data:
        existing_user = AllUsers.query.filter(AllUsers.username == data['username']).filter(AllUsers.id != user_id).first()
        if existing_user:
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
    
    user.username = data.get('username', user.username)
    user.password = encrypt(data.get('password', decrypt(user.password)))
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'User updated successfully'}), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'status': 'error', 'message': 'Missing authorization header'}), 401
    
    token = auth_header
    payload = decode_token(token)
    
    if not payload:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    
    user = AllUsers.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
