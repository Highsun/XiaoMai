# backend/models.py

from datetime import datetime
from .extensions import db
from sqlalchemy.types import JSON

# ============ 用户模型 ============
class User(db.Model):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(32), unique=True, nullable=False)
    email         = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    realname      = db.Column(db.String(64),  default="", nullable=False)
    gender        = db.Column(db.String(8),   default="保密", nullable=False)
    birthday      = db.Column(db.Date,        default=datetime(1970,1,1), nullable=False)
    phone         = db.Column(db.String(20),  default="", nullable=False)
    province      = db.Column(db.String(32),  default="", nullable=False)
    city          = db.Column(db.String(32),  default="", nullable=False)
    district      = db.Column(db.String(32),  default="", nullable=False)
    address       = db.Column(db.String(128), default="", nullable=False)

    watchers = db.relationship('Watcher',
        backref='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def set_password(self, pwd: str):
        from .extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')

    def check_password(self, pwd: str) -> bool:
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, pwd)

    def to_dict(self):
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def __repr__(self):
        return f"<User {self.username}>"

class Watcher(db.Model):
    __tablename__ = 'watchers'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    realname   = db.Column(db.String(64),  nullable=False, default='')
    id_number  = db.Column(db.String(32),  nullable=False, default='')
    phone      = db.Column(db.String(20),  nullable=False, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':        self.id,
            'realname':  self.realname,
            'id_number': self.id_number,
            'phone':     self.phone,
        }

    def __repr__(self):
        return f"<Watcher {self.realname} of User {self.user_id}>"

# ============ 多对多中间表 ============
show_artists = db.Table(
    'show_artists',
    db.Column('show_id',   db.Integer, db.ForeignKey('shows.id'),   primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)

# ============ 艺术家 (Artist) ============
class Artist(db.Model):
    __tablename__ = 'artists'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(128), nullable=False)
    image_path = db.Column(db.String(256), nullable=False)
    link       = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shows = db.relationship(
        'Show',
        secondary=show_artists,
        back_populates='artists',
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'image_url': f"/uploads/{self.image_path}",
            'link':      self.link
        }

    def __repr__(self):
        return f"<Artist {self.name}>"

# ============ 演出 (Show) ============
class Show(db.Model):
    __tablename__ = 'shows'
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(128), nullable=False)
    tag           = db.Column(db.String(32), nullable=False)
    start_date    = db.Column(db.Date, nullable=False)
    end_date      = db.Column(db.Date, nullable=True)
    location      = db.Column(db.String(256), nullable=False)
    price         = db.Column(JSON, nullable=False)
    status        = db.Column(db.String(32), nullable=False)
    ticket_status = db.Column(db.String(32), nullable=False)
    image_path    = db.Column(db.String(256), nullable=False)
    inventory     = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # —— 新增字段 ——
    sessions     = db.Column(JSON,           nullable=False, default={},  server_default='{}')
    price_tiers  = db.Column(JSON,           nullable=False, default={},  server_default='{}')
    map_url      = db.Column(db.String(256), nullable=False, default='',  server_default='')

    artists = db.relationship(
        'Artist',
        secondary=show_artists,
        back_populates='shows',
        lazy='dynamic'
    )

    def to_dict(self):
        # 原有逻辑不变
        names = [a.name for a in self.artists.all()]
        if self.end_date:
            date_str = f"{self.start_date.strftime('%Y-%m-%d')}-{self.end_date.strftime('%Y-%m-%d')}"
        else:
            date_str = self.start_date.strftime('%Y-%m-%d')
        if isinstance(self.price, list):
            if len(self.price) == 1:
                price_str = f"{self.price[0]}元"
            else:
                price_str = f"{self.price[0]}-{self.price[-1]}元"
        else:
            price_str = str(self.price)

        # 在 to_dict 里额外返回新字段
        return {
            "id":          self.id,
            "title":       self.title,
            "tag":         self.tag,
            "start_date":  self.start_date.strftime('%Y-%m-%d'),
            "end_date":    self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            "location":    self.location,
            "price":       self.price,
            "status":      self.status,
            "ticket_status": self.ticket_status,
            "image_url":   f"/uploads/{self.image_path}",
            "artist_names":names,
            "sessions":    self.sessions,
            "price_tiers": self.price_tiers,
            "map_url":     self.map_url
        }

# ============ 订单 (Order) 模型 ============
class Order(db.Model):
    __tablename__ = 'orders'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status      = db.Column(db.String(32), default='pending', nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user  = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan', lazy='joined')

    def __repr__(self):
        return f"<Order id={self.id} user={self.user_id} total={self.total_price}>"

# ============ 订单条目 (OrderItem) 模型 ============
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    show_id    = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seat_number   = db.Column(db.String(32),  default='')
    qr_code       = db.Column(db.String(128), default='')
    ticket_status = db.Column(db.String(16),  default='未使用')
    expire_at     = db.Column(db.DateTime,    nullable=True)

    order = db.relationship('Order', back_populates='items')
    show  = db.relationship('Show')

    def __repr__(self):
        return f"<OrderItem order={self.order_id} show={self.show_id} qty={self.quantity}>"
