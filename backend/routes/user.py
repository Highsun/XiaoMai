from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Watcher, User

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
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


@user_bp.route('/profile', methods=['PUT'])
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

    db.session.commit()
    return jsonify(msg='保存成功'), 200


@user_bp.route('/watchers', methods=['GET'])
@jwt_required()
def get_watchers():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = [w.to_dict() for w in user.watchers]
    return jsonify(code=0, data=data), 200


@user_bp.route('/watchers', methods=['POST'])
@jwt_required()
def add_watcher():
    user_id = get_jwt_identity()
    if User.query.get(user_id).watchers.count() >= 10:
        return jsonify(msg='最多只能添加 10 位观演人'), 400

    json = request.get_json() or {}
    w = Watcher(
        user_id   = user_id,
        realname  = json.get('realname','').strip(),
        id_number = json.get('id_number','').strip(),
        phone     = json.get('phone','').strip()
    )
    db.session.add(w)
    db.session.commit()
    return jsonify(code=0, data=w.to_dict()), 201


@user_bp.route('/watchers/<int:wid>', methods=['PUT'])
@jwt_required()
def update_watcher(wid):
    user_id = get_jwt_identity()
    w = Watcher.query.filter_by(id=wid, user_id=user_id).first_or_404()
    json = request.get_json() or {}
    for field in ('realname','id_number','phone'):
        if field in json:
            setattr(w, field, json[field].strip())
    db.session.commit()
    return jsonify(code=0, data=w.to_dict()), 200


@user_bp.route('/watchers/<int:wid>', methods=['DELETE'])
@jwt_required()
def delete_watcher(wid):
    user_id = get_jwt_identity()
    w = Watcher.query.filter_by(id=wid, user_id=user_id).first_or_404()
    db.session.delete(w)
    db.session.commit()
    return jsonify(code=0, msg='删除成功'), 200
