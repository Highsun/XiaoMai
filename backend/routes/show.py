# backend/routes/show.py

from flask import Blueprint, jsonify
from ..models import Show

show_bp = Blueprint('shows', __name__, url_prefix='/api/shows')

@show_bp.route('/', methods=['GET'])
def get_all_shows():
    shows = Show.query.order_by(Show.start_date).all()
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in shows]
    }), 200

@show_bp.route('/hot', methods=['GET'])
def get_hot_shows():
    hot = Show.query.filter_by(status='hot').order_by(Show.start_date).all()
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in hot]
    }), 200

@show_bp.route('/upcoming', methods=['GET'])
def get_upcoming_shows():
    upcoming = Show.query.filter_by(status='upcoming').order_by(Show.start_date).all()
    return jsonify({
        "code": 0,
        "message": "success",
        "data": [s.to_dict() for s in upcoming]
    }), 200

@show_bp.route('/<int:show_id>', methods=['GET'])
def get_show_detail(show_id):
    show = Show.query.get_or_404(show_id)
    return jsonify({
        "code": 0,
        "message": "success",
        "data": show.to_dict()
    }), 200
