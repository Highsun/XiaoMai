from datetime import datetime
from .extensions import db
from sqlalchemy.types import JSON

# ============ 用户模型 ============
class User(db.Model):
    __tablename__ = 'users'  # 设置表名为 'users'
    id            = db.Column(db.Integer, primary_key=True)  # 用户ID，整型，主键
    username      = db.Column(db.String(32), unique=True, nullable=False)  # 用户名，字符串，唯一，非空
    email         = db.Column(db.String(128), unique=True, nullable=False)  # 邮箱，字符串，唯一，非空
    password_hash = db.Column(db.String(128), nullable=False)  # 密码哈希值，字符串，非空
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间
    realname      = db.Column(db.String(64),  default="", nullable=False)  # 真实姓名，字符串，默认为空，非空
    gender        = db.Column(db.String(8),   default="保密", nullable=False)  # 性别，字符串，默认为"保密"，非空
    birthday      = db.Column(db.Date,        default=datetime(1970,1,1), nullable=False)  # 生日，日期类型，默认为1970-01-01，非空
    phone         = db.Column(db.String(20),  default="", nullable=False)  # 电话号码，字符串，默认为空，非空
    province      = db.Column(db.String(32),  default="", nullable=False)  # 省份，字符串，默认为空
    city          = db.Column(db.String(32),  default="", nullable=False)  # 城市，字符串，默认为空
    district      = db.Column(db.String(32),  default="", nullable=False)  # 区/县，字符串，默认为空
    address       = db.Column(db.String(128), default="", nullable=False)  # 地址，字符串，默认为空

    watchers = db.relationship('Watcher',  # 定义与观演人模型的关系
        backref='user',  # 反向引用，允许从观演人访问用户
        cascade='all, delete-orphan',  # 级联选项，当用户被删除时，删除所有相关的观演人
        lazy='dynamic'  # 动态加载，只有在访问时才加载观演人
    )

    def set_password(self, pwd: str):
        """设置密码，使用 bcrypt 哈希加密"""
        from .extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')

    def check_password(self, pwd: str) -> bool:
        """检查密码是否正确，使用 bcrypt 验证"""
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, pwd)

    def to_dict(self):
        """将用户对象转换为字典"""
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def __repr__(self):
        """返回用户对象的字符串表示形式"""
        return f"<User {self.username}>"

class Watcher(db.Model):
    __tablename__ = 'watchers'  # 设置表名为 'watchers'
    id         = db.Column(db.Integer, primary_key=True)  # 观演人ID，整型，主键
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # 用户ID，外键，关联到 users 表，删除用户时级联删除观演人，非空
    realname   = db.Column(db.String(64),  nullable=False, default='')  # 真实姓名，字符串，非空，默认为空
    id_number  = db.Column(db.String(32),  nullable=False, default='')  # 身份证号，字符串，非空，默认为空
    phone      = db.Column(db.String(20),  nullable=False, default='')  # 电话号码，字符串，非空，默认为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间

    def to_dict(self):
        """将观演人对象转换为字典"""
        return {
            'id':        self.id,
            'realname':  self.realname,
            'id_number': self.id_number,
            'phone':     self.phone,
        }

    def __repr__(self):
        """返回观演人对象的字符串表示形式"""
        return f"<Watcher {self.realname} of User {self.user_id}>"

# ============ 多对多中间表 ============
show_artists = db.Table(
    'show_artists',  # 表名
    db.Column('show_id',   db.Integer, db.ForeignKey('shows.id'),   primary_key=True),  # 演出ID，外键，关联到 shows 表，主键
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)   # 艺术家ID，外键，关联到 artists 表，主键
)

# ============ 艺术家 (Artist) ============
class Artist(db.Model):
    __tablename__ = 'artists'  # 设置表名为 'artists'
    id         = db.Column(db.Integer, primary_key=True)  # 艺术家ID，整型，主键
    name       = db.Column(db.String(128), nullable=False)  # 艺术家姓名，字符串，非空
    image_path = db.Column(db.String(256), nullable=False)  # 艺术家图片路径，字符串，非空
    link       = db.Column(db.String(256), nullable=True)  # 艺术家链接，字符串，可为空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，日期时间类型，默认为当前UTC时间，更新时自动更新

    shows = db.relationship(
        'Show',  # 关联的演出模型
        secondary=show_artists,  # 使用中间表 show_artists
        back_populates='artists',  # 反向引用，允许从演出访问艺术家
        lazy='dynamic'  # 动态加载，只有在访问时才加载演出
    )

    def to_dict(self):
        """将艺术家对象转换为字典"""
        return {
            'id':        self.id,
            'name':      self.name,
            'image_url': f"/uploads/{self.image_path}",  # 图片URL
            'link':      self.link
        }

    def __repr__(self):
        """返回艺术家对象的字符串表示形式"""
        return f"<Artist {self.name}>"

# ============ 演出 (Show) ============
class Show(db.Model):
    __tablename__ = 'shows'  # 设置表名为 'shows'
    id            = db.Column(db.Integer, primary_key=True)  # 演出ID，整型，主键
    title         = db.Column(db.String(128), nullable=False)  # 演出标题，字符串，非空
    tag           = db.Column(db.String(32), nullable=False)  # 演出标签，字符串，非空
    start_date    = db.Column(db.Date, nullable=False)  # 演出开始日期，日期类型，非空
    end_date      = db.Column(db.Date, nullable=True)  # 演出结束日期，日期类型，可为空
    location      = db.Column(db.String(256), nullable=False)  # 演出地点，字符串，非空
    price         = db.Column(JSON, nullable=False)  # 演出价格，JSON类型，非空
    status        = db.Column(db.String(32), nullable=False)  # 演出状态，字符串，非空
    ticket_status = db.Column(db.String(32), nullable=False)  # 票务状态，字符串，非空
    image_path    = db.Column(db.String(256), nullable=False)  # 演出图片路径，字符串，非空
    inventory     = db.Column(db.Integer, nullable=False, default=0, server_default='0')  # 库存，整型，非空，默认为0
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，日期时间类型，默认为当前UTC时间，更新时自动更新

    # —— 新增字段 ——
    sessions     = db.Column(JSON,           nullable=False, default={},  server_default='{}')  # 场次信息，JSON类型，非空，默认为空字典
    price_tiers  = db.Column(JSON,           nullable=False, default={},  server_default='{}')  # 价格阶梯，JSON类型，非空，默认为空字典
    map_url      = db.Column(db.String(256), nullable=False, default='',  server_default='')  # 地图URL，字符串，非空，默认为空

    artists = db.relationship(
        'Artist',  # 关联的艺术家模型
        secondary=show_artists,  # 使用中间表 show_artists
        back_populates='shows',  # 反向引用，允许从艺术家访问演出
        lazy='dynamic'  # 动态加载，只有在访问时才加载艺术家
    )

    def to_dict(self):
        """将演出对象转换为字典"""
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
    __tablename__ = 'orders'  # 设置表名为 'orders'
    id          = db.Column(db.Integer, primary_key=True)  # 订单ID，整型，主键
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 用户ID，外键，关联到 users 表，非空
    total_price = db.Column(db.Numeric(10, 2), nullable=False)  # 订单总价，数值类型，非空
    status      = db.Column(db.String(32), default='pending', nullable=False)  # 订单状态，字符串，默认为 'pending'，非空
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，日期时间类型，默认为当前UTC时间，更新时自动更新

    user  = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))  # 与用户模型的关系，反向引用，允许从用户访问订单
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan', lazy='joined')  # 与订单条目模型的关系，反向引用，级联删除

    def __repr__(self):
        """返回订单对象的字符串表示形式"""
        return f"<Order id={self.id} user={self.user_id} total={self.total_price}>"

# ============ 订单条目 (OrderItem) 模型 ============
class OrderItem(db.Model):
    __tablename__ = 'order_items'  # 设置表名为 'order_items'
    id         = db.Column(db.Integer, primary_key=True)  # 订单条目ID，整型，主键
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)  # 订单ID，外键，关联到 orders 表，非空
    show_id    = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)  # 演出ID，外键，关联到 shows 表，非空
    quantity   = db.Column(db.Integer, nullable=False)  # 数量，整型，非空
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # 单价，数值类型，非空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间
    seat_number   = db.Column(db.String(32),  default='')  # 座位号，字符串，默认为空
    qr_code       = db.Column(db.String(128), default='')  # 二维码，字符串，默认为空
    ticket_status = db.Column(db.String(16),  default='未使用')  # 票务状态，字符串，默认为 '未使用'
    expire_at     = db.Column(db.DateTime,    nullable=True)  # 过期时间，日期时间类型，可为空

    order = db.relationship('Order', back_populates='items')  # 与订单模型的关系，反向引用
    show  = db.relationship('Show')  # 与演出模型的关系

    def __repr__(self):
        """返回订单条目对象的字符串表示形式"""
        return f"<OrderItem order={self.order_id} show={self.show_id} qty={self.quantity}>"

# ============ 收藏夹（Favorites） ============
class Favorite(db.Model):
    __tablename__ = 'favorites'  # 设置表名为 'favorites'
    id = db.Column(db.Integer, primary_key=True)  # 收藏夹ID，整型，主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 用户ID，外键，关联到 users 表，非空
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)  # 演出ID，外键，关联到 shows 表，非空
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，日期时间类型，默认为当前UTC时间

    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic', cascade='all, delete-orphan'))  # 与用户模型的关系，反向引用，级联删除
    show = db.relationship('Show')  # 与演出模型的关系

    def to_dict(self):
        """将收藏夹对象转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'show': self.show.to_dict()  # 可直接把演出信息嵌入
        }