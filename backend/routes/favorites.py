from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Favorite, Show

bp = Blueprint('favorites', __name__, url_prefix='/api/favorites')


@bp.route('/', methods=['GET'])
@bp.route('/list', methods=['GET'])
@jwt_required()
def list_favorites():
    """
    同时支持：
      GET /api/favorites/
      GET /api/favorites/list
    """
    user_id = get_jwt_identity()
    favs = (
        Favorite.query
        .filter_by(user_id=user_id)
        .order_by(Favorite.created_at.desc())
        .all()
    )
    return jsonify({
        'code': 0,
        'data': [f.to_dict() for f in favs]
    }), 200


@bp.route('/is_fav', methods=['GET'])
@jwt_required()
def is_favorite():
    user_id = get_jwt_identity()
    show_id = request.args.get('show_id', type=int)
    if not show_id:
        return jsonify({'code': 1, 'msg': '参数缺失'}), 400
    exists = Favorite.query.filter_by(user_id=user_id, show_id=show_id).first()
    return jsonify({'code': 0, 'data': {'is_fav': bool(exists)}}), 200


@bp.route('/add', methods=['POST'])
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    show_id = data.get('show_id')
    if not show_id:
        return jsonify({'code': 1, 'msg': '参数缺失'}), 400

    if Favorite.query.filter_by(user_id=user_id, show_id=show_id).first():
        return jsonify({'code': 1, 'msg': '已收藏'}), 200

    show = Show.query.get(show_id)
    if not show:
        return jsonify({'code': 1, 'msg': '演出不存在'}), 404

    fav = Favorite(user_id=user_id, show_id=show_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '收藏成功'}), 200


@bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_favorite():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    show_id = data.get('show_id')
    fav = Favorite.query.filter_by(user_id=user_id, show_id=show_id).first()
    if not fav:
        return jsonify({'code': 1, 'msg': '未收藏'}), 200

    db.session.delete(fav)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '取消收藏成功'}), 200
