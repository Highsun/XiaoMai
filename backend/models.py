# backend/models.py

from datetime import datetime
from .extensions import db

# ============ 用户模型 ============
class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(32), unique=True, nullable=False)
    email         = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    realname  = db.Column(db.String(64),  default="")
    gender    = db.Column(db.String(8),   default="保密")
    birthday  = db.Column(db.Date,        default=datetime(1970,1,1))
    phone     = db.Column(db.String(20),  default="")
    province  = db.Column(db.String(32),  default="")
    city      = db.Column(db.String(32),  default="")
    district  = db.Column(db.String(32),  default="")
    address   = db.Column(db.String(128), default="")


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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<User {self.username}>"


# ============ 艺术家 (Artist) 模型 ============
class Artist(db.Model):
    __tablename__ = 'artists'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(128), nullable=False)
    image_path = db.Column(db.String(256), nullable=False)   # 相对 uploads/ 的子路径
    link       = db.Column(db.String(256), nullable=True)    # 艺术家个人链接
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 反向关系：一个 Artist 可拥有多场演出
    shows = db.relationship('Show', back_populates='artist', lazy='dynamic')

    def to_dict(self):
        return {
            'id':        self.id,
            'name':      self.name,
            'image_url': f"/uploads/{self.image_path}",
            'link':      self.link
        }

    def __repr__(self):
        return f"<Artist {self.name}>"


# ============ 演出 (Show) 模型 ============
class Show(db.Model):
    __tablename__ = 'shows'

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(128), nullable=False)    # 演出名称
    start_date = db.Column(db.Date, nullable=False)           # 开始日期
    end_date   = db.Column(db.Date, nullable=True)            # 结束日期（可选）
    location   = db.Column(db.String(256), nullable=False)    # 场馆/城市信息
    price      = db.Column(db.String(64), nullable=False)     # 价格描述
    status     = db.Column(db.String(32), nullable=False)     # hot / upcoming
    image_path = db.Column(db.String(256), nullable=False)    # 封面相对路径

    # —— 库存字段：默认 0，可动态更新 ——
    inventory  = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        server_default='0',
        comment="剩余可售票数"
    )

    # 外键关联 Artist
    artist_id  = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    artist     = db.relationship('Artist', back_populates='shows')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'start_date':  self.start_date.strftime('%Y-%m-%d'),
            'end_date':    self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'location':    self.location,
            'price':       self.price,
            'status':      self.status,
            'image_url':   f"/uploads/{self.image_path}",
            'artist_id':   self.artist_id,
            'inventory':   self.inventory
        }

    def __repr__(self):
        if self.end_date:
            return f"<Show {self.title} ({self.start_date}~{self.end_date})>"
        return f"<Show {self.title} ({self.start_date})>"


# ============ 订单 (Order) 模型 ============
class Order(db.Model):
    __tablename__ = 'orders'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status      = db.Column(db.String(32), default='pending', nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 关联用户和订单条目
    user        = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
    items       = db.relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def __repr__(self):
        return f"<Order id={self.id} user={self.user_id} total={self.total_price}>"


# ============ 订单条目 (OrderItem) 模型 ============
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    show_id    = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # 下单时单价
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联 Order 和 Show
    order      = db.relationship('Order', back_populates='items')
    show       = db.relationship('Show')

    def __repr__(self):
        return f"<OrderItem order={self.order_id} show={self.show_id} qty={self.quantity}>"
