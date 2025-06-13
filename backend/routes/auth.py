from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_
from datetime import datetime
from ..extensions import db
from ..models import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

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
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token), 200


@auth_bp.route('/userinfo', methods=['GET'])
@jwt_required()
def userinfo():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    return jsonify({
        "id":       user.id,
        "username": user.username,
        "email":    user.email,
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    return jsonify({
        "realname": user.realname,
        "gender":   user.gender,
        "birthday": user.birthday.strftime('%Y-%m-%d') if user.birthday else "",
        "phone":    user.phone,
        "province": user.province,
        "city":     user.city,
        "district": user.district,
        "address":  user.address
    }), 200


@auth_bp.route('/profile', methods=['PUT', 'POST'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    data = request.get_json() or {}
    user.realname = data.get('realname', "")
    user.gender   = data.get('gender', "保密")

    bday = data.get('birthday', "")
    try:
        user.birthday = datetime.strptime(bday, "%Y-%m-%d").date() if bday else user.birthday
    except ValueError:
        user.birthday = datetime(1970, 1, 1).date()

    user.phone    = data.get('phone', "")
    user.province = data.get('province', "")
    user.city     = data.get('city', "")
    user.district = data.get('district', "")
    user.address  = data.get('address', "")

    db.session.commit()
    return jsonify(msg='保存成功'), 200


@auth_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.get_json() or {}
    old_pwd     = data.get('old_password', '').strip()
    new_pwd     = data.get('new_password', '').strip()
    confirm_pwd = data.get('confirm_password', '').strip()

    # 基本校验
    if not all([old_pwd, new_pwd, confirm_pwd]):
        return jsonify(msg='请填写旧密码、新密码及确认密码'), 400
    if new_pwd != confirm_pwd:
        return jsonify(msg='两次新密码不一致'), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    # 验证旧密码
    if not user.check_password(old_pwd):
        return jsonify(msg='旧密码不正确'), 401

    # 设置新密码
    user.set_password(new_pwd)
    db.session.commit()
    return jsonify(msg='密码修改成功'), 200


@auth_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    注销当前用户：删除用户及其所有关联记录
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg='用户不存在'), 404

    # 删除用户会级联删除 watchers
    db.session.delete(user)
    db.session.commit()

    return jsonify(msg='账号已成功注销'), 200
