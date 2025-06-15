from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Watcher, User

# 创建一个名为 'user' 的 Blueprint，用于组织用户相关的路由
user_bp = Blueprint('user', __name__)


# 获取用户配置信息的路由（需要 JWT 认证）
@user_bp.route('/profile', methods=['GET'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def get_profile():
    """
    获取当前用户配置信息：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if not user:
        return jsonify(msg='用户不存在'), 404

    return jsonify({
        "realname": user.realname,
        "gender":   user.gender,
        "birthday": user.birthday.strftime('%Y-%m-%d') if user.birthday else "",  # 格式化日期
        "phone":    user.phone,
        "province": user.province,
        "city":     user.city,
        "district": user.district,
        "address":  user.address
    }), 200


# 更新用户配置信息的路由（需要 JWT 认证）
@user_bp.route('/profile', methods=['PUT'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def update_profile():
    """
    更新当前用户配置信息：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if not user:
        return jsonify(msg='用户不存在'), 404

    data = request.get_json() or {}  # 从请求中获取 JSON 数据
    # 更新用户信息
    user.realname = data.get('realname', "")
    user.gender   = data.get('gender', "保密")

    bday = data.get('birthday', "")
    try:
        user.birthday = (
            datetime.strptime(bday, "%Y-%m-%d").date() if bday else user.birthday
        )
    except:
        user.birthday = datetime(1970, 1, 1).date()

    user.phone    = data.get('phone', "")
    user.province = data.get('province', "")
    user.city     = data.get('city', "")
    user.district = data.get('district', "")
    user.address  = data.get('address', "")

    db.session.commit()  # 提交数据库会话，将更改保存到数据库
    return jsonify(msg='保存成功'), 200


# 获取用户观演人的路由（需要 JWT 认证）
@user_bp.route('/watchers', methods=['GET'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def get_watchers():
    """
    获取当前用户的所有观演人信息：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    data = [w.to_dict() for w in user.watchers]  # 将观演人信息转换为字典列表
    return jsonify(code=0, data=data), 200


# 添加用户观演人的路由（需要 JWT 认证）
@user_bp.route('/watchers', methods=['POST'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def add_watcher():
    """
    为当前用户添加观演人：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    # 限制每个用户最多只能添加 10 位观演人
    if User.query.get(user_id).watchers.count() >= 10:
        return jsonify(msg='最多只能添加 10 位观演人'), 400

    json = request.get_json() or {}  # 从请求中获取 JSON 数据
    # 创建观演人对象
    w = Watcher(
        user_id   = user_id,
        realname  = json.get('realname','').strip(),
        id_number = json.get('id_number','').strip(),
        phone     = json.get('phone','').strip()
    )
    db.session.add(w)  # 将观演人添加到数据库会话
    db.session.commit()  # 提交数据库会话，将更改保存到数据库
    return jsonify(code=0, data=w.to_dict()), 201


# 更新用户观演人的路由（需要 JWT 认证）
@user_bp.route('/watchers/<int:wid>', methods=['PUT'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def update_watcher(wid):
    """
    更新指定ID的观演人信息：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    # 查找指定ID且属于当前用户的观演人，如果不存在则返回404错误
    w = Watcher.query.filter_by(id=wid, user_id=user_id).first_or_404()
    json = request.get_json() or {}  # 从请求中获取 JSON 数据
    # 更新观演人信息
    for field in ('realname','id_number','phone'):
        if field in json:
            setattr(w, field, json[field].strip())
    db.session.commit()  # 提交数据库会话，将更改保存到数据库
    return jsonify(code=0, data=w.to_dict()), 200


# 删除用户观演人的路由（需要 JWT 认证）
@user_bp.route('/watchers/<int:wid>', methods=['DELETE'])
@jwt_required()  # 使用 jwt_required 装饰器来保护路由，需要提供有效的 JWT 才能访问
def delete_watcher(wid):
    """
    删除指定ID的观演人：需要 JWT 认证
    """
    user_id = get_jwt_identity()  # 从 JWT 中获取用户 ID
    # 查找指定ID且属于当前用户的观演人，如果不存在则返回404错误
    w = Watcher.query.filter_by(id=wid, user_id=user_id).first_or_404()
    db.session.delete(w)  # 从数据库会话中删除观演人
    db.session.commit()  # 提交数据库会话，将更改保存到数据库
    return jsonify(code=0, msg='删除成功'), 200