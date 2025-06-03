from datetime import datetime
from .extensions import db

# ============ 用户模型（示例，仅做参考） ============
class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(32), unique=True, nullable=False)
    email         = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pwd: str):
        from .extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')

    def check_password(self, pwd: str) -> bool:
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, pwd)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<User {self.username}>"


# ============ 演出 (Show) 模型 ============
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)

    # 演出标题 / 演唱会名称
    title = db.Column(db.String(128), nullable=False)

    # 演出（开始）日期，例如 "2025-06-15"
    start_date = db.Column(db.Date, nullable=False)

    # 演出结束日期，可选
    end_date = db.Column(db.Date, nullable=True)

    # 场馆或城市信息，例如 "北京市·国家体育场-鸟巢"
    location = db.Column(db.String(256), nullable=False)

    # 价格信息，建议直接使用字符串，例如 "380元起"
    price = db.Column(db.String(64), nullable=False)

    # 演出状态：用于区分“热卖中（hot）”和“即将推出（upcoming）”
    status = db.Column(db.String(32), nullable=False)

    # 图像路径：相对于 uploads/ 根目录的子路径，例如 "concerts/DT.JPG"
    image_path = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        """
        序列化时，将 image_path 拼成 "/uploads/..." 相对 URL，前端只管加上域名即可。
        """
        return {
            'id': self.id,
            'title': self.title,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'location': self.location,
            'price': self.price,
            'status': self.status,
            'image_url': f"/uploads/{self.image_path}"
        }

    def __repr__(self):
        if self.end_date:
            return f"<Show {self.title} ({self.start_date}~{self.end_date})>"
        return f"<Show {self.title} ({self.start_date})>"


# ============ 艺术家 (Artist) 模型 ============
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    # 艺术家名称
    name = db.Column(db.String(128), nullable=False)

    # 图像路径：相对于 uploads/ 根目录的子路径，例如 "artists/Jay.png"
    image_path = db.Column(db.String(256), nullable=False)

    # 艺术家个人链接，可选，例如个人官网、社交媒体主页等
    link = db.Column(db.String(256), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': f"/uploads/{self.image_path}",
            'link': self.link
        }

    def __repr__(self):
        return f"<Artist {self.name}>"
