from flask import Flask, jsonify, g
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from config import config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
admin = Admin(template_mode='bootstrap3')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extensions
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
