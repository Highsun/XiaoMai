from flask import Flask
from .config      import Config
from .extensions  import db, migrate, bcrypt, jwt
from .routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    return app

if __name__ == '__main__':
    create_app().run(debug=True, port=5000)
