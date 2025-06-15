from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Order, OrderItem, Show, Artist, User

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

def ticket_to_dict(item, order, show, artist):
    return {
        "id": item.id,
        "createtime": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "artist": artist.name if artist else "",
        "avatar": artist.to_dict()["image_url"] if artist else "",
        "time": f"{show.start_date.strftime('%Y-%m-%d')} {show.sessions[0] if isinstance(show.sessions, list) and show.sessions else ''}",
        "venue": show.location,
        "seat": item.seat_number,
        "price": float(item.unit_price),
        "status": [item.ticket_status, order.status],  # 可以前端自己筛
        "qr": item.qr_code,
        "order_status": order.status,
        "ticket_status": item.ticket_status,
        "expire_at": item.expire_at.strftime('%Y-%m-%d %H:%M:%S') if item.expire_at else "",
        "show_title": show.title,
        "show_id": show.id,
    }

@bp.route('/my-tickets', methods=['GET'])
@jwt_required()
def get_my_tickets():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        for item in order.items:
            show = item.show
            # 拿第一个艺人
            artist = show.artists.first()
            result.append(ticket_to_dict(item, order, show, artist))
    return jsonify({"code": 0, "data": result})

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_history_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        for item in order.items:
            show = item.show
            artist = show.artists.first()
            # 历史订单同样可以复用 ticket_to_dict
            result.append(ticket_to_dict(item, order, show, artist))
    return jsonify({"code": 0, "data": result})
