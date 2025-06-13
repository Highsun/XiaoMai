from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login      import LoginManager

db      = SQLAlchemy()
migrate = Migrate()
bcrypt  = Bcrypt()
jwt     = JWTManager()
login_manager = LoginManager()
