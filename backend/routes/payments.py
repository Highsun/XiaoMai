# backend/routes/payments.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Order, OrderItem, Show
from decimal import Decimal
from datetime import datetime, timedelta
import random

bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    """支付页面打开时调用：创建一个 pending 的 Order，并插入一条 OrderItem"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    # 必须带上 show_id、amount、quantity 三个字段
    show_id = data.get('show_id')
    amount  = data.get('amount')
    quantity = data.get('quantity', 1)

    if show_id is None or amount is None:
        return jsonify({'code': 1, 'msg': '缺少必要参数'}), 400

    # 1. 创建订单
    order = Order(
        user_id=user_id,
        total_price=Decimal(str(amount)),
        status='pending'
    )
    db.session.add(order)
    db.session.flush()  # 拿到 order.id

    # 2. 计算单价并创建一条 OrderItem
    #    票状态先标记为 “未使用”，其他字段留空
    unit_price = (Decimal(str(amount)) / quantity).quantize(Decimal('0.00'))
    item = OrderItem(
        order_id=order.id,
        show_id=show_id,
        quantity=quantity,
        unit_price=unit_price,
        ticket_status='未使用'
    )
    db.session.add(item)

    db.session.commit()
    return jsonify({'code': 0, 'order_id': order.id}), 200


@bp.route('/complete', methods=['POST'])
@jwt_required()
def complete_order():
    """点击“下一步”时调用：把 pending → paid，并补全 OrderItem 的座位、二维码、过期时间"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    order_id = data.get('order_id')
    pay_method = data.get('method')

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order or order.status != 'pending':
        return jsonify({'code': 1, 'msg': '订单无效或已处理'}), 400

    # 1. 更新订单状态
    order.status = 'paid'

    # 2. 给已有的 OrderItem 填充 seat_number、qr_code、expire_at
    for oi in order.items:
        show = Show.query.get(oi.show_id)
        if not show:
            continue

        # 随机座位号：X区 YY排 ZZ号
        area = random.choice(['A','B','C','D','E'])
        row  = random.randint(1,30)
        num  = random.randint(1,20)
        oi.seat_number = f"{area}区 {row}排 {num}号"

        # 统一二维码
        oi.qr_code = '/uploads/已核销.png'

        # 过期时间 = 演出 start_date +1 天 的 23:59:59
        expire_day = show.start_date + timedelta(days=1)
        oi.expire_at = datetime.combine(expire_day, datetime.max.time()).replace(microsecond=0)

    db.session.commit()
    return jsonify({'code': 0, 'msg': '支付完成'}), 200


@bp.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_order():
    """超时或返回首页时调用：把 pending → cancelled"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    order_id = data.get('order_id')

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order or order.status != 'pending':
        return jsonify({'code': 1, 'msg': '订单无效或已处理'}), 400

    order.status = 'cancelled'
    db.session.commit()
    return jsonify({'code': 0, 'msg': '已取消'}), 200
