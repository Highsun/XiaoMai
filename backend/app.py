# backend/app.py

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, bcrypt, jwt, login_manager

from .routes.show      import show_bp
from .routes.artist    import artist_bp
from .routes.auth      import auth_bp
from .routes.user      import user_bp
from .routes.orders    import bp as orders_bp
from .routes.favorites import bp as favorites_bp

import os

def create_app():
    # 不指定 static_folder，所有静态资源都通过下面 /uploads 路由来服务
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    # 初始化登录管理
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # ① 确保 UPLOAD_FOLDER 指向 backend/uploads 目录
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not app.config.get('UPLOAD_FOLDER'):
        app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
    else:
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.isabs(upload_dir):
            app.config['UPLOAD_FOLDER'] = os.path.join(basedir, upload_dir)

    # ② 允许跨域访问 /api/* 和 /uploads/* 路径，并允许 Authorization 头
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*":     {"origins": "*"},
            r"/uploads/*": {"origins": "*"}
        },
        allow_headers=["Content-Type", "Authorization"]
    )

    # ③ 初始化各类扩展（数据库、迁移、加密、JWT）
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ④ 注册各个蓝图
    app.register_blueprint(show_bp,       url_prefix='/api/shows')
    app.register_blueprint(artist_bp,     url_prefix='/api/artists')
    app.register_blueprint(auth_bp,       url_prefix='/api/auth')
    app.register_blueprint(user_bp,       url_prefix='/api/user')
    app.register_blueprint(orders_bp)     # 内部已设置 url_prefix '/api/orders'
    app.register_blueprint(favorites_bp)  # 内部已设置 url_prefix '/api/favorites'

    # ⑤ 暴露 uploads/ 下的静态文件
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ⑥ 根路由，仅作测试用
    @app.route('/')
    def index():
        return jsonify({
            "message": "XiaoMai Backend Running",
            "status":  "ok"
        }), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8888, debug=True)
