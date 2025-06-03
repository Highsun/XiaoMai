from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Show

show_bp = Blueprint('shows', __name__)

@show_bp.route('/', methods=['GET'])
def get_all_shows():
    """
    GET /api/shows/
    返回所有演出信息，按 start_date 升序排列。
    """
    shows = Show.query.order_by(Show.start_date).all()
    data = [s.to_dict() for s in shows]
    return jsonify({"code": 0, "message": "success", "data": data}), 200

@show_bp.route('/hot', methods=['GET'])
def get_hot_shows():
    """
    GET /api/shows/hot
    返回所有 status='hot' 的演出，按 start_date 升序排列。
    """
    hot_list = Show.query.filter_by(status='hot').order_by(Show.start_date).all()
    data = [s.to_dict() for s in hot_list]
    return jsonify({"code": 0, "message": "success", "data": data}), 200

@show_bp.route('/upcoming', methods=['GET'])
def get_upcoming_shows():
    """
    GET /api/shows/upcoming
    返回所有 status='upcoming' 的演出，按 start_date 升序排列。
    """
    upcoming_list = Show.query.filter_by(status='upcoming').order_by(Show.start_date).all()
    data = [s.to_dict() for s in upcoming_list]
    return jsonify({"code": 0, "message": "success", "data": data}), 200

@show_bp.route('/<int:show_id>', methods=['GET'])
def get_show_detail(show_id):
    """
    GET /api/shows/<show_id>
    返回单条演出详情（含 image_url）。
    """
    show = Show.query.get_or_404(show_id)
    return jsonify({"code": 0, "message": "success", "data": show.to_dict()}), 200

# 如果后续需要 POST/PUT/DELETE，可以在这里扩展接口：
# @show_bp.route('/', methods=['POST'])     # 创建新演出
# @show_bp.route('/<int:show_id>', methods=['PUT'])   # 更新演出信息
# @show_bp.route('/<int:show_id>', methods=['DELETE'])# 删除演出
