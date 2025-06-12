from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from ..extensions import db
from ..models import User
from flask_jwt_extended import create_access_token
from flask import current_app
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email    = data.get('email')
    pwd      = data.get('password')
    confirm  = data.get('confirmPassword')  # 前端字段名

    # 1. 基本校验
    if not all([username, email, pwd, confirm]):
        return jsonify(msg='请填写完整信息'), 400
    if pwd != confirm:
        return jsonify(msg='两次输入的密码不一致'), 400

    # 2. 去重：用户名或邮箱都不能重复
    exists = User.query.filter(
        or_(User.username == username, User.email == email)
    ).first()
    if exists:
        return jsonify(msg='用户名或邮箱已存在'), 400

    # 3. 创建并存入数据库
    user = User(username=username, email=email)
    user.set_password(pwd)
    db.session.add(user)
    db.session.commit()

    return jsonify(msg='注册成功'), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    current_app.logger.info(f"💡 login payload → {data}")
    print("💡 login payload →", data, flush=True)

    account  = data.get('account')
    password = data.get('password')

    # 1. 基本校验
    if not account or not password:
        return jsonify(msg='请输入用户名/邮箱和密码'), 400

    # 2. 根据用户名或邮箱查询用户
    user = User.query.filter(
        or_(User.username == account, User.email == account)
    ).first()

    # 3. 校验用户存在且密码匹配
    if not user or not user.check_password(password):
        return jsonify(msg='用户名或密码错误'), 401

    # 4. 生成并返回 JWT
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200


@auth_bp.route('/userinfo', methods=['GET'])
@jwt_required()
def userinfo():
    # 从 JWT token 中提取身份（这里是 user.id）
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    return jsonify({
        "username": user.username,
        # 你还可以返回 email、avatar_url 等
    }), 200