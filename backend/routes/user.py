from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Watcher

bp = Blueprint('user', __name__)

@bp.route('/api/user/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify(code=0, data=current_user.to_dict())

@bp.route('/api/user/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    for field in ['realname','gender','birthday','phone','province','city','district','address']:
        if field in data:
            setattr(current_user, field, data[field])
    db.session.commit()
    return jsonify(code=0, message='更新成功')

@bp.route('/api/user/watchers', methods=['GET'])
@login_required
def get_watchers():
    data = [w.to_dict() for w in current_user.watchers]
    return jsonify(code=0, data=data)

@bp.route('/api/user/watchers', methods=['POST'])
@login_required
def add_watcher():
    if current_user.watchers.count() >= 10:
        return jsonify(code=1, message='最多只能添加 10 位观演人'), 400
    json = request.get_json()
    w = Watcher(
        user_id   = current_user.id,
        realname  = json.get('realname','').strip(),
        id_number = json.get('id_number','').strip(),
        phone     = json.get('phone','').strip()
    )
    db.session.add(w)
    db.session.commit()
    return jsonify(code=0, data=w.to_dict())

@bp.route('/api/user/watchers/<int:wid>', methods=['PUT'])
@login_required
def update_watcher(wid):
    w = Watcher.query.filter_by(id=wid, user_id=current_user.id).first_or_404()
    json = request.get_json()
    for field in ('realname','id_number','phone'):
        if field in json:
            setattr(w, field, json[field].strip())
    db.session.commit()
    return jsonify(code=0, data=w.to_dict())

@bp.route('/api/user/watchers/<int:wid>', methods=['DELETE'])
@login_required
def delete_watcher(wid):
    w = Watcher.query.filter_by(id=wid, user_id=current_user.id).first_or_404()
    db.session.delete(w)
    db.session.commit()
    return jsonify(code=0, message='删除成功')

@bp.route('/api/user/password', methods=['PUT'])
@login_required
def change_password():
    json = request.get_json()
    old_pw = json.get('old_password','')
    new_pw = json.get('new_password','')
    if not current_user.check_password(old_pw):
        return jsonify(code=1, message='旧密码不正确'), 400
    current_user.set_password(new_pw)
    db.session.commit()
    return jsonify(code=0, message='密码修改成功')
