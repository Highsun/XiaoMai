from flask import Blueprint, jsonify
from ..extensions import db
from ..models import Artist

artist_bp = Blueprint('artists', __name__)

@artist_bp.route('/', methods=['GET'])
def get_all_artists():
    """
    GET /api/artists/
    返回所有艺术家信息，按 name 字母顺序排列。
    """
    artists = Artist.query.order_by(Artist.name).all()
    data = [a.to_dict() for a in artists]
    return jsonify({"code": 0, "message": "success", "data": data}), 200

@artist_bp.route('/<int:artist_id>', methods=['GET'])
def get_artist_detail(artist_id):
    """
    GET /api/artists/<artist_id>
    返回单个艺术家详情。
    """
    artist = Artist.query.get_or_404(artist_id)
    return jsonify({"code": 0, "message": "success", "data": artist.to_dict()}), 200

# 后续也可扩展 POST/PUT/DELETE 接口
