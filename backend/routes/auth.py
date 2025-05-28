from flask       import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models     import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not all(k in data for k in ('username','email','password')):
        return jsonify(msg='参数不完整'), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg='用户名已存在'), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify(msg='邮箱已注册'), 400

    u = User(username=data['username'], email=data['email'])
    u.set_password(data['password'])
    db.session.add(u)
    db.session.commit()
    return jsonify(msg='注册成功'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if not all(k in data for k in ('username','password')):
        return jsonify(msg='参数不完整'), 400
    u = User.query.filter_by(username=data['username']).first()
    if not u or not u.check_password(data['password']):
        return jsonify(msg='用户名或密码错误'), 401

    token = create_access_token(identity=u.id)
    return jsonify(access_token=token), 200
