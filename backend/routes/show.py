from flask import Blueprint, jsonify
from ..models import Show

show_bp = Blueprint('shows', __name__, url_prefix='/api/shows')

# 定义路由，获取所有演出信息
@show_bp.route('/', methods=['GET'])
def get_all_shows():
    """
    获取所有演出信息，并按照演出开始时间排序
    """
    # 查询数据库中所有演出信息，并按照开始时间升序排序
    shows = Show.query.order_by(Show.start_date).all()
    # 将查询结果转换为字典列表，并封装在JSON响应中返回
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in shows]
    }), 200

# 定义路由，获取热门演出信息
@show_bp.route('/hot', methods=['GET'])
def get_hot_shows():
    """
    获取状态为 'hot' 的热门演出信息，并按照演出开始时间排序
    """
    # 查询数据库中状态为 'hot' 的演出信息，并按照开始时间升序排序
    hot = Show.query.filter_by(status='hot').order_by(Show.start_date).all()
    # 将查询结果转换为字典列表，并封装在JSON响应中返回
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in hot]
    }), 200

# 定义路由，获取即将到来的演出信息
@show_bp.route('/upcoming', methods=['GET'])
def get_upcoming_shows():
    """
    获取状态为 'upcoming' 的即将到来的演出信息，并按照演出开始时间排序
    """
    # 查询数据库中状态为 'upcoming' 的演出信息，并按照开始时间升序排序
    upcoming = Show.query.filter_by(status='upcoming').order_by(Show.start_date).all()
    # 将查询结果转换为字典列表，并封装在JSON响应中返回
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in upcoming]
    }), 200

# 定义路由，获取指定ID的演出详细信息
@show_bp.route('/<int:show_id>', methods=['GET'])
def get_show_detail(show_id):
    """
    根据演出ID获取演出详细信息
    """
    # 根据ID查询数据库中的演出信息，如果不存在则返回404错误
    show = Show.query.get_or_404(show_id)
    # 将查询结果转换为字典，并封装在JSON响应中返回
    return jsonify({
        "code": 0,
        "message": "success",
        "data": show.to_dict()
    }), 200