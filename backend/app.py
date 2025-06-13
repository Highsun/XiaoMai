from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, bcrypt, jwt
from .routes.show import show_bp
from .routes.artist import artist_bp
from .routes.auth import auth_bp
import os

def create_app():
    # 不指定 static_folder，所有静态资源都通过下面 /uploads 路由来服务
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    # ----------------------------------
    # ① 确保 UPLOAD_FOLDER 指向 backend/uploads 目录
    # ----------------------------------
    # 如果你的 Config 中已经有 UPLOAD_FOLDER，那么就直接用它；否则，自动拼一个路径。
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not app.config.get('UPLOAD_FOLDER'):
        # 默认把项目结构中与本文件同级的 uploads/ 目录作为存储目录
        app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
    else:
        # 如果 Config 中指定了 UPLOAD_FOLDER，就可以添加校验
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.isabs(upload_dir):
            # 把相对路径也转成绝对路径
            app.config['UPLOAD_FOLDER'] = os.path.join(basedir, upload_dir)

    # ----------------------------------
    # ② 允许跨域访问 /uploads/* 路径（防止前端跨域被拦截）
    # ----------------------------------
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}, r"/uploads/*": {"origins": "*"}})
    # ----------------------------------
    # ③ 初始化各类扩展（数据库、迁移、加密、JWT）
    # ----------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # ----------------------------------
    # ④ 注册各个蓝图
    #    - 演出相关接口，前缀 /api/shows
    #    - 艺术家相关接口，前缀 /api/artists
    # ----------------------------------
    app.register_blueprint(show_bp,   url_prefix='/api/shows')
    app.register_blueprint(artist_bp, url_prefix='/api/artists')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # ----------------------------------
    # ⑤ 暴露 uploads/ 目录下的静态文件
    #    前端使用示例：
    #      GET http://<host>:<port>/uploads/concerts/DT.JPG
    #      GET http://<host>:<port>/uploads/artists/Jay.png
    #    Flask 会自动把位于 backend/uploads/concerts/*.png 或 backend/uploads/artists/*.jpeg 返回给调用者
    # ----------------------------------
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        # filename 形如 "concerts/DT.JPG" 或 "artists/Jay.png"
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ----------------------------------
    # ⑥ 根路由，仅作测试用
    # ----------------------------------
    @app.route('/')
    def index():
        return jsonify({"message": "XiaoMai Backend Running", "status": "ok"}), 200

    return app


if __name__ == '__main__':
    # 创建并运行 Flask 应用
    app = create_app()
    app.run(host='0.0.0.0', port=8888, debug=True)
